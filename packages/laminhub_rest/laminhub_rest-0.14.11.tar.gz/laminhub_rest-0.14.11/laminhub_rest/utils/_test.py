import os
import uuid
from typing import Union

import requests  # type: ignore

from laminhub_rest.connector import connect_hub_with_auth
from laminhub_rest.orm._account import sb_insert_account
from laminhub_rest.orm._account_instance import sb_insert_collaborator
from laminhub_rest.orm._instance import sb_insert_instance
from laminhub_rest.orm._storage import sb_insert_storage
from laminhub_rest.utils._access_token import extract_id
from laminhub_rest.utils._id import base62
from laminhub_rest.utils._supabase_client import SbClientAdmin, SbClientAnonymous


def get_lamin_site_base_url():
    if "LAMIN_ENV" in os.environ:
        if os.environ["LAMIN_ENV"] == "local":
            return "http://localhost:3000/"
        elif os.environ["LAMIN_ENV"] == "staging-test":
            return "https://laminapp-ui-staging-hst.vercel.app/"
        elif os.environ["LAMIN_ENV"] == "staging":
            return "https://laminapp-ui-staging-hs.vercel.app/"
        elif os.environ["LAMIN_ENV"] == "prod-test":
            return "https://laminapp-ui-staging-hpt.vercel.app/"
        elif os.environ["LAMIN_ENV"] == "prod":
            return "https://lamin.ai/"


def create_test_auth():
    handle = f"lamin.ci.user.{base62(6)}"
    email = f"{handle}@gmail.com"
    password = "password"

    if "LAMIN_ENV" in os.environ and os.environ["LAMIN_ENV"] != "local":
        # Service role key is needed here as generate_link require admin privileges
        with SbClientAdmin().connect() as client:
            generate_link_response = client.auth.admin.generate_link(
                {
                    "type": "signup",
                    "email": email,
                    "password": password,
                    "options": {
                        "redirect_to": get_lamin_site_base_url(),
                    },
                }
            )
            action_link = generate_link_response.properties.action_link
            try:
                requests.get(action_link)
            except Exception as e:  # noqa
                raise e
            auth_response = client.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
            )
    else:
        with SbClientAnonymous().connect() as client:
            auth_response = client.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                }
            )

    return {
        "handle": handle,
        "email": email,
        "password": password,
        "id": str(auth_response.session.user.id),
        "access_token": auth_response.session.access_token,
        "session": auth_response.session,
    }


def create_test_account(
    handle: str,
    access_token: str,
    organization: Union[bool, None] = False,
):
    hub = connect_hub_with_auth(access_token=access_token)

    account_id = extract_id(access_token)

    account = sb_insert_account(
        {
            "id": account_id,
            "lnid": base62(8),
            "handle": handle,
            "user_id": None if organization else account_id,
        },
        hub,
    )

    hub.auth.sign_out()

    return account


def create_test_instance(storage_id: str, access_token: str):
    hub = connect_hub_with_auth(access_token=access_token)

    account_id = extract_id(access_token)

    name = f"lamin.ci.instance.{base62(6)}"

    instance = sb_insert_instance(
        {
            "id": uuid.uuid4().hex,
            "account_id": account_id,
            "name": name,
            "storage_id": storage_id,
            "public": True,
        },
        hub,
    )

    hub.auth.sign_out()

    return instance


def create_test_storage(access_token: str):
    hub = connect_hub_with_auth(access_token=access_token)

    root = f"lamin.ci.storage.{base62(6)}"
    account_id = extract_id(access_token)

    storage = sb_insert_storage(
        {
            "id": uuid.uuid4().hex,
            "lnid": base62(8),
            "created_by": account_id,
            "root": root,
            "region": "us-east-1",
            "type": "s3",
        },
        hub,
    )

    hub.auth.sign_out()

    return storage


def add_test_collaborator(
    instance_id: str,
    account_id: str,
    role: str,
    access_token: str,
):
    hub = connect_hub_with_auth(access_token=access_token)

    collaborator = sb_insert_collaborator(
        {
            "instance_id": instance_id,
            "account_id": account_id,
            "role": role,
        },
        hub,
    )

    hub.auth.sign_out()

    return collaborator
