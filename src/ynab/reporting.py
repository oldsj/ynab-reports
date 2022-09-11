
from ynab.api import get_ynab_dataset


def get_top_flows(year, month, n_rows):
    df = get_ynab_dataset()
    df = df.loc[lambda d: (d.date.dt.month == month) & (d.date.dt.year <= year)]
    # Remove transfers and exclude categories
    df = df[df.transfer_transaction_id.isnull()]
    df = df[df.exclude == False]
    # Separate inflows and outflows
    df_in = df.loc[lambda d: d.amount >= 0]
    df_out = df.loc[lambda d: d.amount < 0]
    # Date format adjustment
    df_in["date"] = df_in.date.dt.strftime("%b-%d")
    df_out["date"] = df_out.date.dt.strftime("%b-%d")
    # Limit the length of the memo text
    df_in["memo"] = df_in["memo"].str.slice(0, 20)
    df_out["memo"] = df_out["memo"].str.slice(0, 20)
    # Define the original column names and the desired ones
    columns = ["date", "account_name", "amount", "memo"]
    fancy_colnames = ["Date", "Account", "Amount", "Memo"]
    # Select columns and sort by amount
    df_in = df_in[columns].sort_values(by="amount", ascending=False)
    df_out = df_out[columns].sort_values(by="amount", ascending=True)
    # Take the first N rows
    df_in = df_in.head(n_rows)
    df_out = df_out.head(n_rows)
    # Rename the columns
    df_in.columns = fancy_colnames
    df_out.columns = fancy_colnames
    return df_in, df_out
