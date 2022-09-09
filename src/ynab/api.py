import pandas as pd
import ynab_api
from functools import lru_cache

from ynab.config import get_ynab_config
from ynab_api.api import transactions_api


api_config, config = get_ynab_config()


@lru_cache(maxsize=0)
def get_ynab_dataset(min_date=None, max_date=None):
    categories_to_exclude = config.get("categories_to_exclude", [])

    data = get_all_transactions()
    df = pd.DataFrame(data)

    df = df[lambda d: d.deleted == False]  # Remove the deleted transactions
    df = df[lambda d: d.approved == True]  # Remove the non-approved transactions
    df["exclude"] = df.category_name.isin(categories_to_exclude)  # Mark
    df["date"] = pd.to_datetime(df.date, format="%Y-%m-%d")
    if min_date:
        df = df[lambda d: d.date >= min_date]
    if max_date:
        df = df[lambda d: d.date <= max_date]
    df = df.assign(amount=lambda d: d.amount / 1000)
    return df


def get_all_transactions(budget_id: str = config["budget_id"]) -> list:
    with ynab_api.ApiClient(api_config) as api_client:
        api_instance = transactions_api.TransactionsApi(api_client)
        try:
            api_response = api_instance.get_transactions(config["budget_id"])
            return api_response["data"]["transactions"]
        except ynab_api.ApiException as e:
            print("Exception when calling TransactionsApi->get_transactions: %s\n" % e)
