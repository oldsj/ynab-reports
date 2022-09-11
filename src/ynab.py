from ynab.reporting import get_top_flows
from pprint import pprint

df_in, df_out = get_top_flows(year=2022, month=8, n_rows=10)

print(df_in.to_html())
