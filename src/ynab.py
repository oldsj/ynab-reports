import os
import json
from pprint import pprint
from dotenv import load_dotenv
import requests

load_dotenv()

ynab_api = "https://api.youneedabudget.com/v1"
api_key = os.getenv("YNAB_API_KEY")
budget_id = os.getenv("YNAB_BUDGET_ID")
headers = {"accept": "application/json", "Authorization": f"Bearer {api_key}"}

categories = requests.get(f"{ynab_api}/budgets/{budget_id}/categories", headers=headers)
category_groups = categories.json()["data"]["category_groups"]

pprint(category_groups)
