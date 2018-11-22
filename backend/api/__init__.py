from flask import Blueprint
api = Blueprint('api', 'api', url_prefix='', static_folder='../../instance/dist/static')
from .dataset_api import *
from .document_api import *
from .project_api import *
from .user_api import *
from .summary_api import *









