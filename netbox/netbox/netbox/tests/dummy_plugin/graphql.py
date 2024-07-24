from typing import List
import strawberry
import strawberry_django

from . import models


@strawberry_django.type(
    models.DummyModel,
    fields='__all__',
)
class DummyModelType:
    pass


@strawberry.type
class DummyQuery:
    @strawberry.field
    def dummymodel(self, id: int) -> DummyModelType:
        return None
    dummymodel_list: List[DummyModelType] = strawberry_django.field()


schema = [
    DummyQuery,
]
