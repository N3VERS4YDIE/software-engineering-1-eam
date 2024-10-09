from typing import Dict, Generic, List, Type, TypeVar

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel

from app.services.base_service import BaseService


class BaseController:
    def __init__(self, model, entity, service: BaseService):
        self.model = model
        self.entity = entity
        self.router = APIRouter()
        self.service = service

        self.router.add_api_route(
            "", self.create, methods=["POST"], response_model=model
        )
        self.router.add_api_route(
            "", self.get_all, methods=["GET"], response_model=List[model]
        )
        self.router.add_api_route(
            "/{id}", self.get_by_id, methods=["GET"], response_model=model
        )
        self.router.add_api_route(
            "/{id}", self.update, methods=["PUT"], response_model=model
        )
        self.router.add_api_route("/{id}", self.delete, methods=["DELETE"])

    def get_router(self):
        return self.router

    async def get_all(self):
        return self.service.get_all()

    async def get_by_id(self, id: int):
        model = self.service.get_by_id(id)
        if model is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return model

    async def create(self, model: dict = Body(...)):
        return self.service.create(model)

    async def update(self, id: int, model: dict = Body(...)):
        model["id"] = id
        model = self.service.update(model)

        if model is None:
            raise HTTPException(status_code=404, detail="Not found")

        return model

    async def delete(self, id: int):
        is_deleted = self.service.delete(id)

        if not is_deleted:
            raise HTTPException(status_code=404, detail="Not found")

        return {"msg": "Item deleted successfully"}
