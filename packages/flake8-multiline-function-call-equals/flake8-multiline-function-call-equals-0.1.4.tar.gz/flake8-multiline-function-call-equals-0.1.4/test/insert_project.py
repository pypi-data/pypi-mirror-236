import argparse
import psycopg2 as pg
import yaml


def args():
    '''
    Get the CLI arguments for this tool
    '''
    args = argparse.ArgumentParser(description='Add new projects to the database')
    args.add_argument('project_names', nargs="+")
    args.add_argument('-c' '--config-file', dest='config_file', required=True)

    return args.parse_args()


def argsanity(args):
    '''
    Ensure that the arguments are sane and perform the necessary ETL.

    Ensure that args.project_names contains a list of 1-typles, 
        each containing the name of a project to be inserted into the database.
    This is necessary for `main`'s executemany to work correctly
    '''
    args.project_names = [(i,) for i in args.project_names]
    return args


def main(args):
    '''
    Given the commandline arguments, write everything to the database
    '''

    # read the config
    with open(args.config_file) as infile:
        conf = yaml.load(infile.read(), Loader=yaml.Loader)
        conf = conf['database']

    # connect to the database
    with pg.connect(host = conf['host'],
                    database = conf['db_name'],
                    user = conf['user'],
                    password = conf['pass']) as conn:

        conn.set_session(autocommit=True)
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO admin.projects(title) VALUES (%s)""", args.project_names)


if __name__ == "__main__":
    main(argsanity(args()))
