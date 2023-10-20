import ast
import importlib.metadata


class Visitor(ast.NodeVisitor):

    def __init__(self):
        self.problems = []

        # messages / Error codes
        self.errors = {100: "EQA100 Too many whitespaces surrounding assignment operator in single-line function call",
                       101: "EQA101 Too many whitespaces surrounding assignment operator in multiline function call",
                       102: "EQA102 Too few whitespaces surrounding assignment operator in multiline function call",
                       103: "EQA103 Empty line in multiline function call",
                       104: "EQA104 Multiple arguments on the same line in multiline function call",
                       105: "EQA105 First argument does not start on the call line in multiline function call",
                       106: "EQA106 Closing paren is on the same line as the last argument",
                       }

    def visit_Call(self, node):
        sofar = node.func.end_col_offset + 1  # +1 for the paren

        for k,keyword in enumerate(node.keywords):
            if keyword.arg is None:
                continue

            if node.end_lineno - node.lineno == 0:  # single-line call
                if k == 0:
                    args = node.args
                    if args:
                        arg = args[-1]
                        sofar = arg.end_col_offset + 2  # comma and space

                self.processSingleLineCall(keyword, sofar)
                sofar = keyword.value.end_col_offset
                sofar += 2  # comma and space

            else:  # multiline call
                self.processMultiLineCall(keyword, node.func.end_col_offset+1)  # +1 for the paren

                args = node.args + node.keywords
                for k1,k2 in zip(args, args[1:]):  # check for empty lines
                    if getattr(k2, 'lineno', getattr(getattr(k2, 'value', None), 'lineno', None)) > getattr(k1, 'end_lineno', getattr(getattr(k1, 'value', None), 'end_lineno', None))+1:
                        self.problems.append((k2.value.lineno-1, 0, self.errors[103]))
                        continue
        
                    if getattr(k2, 'lineno', getattr(getattr(k2, 'value', None), 'lineno', None)) == getattr(k1, 'end_lineno', getattr(getattr(k1, 'value', None), 'end_lineno', None)):
                        self.problems.append((getattr(k2.value, 'lineno', getattr(k2, 'lineno', None)), 0, self.errors[104]))
                        continue


        if node.end_lineno - node.lineno != 0:  # multiline function call
            # ensure the first argument is on the same line as the function call
            args = node.args + node.keywords
            if args:
                n = args[0]
                if hasattr(n, 'value') and hasattr(n.value, 'lineno'):
                    nlineno = n.value.lineno
                else:
                    nlineno = n.lineno
    
                if nlineno > node.lineno:
                    print(args[0].__dict__)  ##
                    lineno = getattr(args[0], 'lineno', getattr(getattr(args[0], 'value', None), 'lineno', None))
                    col = getattr(args[0], 'col_offset', getattr(getattr(args[0], 'value', None), 'col_offset', None))
                    self.problems.append((lineno, col, self.errors[105]))
    
                # ensure that the close-paren is on its own line
                if hasattr(args[-1], 'value') and hasattr(args[-1].value, 'end_lineno'):
                    nendlineno = args[-1].value.end_lineno
                else:
                    nendlineno = args[-1].end_lineno
    
                if node.end_lineno==nendlineno and len(node.args)>1:
                    self.problems.append((node.end_lineno, node.end_col_offset, self.errors[106]))
    
                # no blank lines before the closing paren
                larg = args[-1]
                largLine = getattr(larg, 'end_lineno', getattr(getattr(larg, 'value', None), 'end_lineno', None))
            
                if node.end_lineno > largLine + 1:
                    self.problems.append((node.end_lineno, 0, self.errors[103]))

        self.generic_visit(node)

    def processSingleLineCall(self, keyword, startCol):
        arg = keyword.arg
        val = keyword.value

        if val.col_offset > startCol + len(arg) + 1:  # +1 for the `=`
            self.problems.append((keyword.value.lineno, startCol, self.errors[100]))


    def processMultiLineCall(self, keyword, startCol):
        arg = keyword.arg
        val = keyword.value

        if val.col_offset > startCol + len(arg) + 3:  # 3 because ` = `
            self.problems.append((val.lineno, startCol, self.errors[101]))
            return

        if val.col_offset < startCol + len(arg) + 3:  # 3 because ` = `
            self.problems.append((val.lineno, startCol, self.errors[102]))


class Plugin:
    name = __name__
    version = importlib.metadata.version(__name__)

    def __init__(self, tree):
        self._tree = tree

    def run(self):
        v = Visitor()
        v.visit(self._tree)
        for line, col, msg in v.problems:
            yield line, col, msg, type(self)
