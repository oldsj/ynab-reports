from ynab.api import get_all_transactions
from pprint import pprint

transactions = get_all_transactions()
for transaction in transactions:
    pprint(transaction)
