from typing import Type, TypeVar, cast
from typing_extensions import Annotated

from functools import lru_cache
from copy import deepcopy

from pydantic import BaseModel


TEntity = TypeVar('TEntity', bound='BaseEntity')
Partial = Annotated[TEntity, 'Partially initialized instance']


def snake_to_camel(s: str):
    first_word, *next_words = s.split('_')
    return first_word + ''.join(map(str.title, next_words))


@lru_cache(maxsize=None)
def create_partial_entity_cls(cls: Type[TEntity]) -> Partial[TEntity]:
    partial_cls_name = f'{cls.__name__}Partial'
    partial_cls = type(
        partial_cls_name,
        cls.__bases__,
        dict(cls.__dict__)
    )

    partial_cls.__fields__ = deepcopy(partial_cls.__fields__)
    for field in partial_cls.__fields__.values():
        field.required = False

    return cast(Partial[TEntity], partial_cls)


class BaseEntity(BaseModel):
    @classmethod
    def partial(cls: Type[TEntity], *args, **kwargs) -> Partial[TEntity]:
        partial_cls = create_partial_entity_cls(cls)
        return partial_cls(*args, **kwargs)

    class Config:
        alias_generator = snake_to_camel
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        frozen = True
