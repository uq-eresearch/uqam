# Django settings for uqam project.
import os.path
import socket

hostname = socket.gethostname()

if os.path.exists('development_mode'):
    from dev_settings import *
elif hostname.endswith('uat'):
    from uat_settings import *
else:
    from default_settings import *


#TEST_RUNNER = 'common.testrunner.NoDbTestRunner'
