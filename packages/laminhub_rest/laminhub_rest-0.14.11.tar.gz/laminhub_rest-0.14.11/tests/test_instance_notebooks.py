import secrets
import string
from uuid import uuid4

import pytest
from deepdiff import DeepDiff
from lamindb_setup.dev._hub_core import init_instance

from laminhub_rest.core.account import delete_account
from laminhub_rest.core.instance import delete_instance, update_instance
from laminhub_rest.orm._account_instance import (
    sb_delete_collaborator,
    sb_insert_collaborator,
    sb_select_collaborator,
    sb_select_collaborators,
    sb_update_collaborator,
)
from laminhub_rest.orm._instance import (
    sb_delete_instance,
    sb_insert_instance,
    sb_select_instance,
    sb_select_instance_by_name,
    sb_update_instance,
)
from laminhub_rest.orm._storage import sb_delete_storage
from laminhub_rest.routers.instance import get_instance_accounts, get_instance_by_name
from laminhub_rest.utils._supabase_client import SbClientFromAccesToken
from laminhub_rest.utils._test import (
    add_test_collaborator,
    create_test_account,
    create_test_auth,
    create_test_instance,
    create_test_storage,
)


def base26(n_char: int):
    alphabet = string.ascii_lowercase
    return "".join(secrets.choice(alphabet) for i in range(n_char))


def test_update_instance(user_account_1, test_client, hub_rest_api_url):
    auth, account = user_account_1
    storage = create_test_storage(access_token=auth["access_token"])
    instance = create_test_instance(
        storage_id=storage["id"], access_token=auth["access_token"]
    )

    # add a collaborator
    response = test_client.post(
        f"{hub_rest_api_url}/instance/resources/accounts/?handle={account['handle']}&instance_owner_handle={account['handle']}&instance_name={instance['name']}&role=admin",  # noqa
        headers={"authentication": f"Bearer {auth['access_token']}"},
    ).json()
    assert response == "success"

    # update an instance (call update_instance)
    new_description_1 = "Description"
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = update_instance(
            instance_id=instance["id"],
            supabase_client=client,
            description=new_description_1,
        )
        assert message is None
        instance = sb_select_instance(instance["id"], client)
        assert instance["description"] == new_description_1

    # update an instance (put method on /instance route)
    new_description_2 = "Description 2"
    response = test_client.put(
        f"{hub_rest_api_url}/instance/?instance_id={instance['id']}&description={new_description_2}",  # noqa
        headers={"authentication": f"Bearer {auth['access_token']}"},
    )
    assert response.json() == "success"
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        instance = sb_select_instance(instance["id"], client)
        assert instance["description"] == new_description_2

    # update a non existing instance (call update_instance)
    non_existing_instance_id = instance["id"][:-5] + "1aa63"
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        message = update_instance(
            instance_id=non_existing_instance_id,
            supabase_client=client,
            description="Description",
        )
        assert message == "instance-not-updated"

    # update a non existing instance (put method on /instance route)
    response = test_client.put(
        f"{hub_rest_api_url}/instance/?instance_id={non_existing_instance_id}&description={new_description_2}",  # noqa
        headers={"authentication": f"Bearer {auth['access_token']}"},
    )
    assert response.json() == "instance-not-updated"

    # clean up test assets
    with SbClientFromAccesToken(auth["access_token"]).connect() as client:
        delete_instance(
            owner=account["handle"], name=instance["name"], supabase_client=client
        )
        sb_delete_storage(id=storage["id"], supabase_client=client)


