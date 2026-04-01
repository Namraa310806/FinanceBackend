"""Select settings module based on the DJANGO_ENV environment variable."""

import os

env = os.getenv('DJANGO_ENV', 'development').lower()

if env == 'production':
    from .production import *  # noqa: F403, F401
else:
    from .development import *  # noqa: F403, F401

