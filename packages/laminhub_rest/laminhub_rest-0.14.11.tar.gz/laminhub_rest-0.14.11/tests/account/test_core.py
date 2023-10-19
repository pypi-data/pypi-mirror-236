import pytest
from faker import Faker
from postgrest.exceptions import APIError

from laminhub_rest.core.account import (
    create_organization_account,
    create_user_account,
    delete_account,
    update_account,
)
from laminhub_rest.orm._account import sb_select_account_by_handle
from laminhub_rest.orm._organization_user import sb_select_member
from laminhub_rest.utils._id import base62
from laminhub_rest.utils._supabase_client import (
    SbClientAdmin,
    SbClientAnonymous,
    SbClientFromAccesToken,
)
from laminhub_rest.utils._test import create_test_auth

FAKE = Faker()


def test_create_user_account():
    auth = create_test_auth()
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = create_user_account(
            handle=auth["handle"],
            id=auth["id"],
            supabase_client=client,
        )
        assert message is None
        account = sb_select_account_by_handle(auth["handle"], client)
        assert account is not None
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        delete_account(auth["handle"], client)
        account = sb_select_account_by_handle(auth["handle"], client)
        assert account is None
    with SbClientAdmin().connect() as client:
        client.auth.admin.delete_user(auth["id"])


def test_create_organization_account(user_account_1):
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
        assert org_account["handle"] == org_handle
        assert org_account["user_id"] is None
        member = sb_select_member(org_account["id"], auth_1["id"], client)
        assert member["role"] == "owner"
    # RLS policies not yet implemented for org deletion by owners
    with SbClientAdmin().connect() as client:
        delete_account(org_handle, client)
        del_org_account = sb_select_account_by_handle(org_handle, client)
        assert del_org_account is None
        del_member = sb_select_member(org_account["id"], auth_1["id"], client)
        assert del_member is None


def test_create_existing_user_account(user_account_1):
    auth, _ = user_account_1
    with pytest.raises(APIError) as error:
        with SbClientFromAccesToken(auth["access_token"]).connect() as client:
            create_user_account(
                handle=auth["handle"],
                id=auth["id"],
                supabase_client=client,
            )
        assert (
            'duplicate key value violates unique constraint "pk_account"'
            in error.exconly()
        )


def test_create_wrong_user_account():
    auth = create_test_auth()
    with pytest.raises(Exception) as error:
        with SbClientAnonymous().connect() as client:
            _ = create_user_account(
                handle=auth["handle"],
                id=auth["id"],
                supabase_client=client,
            )
        assert "new row violates row-level security policy" in error.value.message
    with SbClientAdmin().connect() as client:
        client.auth.admin.delete_user(auth["id"])


def test_update_account(user_account_for_update):
    auth, _ = user_account_for_update
    new_name = FAKE.name()
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = update_account(
            id=auth["id"],
            handle=auth["handle"],
            name=new_name,
            bio=None,
            github_handle=None,
            linkedin_handle=None,
            twitter_handle=None,
            website=None,
            supabase_client=client,
        )

        assert message is None

        account = sb_select_account_by_handle(auth["handle"], client)
        assert account["name"] == new_name


def test_update_nonexistent_account():
    auth = create_test_auth()
    name = FAKE.name()
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = update_account(
            id=auth["id"],
            handle=auth["handle"],
            name=name,
            bio=None,
            github_handle=None,
            linkedin_handle=None,
            twitter_handle=None,
            website=None,
            supabase_client=client,
        )
        assert message == "account-not-exists"


def test_update_wrong_account(user_account_1, user_account_2):
    auth_1, account_1 = user_account_1
    auth_2, _ = user_account_2
    new_name = FAKE.name()
    with pytest.raises(AssertionError):
        with SbClientFromAccesToken(auth_2["access_token"]).connect() as client:
            _ = update_account(
                id=account_1["id"],
                handle=account_1["handle"],  # this handle doesn't exist
                name=new_name,
                bio=None,
                github_handle=None,
                linkedin_handle=None,
                twitter_handle=None,
                website=None,
                supabase_client=client,
            )
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        account = sb_select_account_by_handle(account_1["handle"], client)
        assert account["name"] != new_name


def test_everyone_can_see_account(user_account_2, user_account_1):
    auth_1, _ = user_account_1
    _, account_2 = user_account_2
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        account = sb_select_account_by_handle(account_2["handle"], client)
        assert account


def test_delete_user_account(user_account_for_deletion):
    auth_del, _ = user_account_for_deletion
    with SbClientFromAccesToken(auth_del["access_token"]).connect() as client:
        _ = delete_account(handle=auth_del["handle"], supabase_client=client)
        account = sb_select_account_by_handle(
            handle=auth_del["handle"], supabase_client=client
        )
        assert account is None


def test_delete_wrong_user_account(user_account_for_deletion, user_account_1):
    auth_del, _ = user_account_for_deletion
    auth_1, _ = user_account_1
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        _ = delete_account(handle=auth_del["handle"], supabase_client=client)
        account = sb_select_account_by_handle(
            handle=auth_del["handle"], supabase_client=client
        )
        assert account is not None
    # we have to delete it properly as the fixture only takes care of
    # tearing up the user auth
    with SbClientFromAccesToken(auth_del["access_token"]).connect() as client:
        _ = delete_account(handle=auth_del["handle"], supabase_client=client)
        account = sb_select_account_by_handle(
            handle=auth_del["handle"], supabase_client=client
        )
        assert account is None


# Necessary RLS policies are not yet implemented
# def test_delete_org_account(org_account_for_deletion):
#     owner_auth, org_account = org_account_for_deletion
#     with SbClientFromAccesToken(owner_auth["access_token"]).connect() as client:
#         delete_account(org_account["handle"], client)
#         account = sb_select_account_by_handle(org_account["handle"], client)
#         assert account is None
#         member = sb_select_member(org_account["id"], owner_auth["id"], client)
#         assert member is None

# Necessary RLS policies are not yet implemented
# def test_delete_wrong_org_account(org_account_for_deletion, user_account_1):
#     owner_auth, org_account = org_account_for_deletion
#     auth_1, _ = user_account_1
#     with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
#         delete_account(org_account["handle"], client)
#     with SbClientFromAccesToken(owner_auth["access_token"]).connect() as client:
#         account = sb_select_account_by_handle(org_account["handle"], client)
#         assert account is not None
#         member = sb_select_member(org_account["id"], owner_auth["id"], client)
#         assert member is not None
#     # we have to delete it properly as the fixture does not tear up the account
#     with SbClientFromAccesToken(owner_auth["access_token"]).connect() as client:
#         delete_account(org_account["handle"], client)