def test_delete_instance(user_account_1, user_account_2, test_client, hub_rest_api_url):
    auth_1, account_1 = user_account_1
    auth_2, account_2 = user_account_2

    storage = create_test_storage(access_token=auth_1["access_token"])
    existing_storage_root = storage["root"]

    instance_name_1 = f"lamin.ci.instance.{base26(6)}"
    db_1 = f"postgresql://postgres:pwd@0.0.0.0:5432/{instance_name_1}"

    instance_name_2 = f"lamin.ci.instance.{base26(6)}"
    db_2 = f"postgresql://postgres:pwd@0.0.0.0:5432/{instance_name_2}"

    # Init instance 1 and add a collaborator
    init_instance(
        name=instance_name_1,
        storage=existing_storage_root,
        db=db_1,
    )
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        instance_1 = sb_select_instance_by_name(
            account_id=account_1["id"], name=instance_name_1, supabase_client=client
        )
    _ = add_test_collaborator(
        instance_id=instance_1["id"],
        account_id=account_2["id"],
        role="admin",
        access_token=auth_1["access_token"],
    )

    # Init instance 2
    init_instance(
        name=instance_name_2,
        storage=existing_storage_root,
        db=db_2,
    )

    # Delete and instance
    # test cascade delete
    with SbClientFromAccesToken(auth_2["access_token"]).connect() as client:
        sb_delete_instance(instance_1["id"], client)

    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        instance = sb_select_instance(instance_1["id"], client)
        assert instance is None

        collaborators = sb_select_collaborators(instance_1["id"], client)
        assert collaborators is None

    # restore instance
    init_instance(
        name=instance_name_1,
        storage=existing_storage_root,
        db=db_1,
    )
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        instance_1 = sb_select_instance_by_name(
            account_id=account_1["id"], name=instance_name_1, supabase_client=client
        )
    _ = add_test_collaborator(
        instance_id=instance_1["id"],
        account_id=account_2["id"],
        role="admin",
        access_token=auth_1["access_token"],
    )

    # call delete_instance
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        delete_instance(
            owner=account_1["handle"], name=instance_name_1, supabase_client=client
        )
        instance = sb_select_instance(instance_1["id"], client)
        assert instance is None

    # check that all collaborators were successfully added
    instance_accounts = get_instance_accounts(
        account_1["handle"], instance_name_1, f"Bearer {auth_1['access_token']}"
    )
    assert instance_accounts["accounts"] is None

    # delete method on /instance route
    response = test_client.delete(
        f"{hub_rest_api_url}/instance/?account_handle={account_1['handle']}&name={instance_name_2}",  # noqa
        headers={"authentication": f"Bearer {auth_1['access_token']}"},
    )
    assert response.json() == "success"
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        instance = sb_select_instance_by_name(
            account_id=account_1["id"], name=instance_name_2, supabase_client=client
        )
        assert instance is None

    # delete a non existing instance
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        message = delete_instance(
            owner=account_1["handle"], name=instance_name_1, supabase_client=client
        )
        assert message == "instance-not-reachable"

    # clean up test assets
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        sb_delete_storage(storage["id"], client)


def test_fetch_instance(user_account_1, user_account_2, test_client, hub_rest_api_url):
    auth_1, account_1 = user_account_1
    auth_2, account_2 = user_account_2

    storage = create_test_storage(access_token=auth_1["access_token"])
    instance = create_test_instance(
        storage_id=storage["id"], access_token=auth_1["access_token"]
    )

    # Add account 1 as an admin member
    instance_collaborator_1 = add_test_collaborator(
        instance_id=instance["id"],
        account_id=account_1["id"],
        role="admin",
        access_token=auth_1["access_token"],
    )

    # Add account 2 as a member with read role
    instance_collaborator_2 = add_test_collaborator(
        instance_id=instance["id"],
        account_id=account_2["id"],
        role="read",
        access_token=auth_1["access_token"],
    )

    # Fetch instance by name
    instance_expected = {
        "instance": {
            **instance,
            "storage": {"root": storage["root"]},
            "account": {"handle": account_1["handle"], "id": account_1["id"]},
        },
        "role": "admin",
    }

    # Call get_instance_by_name
    instance_response = get_instance_by_name(
        account_1["handle"], instance["name"], f"Bearer {auth_1['access_token']}"
    )
    assert str(instance_response) == str(instance_expected)

    # Get method on /instance/{handle}/{name} route
    response = test_client.get(
        f"{hub_rest_api_url}/instance/{account_1['handle']}/{instance['name']}",
        headers={"authentication": f"Bearer {auth_1['access_token']}"},
    )
    assert str(response.json()) == str(instance_expected)

    # Fetch instance's account
    instance_accounts_expected = {
        "accounts": [
            {
                **instance_collaborator_1,
                "account": account_1,
            },
            {
                **instance_collaborator_2,
                "account": account_2,
            },
        ],
        "role": "admin",
    }

    # call get_instance_accounts
    instance_accounts = get_instance_accounts(
        account_1["handle"], instance["name"], f"Bearer {auth_1['access_token']}"
    )
    assert (
        DeepDiff(instance_accounts, instance_accounts_expected, ignore_order=True) == {}
    )

    # Get method on /instance/resources/accounts/{handle}/{name} route
    response = test_client.get(
        f"{hub_rest_api_url}/instance/resources/accounts/{account_1['handle']}/{instance['name']}",  # noqa
        headers={"authentication": f"Bearer {auth_1['access_token']}"},
    )
    assert str(response.json()) == str(instance_accounts_expected)

    # Clean up test assets
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        delete_instance(
            owner=account_1["handle"], name=instance["name"], supabase_client=client
        )
        sb_delete_storage(storage["id"], client)


