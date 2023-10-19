import pytest

# Test assets
from laminhub_rest.core.account import create_organization_account, delete_account
from laminhub_rest.orm._account import sb_select_account_by_handle
from laminhub_rest.utils._id import base62
from laminhub_rest.utils._supabase_client import SbClientAdmin, SbClientFromAccesToken

# Test utils
from laminhub_rest.utils._test import create_test_account, create_test_auth


def test_create_organization():
    pass  # this is tested under tests/account/.


def test_manage_members(test_client, hub_rest_api_url, user_account_1, user_account_2):
    auth_1, account_1 = user_account_1
    auth_2, account_2 = user_account_2

    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        org_handle_1 = f"lamin.ci.org.{base62(8)}"
        _ = create_organization_account(
            handle=org_handle_1, user_id=account_1["id"], supabase_client=client
        )
        org_account = sb_select_account_by_handle(
            handle=org_handle_1, supabase_client=client
        )

    # Test fetching of account's organizations
    response = test_client.get(
        f"{hub_rest_api_url}/account/resources/organizations/{account_1['handle']}",
        headers={"authentication": f"Bearer {auth_1['access_token']}"},
    ).json()
    assert len(response) == 1
    assert response[0]["account"]["handle"] == org_handle_1

    # Test addition of a member
    response = test_client.post(
        f"{hub_rest_api_url}/organization/resources/members/{org_account['id']}/?user_id={account_2['id']}",  # noqa
        headers={"authentication": f"Bearer {auth_1['access_token']}"},
    ).json()
    assert response == "success"

    # Test updated of a member
    response = test_client.put(
        f"{hub_rest_api_url}/organization/resources/members/{org_account['id']}/?user_id={account_2['id']}&role=owner",  # noqa
        headers={"authentication": f"Bearer {auth_1['access_token']}"},
    ).json()
    assert response == "success"

    # Test removal of a member
    response = test_client.delete(
        f"{hub_rest_api_url}/organization/resources/members/{org_account['id']}/?user_id={account_2['id']}",  # noqa
        headers={"authentication": f"Bearer {auth_1['access_token']}"},
    ).json()
    assert response == "success"

    # Clean up test assets
    # RLS policies not yet implemented for org deletion by owners
    with SbClientAdmin().connect() as client:
        delete_account(org_account["handle"], client)


def test_rls(test_client, hub_rest_api_url, user_account_1, user_account_2):
    auth_1, account_1 = user_account_1
    auth_2, account_2 = user_account_2
    auth_3 = create_test_auth()
    account_3 = create_test_account(
        handle=auth_3["handle"], access_token=auth_3["access_token"]
    )
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        org_handle_1 = f"lamin.ci.org.{base62(8)}"
        _ = create_organization_account(
            handle=org_handle_1, user_id=account_1["id"], supabase_client=client
        )
        org_account = sb_select_account_by_handle(
            handle=org_handle_1, supabase_client=client
        )

    # Enable member to select other member
    # Add a member to the organization
    _ = test_client.post(
        f"{hub_rest_api_url}/organization/resources/members/{org_account['id']}/?user_id={account_2['id']}",  # noqa
        headers={"authentication": f"Bearer {auth_1['access_token']}"},
    )
    # Member should be able to select all members of the organization.
    response = test_client.get(
        f"{hub_rest_api_url}/organization/resources/members/{org_account['id']}",
        headers={"authentication": f"Bearer {auth_2['access_token']}"},
    ).json()
    assert len(response) == 2

    # Enable owners to add members
    # Non-owner member should not be able to add other members
    with pytest.raises(Exception) as error:
        response = test_client.post(
            f"{hub_rest_api_url}/organization/resources/members/{org_account['id']}/?user_id={account_3['id']}",  # noqa
            headers={"authentication": f"Bearer {auth_2['access_token']}"},
        ).json()
        assert "new row violates row-level security policy" in error.value.message

    # Enable owners to update members
    # Non-owner member should not be able to update other members
    response = test_client.put(
        f"{hub_rest_api_url}/organization/resources/members/{org_account['id']}/?user_id={account_1['id']}&role=member",  # noqa
        headers={"authentication": f"Bearer {auth_2['access_token']}"},
    ).json()
    assert response == "member-not-updated"

    # Enable owners to delete members
    # Non-owner member should not be able to delete other members
    response = test_client.delete(
        f"{hub_rest_api_url}/organization/resources/members/{org_account['id']}/?user_id={account_1['id']}",  # noqa
        headers={"authentication": f"Bearer {auth_2['access_token']}"},
    ).json()
    assert response == "member-not-deleted"

    # Clean up tests assets
    with SbClientFromAccesToken(auth_3["access_token"]).connect() as client:
        delete_account(account_3["handle"], client)
    # RLS policies not yet implemented for org deletion by owners
    with SbClientAdmin().connect() as client:
        delete_account(org_account["handle"], client)
