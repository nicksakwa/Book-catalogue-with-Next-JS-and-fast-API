# book-catalog-app/backend/app/__init__.py

# This file explicitly imports the submodules so they are recognized 
# by the 'app' package, resolving the ImportError: cannot import name 'crud'.

from . import crud
from . import models
from . import schemas
from . import database