def test_rls_instance(user_account_1, user_account_2, test_client, hub_rest_api_url):
    auth_1, account_1 = user_account_1
    auth_2, account_2 = user_account_2
    auth_3 = create_test_auth()
    account_3 = create_test_account(
        handle=auth_3["handle"], access_token=auth_3["access_token"]
    )
    auth_4 = create_test_auth()
    account_4 = create_test_account(
        handle=auth_4["handle"], access_token=auth_4["access_token"]
    )

    storage = create_test_storage(access_token=auth_1["access_token"])

    # Enable authenticated accounts to create instance
    instance_1_name = f"lamin.ci.instance.{base26(6)}"
    instance_1_id = uuid4().hex
    db = f"postgresql://postgres:pwd@0.0.0.0:5432/{instance_1_name}"

    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        instance_1 = sb_insert_instance(
            instance_fields={
                "id": instance_1_id,
                "account_id": account_1["id"],
                "name": instance_1_name,
                "storage_id": storage["id"],
                "db": db,
                "public": True,
            },
            supabase_client=client,
        )
        assert instance_1 is not None

    # Enable owner to add collaborators
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        sb_insert_collaborator(
            account_instance_fields={
                "account_id": account_1["id"],
                "instance_id": instance_1["id"],
                "role": "admin",
            },
            supabase_client=client,
        )

        assert (
            sb_select_collaborator(
                instance_id=instance_1["id"],
                account_id=account_1["id"],
                supabase_client=client,
            )
            is not None
        )

    # Enable admin accounts to add collaborators
    # An admin can add a collaborator as an admin.
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        sb_insert_collaborator(
            account_instance_fields={
                "account_id": account_2["id"],
                "instance_id": instance_1["id"],
                "role": "admin",
            },
            supabase_client=client,
        )

        assert (
            sb_select_collaborator(
                instance_id=instance_1["id"],
                account_id=account_2["id"],
                supabase_client=client,
            )
            is not None
        )

    # An admin can add a collaborator with a read role.
    with SbClientFromAccesToken(auth_2["access_token"]).connect() as client:
        sb_insert_collaborator(
            account_instance_fields={
                "account_id": account_3["id"],
                "instance_id": instance_1["id"],
                "role": "read",
            },
            supabase_client=client,
        )

        assert (
            sb_select_collaborator(
                instance_id=instance_1["id"],
                account_id=account_3["id"],
                supabase_client=client,
            )
            is not None
        )

    # A collaborator with a read role can't add a collaborator.
    with SbClientFromAccesToken(auth_3["access_token"]).connect() as client:
        with pytest.raises(Exception) as error:
            sb_insert_collaborator(
                account_instance_fields={
                    "account_id": account_4["id"],
                    "instance_id": instance_1["id"],
                    "role": "read",
                },
                supabase_client=client,
            )

        assert "new row violates row-level security policy" in error.value.message

    # A non collaborator can't add a collaborator.
    with SbClientFromAccesToken(auth_4["access_token"]).connect() as client:
        with pytest.raises(Exception) as error:
            sb_insert_collaborator(
                account_instance_fields={
                    "account_id": account_4["id"],
                    "instance_id": instance_1["id"],
                    "role": "read",
                },
                supabase_client=client,
            )

        assert "new row violates row-level security policy" in error.value.message

    # Enable admin to updated collaborators
    # An admin can update a collaborator
    with SbClientFromAccesToken(auth_2["access_token"]).connect() as client:
        sb_update_collaborator(
            account_id=account_3["id"],
            instance_id=instance_1["id"],
            role="write",
            supabase_client=client,
        )

        assert (
            sb_select_collaborator(
                account_id=account_3["id"],
                instance_id=instance_1["id"],
                supabase_client=client,
            )["role"]
            == "write"  # noqa
        )

    # A member with a non admin role can't update a collaborator.
    with SbClientFromAccesToken(auth_3["access_token"]).connect() as client:
        sb_update_collaborator(
            account_id=account_2["id"],
            instance_id=instance_1["id"],
            role="write",
            supabase_client=client,
        )

        assert (
            sb_select_collaborator(
                account_id=account_2["id"],
                instance_id=instance_1["id"],
                supabase_client=client,
            )["role"]
            == "admin"  # noqa
        )

    # Enable admin to delete collaborators
    # Non admin cannot delete collaborator
    with SbClientFromAccesToken(auth_3["access_token"]).connect() as client:
        sb_delete_collaborator(
            account_id=account_2["id"],
            instance_id=instance_1["id"],
            supabase_client=client,
        )
        collaborator = sb_select_collaborator(
            account_id=account_2["id"],
            instance_id=instance_1["id"],
            supabase_client=client,
        )
        assert collaborator is not None

    # Admin can delete collaborator
    with SbClientFromAccesToken(auth_2["access_token"]).connect() as client:
        sb_delete_collaborator(
            account_id=account_3["id"],
            instance_id=instance_1["id"],
            supabase_client=client,
        )
        collaborator = sb_select_collaborator(
            account_id=account_3["id"],
            instance_id=instance_1["id"],
            supabase_client=client,
        )
        assert collaborator is None

    # Enable owner to delete collaborators (even if he is not part of account_instance table)  # noqa
    instance_2_name = f"lamin.ci.instance.{base26(6)}"
    instance_2_id = uuid4().hex
    db = f"postgresql://postgres:pwd@0.0.0.0:5432/{instance_2_name}"
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        instance_2 = sb_insert_instance(
            instance_fields={
                "id": instance_2_id,
                "account_id": account_1["id"],
                "name": instance_2_name,
                "storage_id": storage["id"],
                "db": db,
                "public": True,
            },
            supabase_client=client,
        )

        assert (
            sb_insert_collaborator(
                account_instance_fields={
                    "account_id": account_2["id"],
                    "instance_id": instance_2["id"],
                    "role": "admin",
                },
                supabase_client=client,
            )
            is not None
        )

        sb_delete_collaborator(
            account_id=account_2["id"],
            instance_id=instance_2["id"],
            supabase_client=client,
        )

        assert (
            sb_select_collaborator(
                account_id=account_2["id"],
                instance_id=instance_2["id"],
                supabase_client=client,
            )
            is None
        )

    # Enable everyone to select public instances
    with SbClientFromAccesToken(auth_4["access_token"]).connect() as client:
        instance_response = sb_select_instance(
            id=instance_1["id"], supabase_client=client
        )
        assert instance_response is not None

    # Enable members to select their instances
    instance_private_name = f"lamin.ci.instance.{base26(6)}"
    instance_private_id = uuid4().hex
    db = f"postgresql://postgres:pwd@0.0.0.0:5432/{instance_private_name}"
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        private_instance = sb_insert_instance(
            instance_fields={
                "id": instance_private_id,
                "account_id": account_1["id"],
                "name": instance_private_name,
                "storage_id": storage["id"],
                "db": db,
                "public": False,
            },
            supabase_client=client,
        )

        sb_insert_collaborator(
            account_instance_fields={
                "account_id": account_1["id"],
                "instance_id": private_instance["id"],
                "role": "read",
            },
            supabase_client=client,
        )

        assert (
            sb_select_instance(id=private_instance["id"], supabase_client=client)
            is not None
        )
    with SbClientFromAccesToken(auth_3["access_token"]).connect() as client:
        assert (
            sb_select_instance(id=private_instance["id"], supabase_client=client)
            is None
        )

    # Enable admin accounts to update their instances
    # Non admin accounts cannot update
    with SbClientFromAccesToken(auth_3["access_token"]).connect() as client:
        sb_update_instance(
            instance_id=instance_1["id"],
            instance_fields={"description": "Description"},
            supabase_client=client,
        )

        assert (
            sb_select_instance(id=instance_1["id"], supabase_client=client)[
                "description"
            ]
            is None
        )

    # Admin accounts can update
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        sb_insert_collaborator(
            account_instance_fields={
                "account_id": account_3["id"],
                "instance_id": instance_1["id"],
                "role": "admin",
            },
            supabase_client=client,
        )

    with SbClientFromAccesToken(auth_3["access_token"]).connect() as client:
        sb_update_instance(
            instance_id=instance_1["id"],
            instance_fields={"description": "Description"},
            supabase_client=client,
        )

        assert (
            sb_select_instance(id=instance_1["id"], supabase_client=client)[
                "description"
            ]
            == "Description"  # noqa
        )

    # Enable owners to select their instances
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        # Delete all collaborators of the private instance
        (
            client.table("account_instance")
            .delete()
            .eq("instance_id", private_instance["id"])
            .execute()
        )
        (
            client.table("account_instance")
            .select("*")
            .eq("instance_id", private_instance["id"])
            .execute()
        )
        # Ensure owner can still select it
        assert (
            sb_select_instance(id=private_instance["id"], supabase_client=client)
            is not None
        )

    # Enable owners to delete their instances
    with SbClientFromAccesToken(auth_2["access_token"]).connect() as client:
        sb_delete_instance(id=private_instance["id"], supabase_client=client)

    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        assert (
            sb_select_instance(id=private_instance["id"], supabase_client=client)
            is not None
        )

        sb_delete_instance(id=private_instance["id"], supabase_client=client)

        assert (
            sb_select_instance(id=private_instance["id"], supabase_client=client)
            is None
        )

    # Clean up test assets
    with SbClientFromAccesToken(auth_3["access_token"]).connect() as client:
        delete_account(account_3["handle"], client)
    with SbClientFromAccesToken(auth_4["access_token"]).connect() as client:
        delete_account(account_4["handle"], client)
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        delete_instance(
            owner=account_1["handle"], name=instance_1["name"], supabase_client=client
        )
        delete_instance(
            owner=account_1["handle"], name=instance_2["name"], supabase_client=client
        )
        delete_instance(
            owner=account_1["handle"],
            name=private_instance["name"],
            supabase_client=client,
        )
        sb_delete_storage(storage["id"], client)
