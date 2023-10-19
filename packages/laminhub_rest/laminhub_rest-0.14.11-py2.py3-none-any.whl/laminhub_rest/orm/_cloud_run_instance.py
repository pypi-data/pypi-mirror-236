from datetime import datetime

from supabase.client import Client

# SELECT


def sb_select_cloud_run_instance_by_lamin_instance_id(
    lamin_instance_id: str,
    supabase_client: Client,
):
    data = (
        supabase_client.table("cloud_run_instance")
        .select("*")
        .eq("lamin_instance_id", lamin_instance_id)
        .execute()
        .data
    )

    if len(data) == 0:
        return None
    return data[0]


def sb_select_cloud_run_instance_by_server_name(
    cloud_run_instance_name: str, supabase_client: Client
):
    data = (
        supabase_client.table("cloud_run_instance")
        .select("*")
        .eq("cloud_run_instance_name", cloud_run_instance_name)
        .execute()
        .data
    )

    if len(data) == 0:
        return None
    return data[0]


def sb_select_least_recently_used_generic_cloud_run_instance(supabase_client: Client):
    data = (
        supabase_client.table("cloud_run_instance")
        .select("*")
        .order("last_access_at")
        .like("cloud_run_instance_name", "generic-instance-%")
        .execute()
        .data
    )

    if len(data) == 0:
        return None
    return data[0]


# INSERT


def sb_insert_cloud_run_instance(
    cloud_run_instance_id: str, lamin_instance_id: str, supabase_client: Client
):
    data = (
        supabase_client.table("cloud_run_instance")
        .insert(
            {
                "id": cloud_run_instance_id,
                "lamin_instance_id": lamin_instance_id,
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now()),
                "last_access_at": str(datetime.now()),
            }
        )
        .execute()
        .data
    )

    if len(data) == 0:
        return None
    return data[0]


# UPDATE


def sb_update_cloud_run_instance(
    cloud_run_instance_id: str, lamin_instance_id: str, supabase_client: Client
):
    data = (
        supabase_client.table("cloud_run_instance")
        .update(
            {
                "lamin_instance_id": lamin_instance_id,
                "updated_at": str(datetime.now()),
                "last_access_at": str(datetime.now()),
            }
        )
        .eq("id", cloud_run_instance_id)
        .execute()
        .data
    )

    if len(data) == 0:
        return None
    return data[0]


def sb_update_last_access_at(cloud_run_instance_id: str, supabase_client: Client):
    data = (
        supabase_client.table("cloud_run_instance")
        .update(
            {
                "last_access_at": str(datetime.now()),
            }
        )
        .eq("id", cloud_run_instance_id)
        .execute()
        .data
    )

    if len(data) == 0:
        return None
    return data[0]
