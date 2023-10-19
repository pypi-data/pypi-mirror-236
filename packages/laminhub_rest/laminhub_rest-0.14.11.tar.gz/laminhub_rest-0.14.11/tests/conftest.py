import os
from pathlib import Path
from subprocess import DEVNULL, getoutput, run

import pytest
from lamindb_setup import login

from laminhub_rest.core.account import (
    create_organization_account,
    create_user_account,
    delete_account,
)
from laminhub_rest.orm._account import sb_select_account_by_handle
from laminhub_rest.utils._id import base62
from laminhub_rest.utils._supabase_client import SbClientAdmin, SbClientFromAccesToken
from laminhub_rest.utils._test import create_test_auth


# this function is duplicated across laminhub-rest and lamindb-setup
def create_and_set_local_supabase_env():
    start_supabase = """supabase start -x realtime,storage-api,imgproxy,pgadmin-schema-diff,migra,postgres-meta,studio,edge-runtime,logflare,vector,pgbouncer"""  # noqa
    # unfortunately, supabase status -o env does not work with
    # a reduced number of containers (running supabase CLI version 1.38.6 & 1.96.4)
    # hence, we need this ugly regex
    get_keys = """grep -e 'anon key' -e 'service_role key' | cut -f2 -d ":" | sed -e 's/^[[:space:]]*//'"""  # noqa
    keys = getoutput(f"{start_supabase}|{get_keys}").split("\n")
    if (
        len(keys) > 1
    ):  # output from 2nd call to supabase start is different (see note in line 41)
        anon_key = keys[-2]
        service_role_key = keys[-1]
        env = {
            "POSTGRES_DSN": "postgresql://postgres:postgres@localhost:54322/postgres",
            "SUPABASE_API_URL": "http://localhost:54321",
            "SUPABASE_ANON_KEY": anon_key,
            "SUPABASE_SERVICE_ROLE_KEY": service_role_key,
        }
    else:
        env = {}
    # update environment variables with these values
    for key, value in env.items():
        # the following will not overwrite existing environment variables
        # the reason is that create_and_set_local_supabase_env seems to be called
        # multiple times; for any but the 1st time the supabase CLI is called,
        # we see a trivial output message and cannot parse the anon_key
        # (Alex doesn't understand why it's called several times and extensive
        #  debugging with logging didn't yield a conclusion)
        if key not in os.environ:
            os.environ[key] = value
        else:
            print(f"WARNING: env variable {key} is already set to {os.environ[key]}")


def pytest_configure():
    if os.environ["LAMIN_ENV"] == "local":
        create_and_set_local_supabase_env()
        import laminhub_rest

        run(
            "lnhub alembic upgrade head",
            shell=True,
            env=os.environ,
            cwd=Path(laminhub_rest.__file__).parent.parent,
            check=True,
        )


def pytest_unconfigure():
    if os.environ["LAMIN_ENV"] == "local":
        print(" tear down supabase")
        run("supabase stop", shell=True, stdout=DEVNULL)


@pytest.fixture(scope="session")
def test_client():
    if os.environ["LAMIN_ENV"] == "local":
        from laminhub_rest.main import client

        return client
    else:
        import requests  # type: ignore

        return requests


@pytest.fixture(scope="session")
def hub_rest_api_url():
    if os.environ["LAMIN_ENV"] == "local":
        return ""
    else:
        return os.environ["LAMIN_HUB_REST_SERVER_URL"]


@pytest.fixture(scope="session")
def user_account_1():
    auth = create_test_auth()
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = create_user_account(
            handle=auth["handle"],
            id=auth["id"],
            supabase_client=client,
        )
        assert message is None
        account = sb_select_account_by_handle(auth["handle"], client)
        # use this account as default client account (needed for init_instance)
        login(user=auth["email"], password=auth["password"])
    yield auth, account
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        delete_account(auth["handle"], client)
    with SbClientAdmin().connect() as client:
        client.auth.admin.delete_user(auth["id"])


@pytest.fixture(scope="session")
def user_account_2():
    auth = create_test_auth()
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = create_user_account(
            handle=auth["handle"],
            id=auth["id"],
            supabase_client=client,
        )
        assert message is None
        account = sb_select_account_by_handle(auth["handle"], client)
    yield auth, account
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        delete_account(auth["handle"], client)
    with SbClientAdmin().connect() as client:
        client.auth.admin.delete_user(auth["id"])


@pytest.fixture(scope="function")
def user_account_for_deletion():
    auth = create_test_auth()
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = create_user_account(
            handle=auth["handle"],
            id=auth["id"],
            supabase_client=client,
        )
        assert message is None
        account = sb_select_account_by_handle(auth["handle"], client)
    yield auth, account
    with SbClientAdmin().connect() as client:
        client.auth.admin.delete_user(auth["id"])


@pytest.fixture(scope="session")
def user_account_for_update():
    auth = create_test_auth()
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = create_user_account(
            handle=auth["handle"],
            id=auth["id"],
            supabase_client=client,
        )
        assert message is None
        account = sb_select_account_by_handle(auth["handle"], client)
    yield auth, account
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        delete_account(auth["handle"], client)
    with SbClientAdmin().connect() as client:
        client.auth.admin.delete_user(auth["id"])


@pytest.fixture(scope="function")
def org_account_for_deletion(user_account_1):
    auth_1, _ = user_account_1
    org_handle = "org.handle." + base62(6)
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        message = create_organization_account(
            handle=org_handle,
            user_id=auth_1["id"],
            supabase_client=client,
        )
        assert message is None
        org_account = sb_select_account_by_handle(org_handle, client)
        yield auth_1, org_account


@pytest.fixture(scope="session")
def user_account_for_vault():
    auth = create_test_auth()
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = create_user_account(
            handle=auth["handle"],
            id=auth["id"],
            supabase_client=client,
        )
        assert message is None
        account = sb_select_account_by_handle(auth["handle"], client)
    yield auth, account
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        delete_account(auth["handle"], client)
    with SbClientAdmin().connect() as client:
        client.auth.admin.delete_user(auth["id"])
