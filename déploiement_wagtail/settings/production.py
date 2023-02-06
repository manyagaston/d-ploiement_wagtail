from .base import *

DEBUG = False

SECRET_KEY = "esd+g0%f$2o+5)80gjg9dg798v#k0m%q7o%t7l9=q47&0%z-tj"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["JManya.pythonanywhere.com "]

ROOT_URLCONF = "déploiement_wagtail.urls"

try:
    from .local import *
except ImportError:
    pass
