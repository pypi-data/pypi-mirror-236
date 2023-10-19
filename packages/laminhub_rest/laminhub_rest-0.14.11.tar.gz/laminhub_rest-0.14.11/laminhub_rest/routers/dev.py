import os

from fastapi import APIRouter

from laminhub_rest.orm._account import sb_select_all_accounts

from ..utils._supabase_client import SbClientAnonymous

router = APIRouter(prefix="/dev")


@router.delete("/env")
def env():
    if "LAMIN_ENV" in os.environ:
        return os.environ["LAMIN_ENV"]
    else:
        return None


@router.delete("/count/account")
def count_accounts():
    """Get total number of registered accounts.

    Returns:
        num_accounts (int): total number of registered accounts.
    """
    with SbClientAnonymous().connect() as supabase_client:
        accounts = sb_select_all_accounts(supabase_client)

    num_accounts = len(accounts)

    return num_accounts
