from deepdiff import DeepDiff
from faker import Faker

from laminhub_rest.core.account import delete_account
from laminhub_rest.core.instance import delete_instance
from laminhub_rest.orm._account import sb_select_account_by_handle
from laminhub_rest.orm._organization_user import sb_select_member
from laminhub_rest.orm._storage import sb_delete_storage
from laminhub_rest.routers.account import (
    get_account_instances,
    get_account_instances_with_role,
)
from laminhub_rest.utils._id import base62
from laminhub_rest.utils._supabase_client import SbClientAdmin, SbClientFromAccesToken
from laminhub_rest.utils._test import (
    add_test_collaborator,
    create_test_auth,
    create_test_instance,
    create_test_storage,
)

FAKE = Faker()


def test_create_user_account(test_client, hub_rest_api_url):
    auth = create_test_auth()
    response = test_client.post(
        f"{hub_rest_api_url}/account/?handle={auth['handle']}&organization={False}",
        headers={"authentication": f"Bearer {auth['access_token']}"},
    )
    assert response.json() == "success"
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        account = sb_select_account_by_handle(auth["handle"], client)
        assert account["id"] == auth["id"]
        delete_account(auth["handle"], client)
    with SbClientAdmin().connect() as client:
        client.auth.admin.delete_user(auth["id"])


def test_create_organization_account(test_client, hub_rest_api_url, user_account_1):
    auth_1, _ = user_account_1
    org_handle = "org.handle." + base62(6)
    response = test_client.post(
        f"{hub_rest_api_url}/account/?handle={org_handle}&organization={True}",
        headers={"authentication": f"Bearer {auth_1['access_token']}"},
    )
    assert response.json() == "success"
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        org_account = sb_select_account_by_handle(org_handle, client)
        assert org_account["user_id"] is None
        assert org_account["handle"] == org_handle
        member = sb_select_member(org_account["id"], auth_1["id"], client)
        assert member["role"] == "owner"
    # RLS policies not yet implemented for org deletion by owners
    with SbClientAdmin().connect() as client:
        delete_account(org_handle, client)
        del_org_account = sb_select_account_by_handle(org_handle, client)
        assert del_org_account is None
        del_member = sb_select_member(org_account["id"], auth_1["id"], client)
        assert del_member is None


def test_update_user_account(test_client, hub_rest_api_url, user_account_for_update):
    auth, _ = user_account_for_update
    new_name = FAKE.name()
    response = test_client.put(
        f"{hub_rest_api_url}/account/?name={new_name}",
        headers={"authentication": f"Bearer {auth['access_token']}"},
    )
    assert response.json() == "success"
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        account = sb_select_account_by_handle(auth["handle"], client)
        assert account["name"] == new_name


def test_get_account_by_id(test_client, hub_rest_api_url, user_account_1):
    _, account = user_account_1
    response = test_client.get(f"{hub_rest_api_url}/account/{account['id']}")
    assert str(response.json()) == str(account)


def test_get_account_by_handle(test_client, hub_rest_api_url, user_account_1):
    _, account = user_account_1
    response = test_client.get(f"{hub_rest_api_url}/account/handle/{account['handle']}")
    assert str(response.json()) == str(account)


def test_get_account_instances(test_client, hub_rest_api_url, user_account_1):
    auth, account = user_account_1
    # Create storage
    storage = create_test_storage(access_token=auth["access_token"])

    # Create instance
    instance = create_test_instance(
        storage_id=storage["id"], access_token=auth["access_token"]
    )

    # Add account as an admin member
    _ = add_test_collaborator(
        instance_id=instance["id"],
        account_id=account["id"],
        role="admin",
        access_token=auth["access_token"],
    )

    # Fetch account's instances
    account_instances_expected = [
        {
            **instance,
            "storage": {"root": storage["root"]},
            "account": {"handle": account["handle"], "id": account["id"]},
        }
    ]

    # call get_account_instances
    instances = get_account_instances(
        account["handle"], False, f"Bearer {auth['access_token']}"
    )
    assert DeepDiff(instances, account_instances_expected, ignore_order=True) == {}

    # get method on /account/{id} route
    response = test_client.get(
        f"{hub_rest_api_url}/account/resources/instances/{account['handle']}",
        headers={"authentication": f"Bearer {auth['access_token']}"},
    )
    assert str(response.json()) == str(account_instances_expected)

    # Clean up test assets
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        delete_instance(
            owner=account["handle"], name=instance["name"], supabase_client=client
        )
        sb_delete_storage(storage["id"], client)


def test_get_account_instances_with_role(test_client, hub_rest_api_url, user_account_1):
    auth, account = user_account_1
    # Create storage
    storage = create_test_storage(access_token=auth["access_token"])

    # Create instance
    instance = create_test_instance(
        storage_id=storage["id"], access_token=auth["access_token"]
    )

    # Add account as an admin member
    _ = add_test_collaborator(
        instance_id=instance["id"],
        account_id=account["id"],
        role="admin",
        access_token=auth["access_token"],
    )

    # Fetch account's instances
    account_instances_expected = [
        {
            "role": "admin",
            "instance": {
                **instance,
                "storage": {"root": storage["root"]},
                "account": {"handle": account["handle"], "id": account["id"]},
                "cloud_run_instance": None,
            },
        }
    ]

    # call get_account_instances
    instances = get_account_instances_with_role(
        account["handle"], f"Bearer {auth['access_token']}"
    )
    assert DeepDiff(instances, account_instances_expected, ignore_order=True) == {}

    # get method on /account/{id} route
    response = test_client.get(
        f"{hub_rest_api_url}/account/resources/instances-with-role/{account['handle']}",
        headers={"authentication": f"Bearer {auth['access_token']}"},
    )
    assert str(response.json()) == str(account_instances_expected)

    # Clean up test assets
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        delete_instance(
            owner=account["handle"], name=instance["name"], supabase_client=client
        )
        sb_delete_storage(storage["id"], client)
