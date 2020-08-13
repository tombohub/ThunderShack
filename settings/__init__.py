from decouple import config
from .base import *

if config('DJANGO_ENVIRONMENT') == 'development':
    from. development import *
else:
    from .production import *
