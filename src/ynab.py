import json
from pprint import pprint
from ynab.config import get_ynab_config
import ynab_api
from ynab_api.api import months_api
from ynab_api.model.month_summaries_response import MonthSummariesResponse
from ynab_api.model.error_response import ErrorResponse


api_config, config = get_ynab_config()

with ynab_api.ApiClient(api_config) as api_client:
    api_instance = months_api.MonthsApi(api_client)
    budget_id = config[
        "budget_id"
    ]  
    try:
        # List budget months
        api_response = api_instance.get_budget_months(budget_id)
        pprint(api_response)
    except ynab_api.ApiException as e:
        print("Exception when calling MonthsApi->get_budget_months: %s\n" % e)
