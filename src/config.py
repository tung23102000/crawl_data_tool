from os import *
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
parent_directory = path.dirname(basedir)
load_dotenv(path.join(parent_directory, '.env')) 

URL_PAGE='https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index&indexSelect=-1'

DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_HOST = environ.get('DB_HOST')
DB_PORT = environ.get('DB_PORT')
DB_DATABASE = environ.get('DB_DATABASE')

