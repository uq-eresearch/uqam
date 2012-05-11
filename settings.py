# Django settings for uqam project.
import os.path
if os.path.exists('development_mode'):
    from dev_settings import *
else:
    from default_settings import *


TEST_RUNNER = 'common.testrunner.NoDbTestRunner'
