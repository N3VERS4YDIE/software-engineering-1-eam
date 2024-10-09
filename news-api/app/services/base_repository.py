from typing import Generic, List, Optional, Type, TypeVar


class BaseRepository:
    def __init__(self, entity):
        self.entity = entity

    def get_all(self):
        return list(self.entity.select())

    def get_by_id(self, id: int):
        try:
            return self.entity.get(self.entity.id == id)
        except self.entity.DoesNotExist:
            return None

    def create(self, model):
        return self.entity.create(**model)

    def delete(self, id: int) -> bool:
        query = self.entity.delete().where(self.entity.id == id)
        return query.execute() > 0
