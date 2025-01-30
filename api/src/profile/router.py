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


@router.get("/list", status_code=status.HTTP_200_OK)
async def get_profiles(uow: uowDEP) -> list[ProfileShowResponseSchema]:
    return await ProfileService(uow).get_profiles()


@router.get("/get/{slug}/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def parse_steam_link(
    uow: uowDEP,
    slug: str,
):
    return await ProfileService(uow).get_profile(slug)


@router.delete("/delete/{profile_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(uow: uowDEP, profile_id: int):
    return await ProfileService(uow).delete_profile(profile_id)
