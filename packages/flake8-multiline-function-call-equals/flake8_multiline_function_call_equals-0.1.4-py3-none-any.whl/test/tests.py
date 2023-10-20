import sys; sys.path.append('..')  # noqa
import os;  os.environ['RANDOM_QBIT_CONFIG_PATH'] = os.path.join(os.path.dirname(os.path.dirname(__file__)),  # noqa
                                                                'test_master_config.yaml')  # noqa

from SocialCollector.all_tests import run_tests  # noqa


failure = run_tests.run_smoke_tests('test_config.yaml')
if failure:
    sys.exit(1)
