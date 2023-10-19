from typing import Union

from fastapi import APIRouter, Header

from laminhub_rest.orm._cloud_run_instance import (
    sb_select_cloud_run_instance_by_lamin_instance_id,
    sb_select_cloud_run_instance_by_server_name,
    sb_select_least_recently_used_generic_cloud_run_instance,
    sb_update_cloud_run_instance,
    sb_update_last_access_at,
)

from ..utils._supabase_client import SbClientAdmin, SbClientFromAccesToken
from .utils import extract_access_token

router = APIRouter(prefix="/cloud-run")


@router.get("/linked-instance/{lamin_instance_id}")
def get_linked_cloud_run_instance(
    lamin_instance_id: str,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        return sb_select_cloud_run_instance_by_lamin_instance_id(
            lamin_instance_id=lamin_instance_id, supabase_client=supabase_client
        )


@router.post("/link/{lamin_instance_id}/{cloud_run_instance_id}")
def link_to_cloud_run_instance(lamin_instance_id: str, cloud_run_instance_id: str):
    with SbClientAdmin().connect() as supabase_client:
        return sb_update_cloud_run_instance(
            cloud_run_instance_id=cloud_run_instance_id,
            lamin_instance_id=lamin_instance_id,
            supabase_client=supabase_client,
        )


@router.post("/auto-link/{lamin_instance_id}")
def link_to_evicted_cloud_run_instance(lamin_instance_id: str):
    with SbClientAdmin().connect() as supabase_client:
        cloud_run_instance = (
            sb_select_least_recently_used_generic_cloud_run_instance(  # noqa
                supabase_client=supabase_client
            )
        )

    return link_to_cloud_run_instance(
        lamin_instance_id=lamin_instance_id,
        cloud_run_instance_id=cloud_run_instance["id"],
    )


@router.get("/{cloud_run_instance_name}")
def get_cloud_run_instance_by_name(cloud_run_instance_name: str):
    with SbClientAdmin().connect() as supabase_client:
        return sb_select_cloud_run_instance_by_server_name(
            cloud_run_instance_name=cloud_run_instance_name,
            supabase_client=supabase_client,
        )


@router.post("/update-last-access-at/{cloud_run_instance_id}")
def update_last_access_at(cloud_run_instance_id: str):
    with SbClientAdmin().connect() as supabase_client:
        return sb_update_last_access_at(
            cloud_run_instance_id=cloud_run_instance_id, supabase_client=supabase_client
        )


def get_evicted_cloud_run_instance():
    with SbClientAdmin().connect() as supabase_client:
        return sb_select_least_recently_used_generic_cloud_run_instance(  # noqa
            supabase_client=supabase_client
        )


def get_default_instance_identifier():
    return "laminlabs/laminapp-default-instance"
