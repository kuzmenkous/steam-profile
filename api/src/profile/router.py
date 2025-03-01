from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse

from ..core.db.dependencies import uowDEP

from .schemas import CreateProfileSchema, ProfileShowResponseSchema, UpdateProfileSchema
from .service import ProfileService


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def create_profile(uow: uowDEP, data: CreateProfileSchema) -> ProfileShowResponseSchema:
    return await ProfileService(uow).create_profile(data)


@router.put("/update/{profile_id}/", status_code=status.HTTP_200_OK)
async def update_profile(
    uow: uowDEP,
    profile_id: int,
    data: UpdateProfileSchema,
):
    return await ProfileService(uow).update_profile(profile_id, data)


@router.post(
    "/invite_link_path/generate/{profile_id}/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProfileShowResponseSchema,
)
async def generate_invite_link_path(
    uow: uowDEP,
    profile_id: int,
) -> ProfileShowResponseSchema:
    return await ProfileService(uow).generate_new_invite_link_path(profile_id=profile_id)


@router.get("/list", status_code=status.HTTP_200_OK)
async def get_profiles(uow: uowDEP) -> list[ProfileShowResponseSchema]:
    return await ProfileService(uow).get_profiles()


@router.get("/get/by_invite_link_path/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_profile_by_invite_link_path(
    uow: uowDEP,
    invite_link_path: str,
):
    return await ProfileService(uow).get_profile_by_invite_link_path(invite_link_path)


@router.get("/get/{slug}/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_profile_by_slug(
    uow: uowDEP,
    slug: str,
    with_invite: bool = False,
):
    return await ProfileService(uow).get_profile(slug, with_invite)


@router.get("/get/by_id/{profile_id}/", status_code=status.HTTP_200_OK)
async def get_profile_by_id(uow: uowDEP, profile_id: int):
    return await ProfileService(uow).get_profile_by_id(profile_id)


@router.delete("/delete/{profile_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(uow: uowDEP, profile_id: int):
    return await ProfileService(uow).delete_profile(profile_id)
