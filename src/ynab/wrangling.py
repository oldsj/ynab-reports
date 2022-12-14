import calendar
from datetime import datetime

import pandas as pd

from ynab.api import get_all_transactions_json
from ynab.config import get_ynab_config
from ynab.data_tools import cartesian_multiple, cartesian_pair

from functools import lru_cache


@lru_cache(maxsize=0)
def get_ynab_dataset(min_date=None, max_date=None):
    configuration, ynab_conf = get_ynab_config()
    categories_to_exclude = ynab_conf.get("categories_to_exclude", [])
    if type(ynab_conf["budget_id"]) is list:
        budget_names = ynab_conf["budget_id"]
        rates = ynab_conf["currency_rate"]
        assert len(budget_names) == len(rates)
        df = []
        for name, rate in zip(budget_names, rates):
            data = get_all_transactions_json(name)
            df.append(pd.DataFrame(data).assign(amount=lambda d: d.amount * rate))
        df = pd.concat(df, axis=0)
    else:
        data = get_all_transactions_json(ynab_conf["budget_id"])
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


def calculate_daily_balances(df):
    """Calculate daily balances from the YNAB dataset, by cumulative summing the
    daily inflows and outflows, at account, category and date level.

    Args:
        df (pd.DataFrame): YNAB data frame with all the transactions.

    Returns:
        pd.DataFrame: data frame with the daily balances at account and category
        level.
    """
    pks = ["account_name", "category_name"]
    # Extend it until end of month
    max_date = df.date.max()
    eom_day = calendar.monthrange(max_date.year, max_date.month)[1]
    eom_date = datetime(max_date.year, max_date.month, eom_day)
    df_date = pd.DataFrame({"date": pd.date_range(df.date.min(), eom_date)})
    df_pks = cartesian_multiple(df[pks], pks)
    df_base = cartesian_pair(df_date, df_pks)
    df = df_base.merge(df[pks + ["date", "amount"]], how="left").fillna(0)
    # Aggregate at the right level to remove duplicated transactions
    df = df.groupby(pks + ["date"]).amount.sum().reset_index()
    df = df.sort_values(by="date")
    df = df.assign(
        amount=lambda d: d.groupby(pks).amount.transform(lambda x: x.cumsum())
    )
    return df
