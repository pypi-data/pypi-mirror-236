from uuid import uuid4

import pytest

from laminhub_rest.orm._storage import (
    sb_delete_storage,
    sb_insert_storage,
    sb_select_storage,
    sb_udpate_storage,
)
from laminhub_rest.utils._id import base62
from laminhub_rest.utils._supabase_client import (
    SbClientAnonymous,
    SbClientFromAccesToken,
)


def test_rls_storage(user_account_1, user_account_2):
    auth_1, account_1 = user_account_1
    auth_2, account_2 = user_account_2

    # Enable authenticated accounts to create storage
    # With an anonymous supabase client
    with SbClientAnonymous().connect() as client:
        with pytest.raises(Exception) as error:
            storage = sb_insert_storage(
                storage_fields={
                    "id": uuid4().hex,
                    "lnid": (base62(8),),
                    "created_by": account_1["id"],
                    "root": f"lamin.ci.storage.{base62(6)}",
                    "region": "us-east-1",
                    "type": "s3",
                },
                supabase_client=client,
            )

            assert "new row violates row-level security policy" in error.value.message

    # Using another account authentication
    with SbClientFromAccesToken(auth_2["access_token"]).connect() as client:
        with pytest.raises(Exception) as error:
            storage = sb_insert_storage(
                storage_fields={
                    "id": uuid4().hex,
                    "lnid": (base62(8),),
                    "created_by": account_1["id"],
                    "root": f"lamin.ci.storage.{base62(6)}",
                    "region": "us-east-1",
                    "type": "s3",
                },
                supabase_client=client,
            )

            assert "new row violates row-level security policy" in error.value.message

    # Using corresponding account authentication
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        storage = sb_insert_storage(
            storage_fields={
                "id": uuid4().hex,
                "lnid": (base62(8),),
                "created_by": account_1["id"],
                "root": f"lamin.ci.storage.{base62(6)}",
                "region": "us-east-1",
                "type": "s3",
            },
            supabase_client=client,
        )

        assert storage is not None

    # Enable everyone to select a storage
    with SbClientAnonymous().connect() as client:
        storage_res = sb_select_storage(id=storage["id"], supabase_client=client)
        assert storage_res is not None

    # Enable owner to update their storage
    # With an anonymous supabase client
    with SbClientAnonymous().connect() as client:
        storage_res = sb_udpate_storage(
            id=storage["id"],
            storage_fields={
                "region": "us-east-2",
            },
            supabase_client=client,
        )

        assert storage_res is None
        assert (
            sb_select_storage(id=storage["id"], supabase_client=client)["region"]
            == "us-east-1"  # noqa
        )

    # Using another account authentication
    with SbClientFromAccesToken(auth_2["access_token"]).connect() as client:
        storage_res = sb_udpate_storage(
            id=storage["id"],
            storage_fields={
                "region": "us-east-2",
            },
            supabase_client=client,
        )

        assert storage_res is None
        assert (
            sb_select_storage(id=storage["id"], supabase_client=client)["region"]
            == "us-east-1"  # noqa
        )

    # Using corresponding account authentication
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        storage_res = sb_udpate_storage(
            id=storage["id"],
            storage_fields={
                "region": "us-east-2",
            },
            supabase_client=client,
        )

        assert storage_res is not None
        assert (
            sb_select_storage(id=storage["id"], supabase_client=client)["region"]
            == "us-east-2"  # noqa
        )

    # Enable owner to delete their storage
    # With an anonymous supabase client
    with SbClientAnonymous().connect() as client:
        storage_res = sb_delete_storage(id=storage["id"], supabase_client=client)
        assert storage_res is None
        assert sb_select_storage(id=storage["id"], supabase_client=client) is not None

    # Using another account authentication
    with SbClientFromAccesToken(auth_2["access_token"]).connect() as client:
        storage_res = sb_delete_storage(id=storage["id"], supabase_client=client)
        assert storage_res is None
        assert sb_select_storage(id=storage["id"], supabase_client=client) is not None

    # Using corresponding account authentication
    with SbClientFromAccesToken(auth_1["access_token"]).connect() as client:
        storage_res = sb_delete_storage(id=storage["id"], supabase_client=client)
        assert storage_res is not None
        assert sb_select_storage(id=storage["id"], supabase_client=client) is None
