from dotenv import load_dotenv
import os
import ynab_api

load_dotenv()

ynab_api_host = "https://api.youneedabudget.com/v1"
api_key = os.getenv("YNAB_API_KEY")
budget_id = os.getenv("YNAB_BUDGET_ID")


def ynab_config():
    YNAB_CONFIG = {
        "ynab_api": ynab_api_host,
        "api_key": api_key,
        "budget_id": budget_id,
    }
    return YNAB_CONFIG


def get_ynab_config():
    """Handles YNAB connection and returns the cli

    Returns:
        ynab_api: client ready to query the API
    """
    config = ynab_config()
    configuration = ynab_api.Configuration(host=ynab_api_host)
    configuration.api_key["bearer"] = api_key
    configuration.api_key_prefix["bearer"] = "Bearer"
    return configuration, config
