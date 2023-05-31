import os #Corey Python Module

from deta import Deta #pip install deta
from dotenv import load_dotenv #pip install python-dotenv


# Load the environment variables
load_dotenv()
DETA_PROJECT_KEY = os.getenv('DETA_PROJECT_KEY')
# ---- ####### ----

# Initialze with project key
deta = Deta(DETA_PROJECT_KEY)

# Connect to db
db = deta.Base("finance-data")

def insert_period(period, incomes, expenses, comment):
    '''Returns the report on a successful creation, otherwise raises an error'''
    return db.put({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})

def fetch_all_periods():
    '''Returns a dict of all periods'''
    res = db.fetch()
    return res.items

def get_period(period):
    '''If not found, the function will return None'''
    return db.get(period)