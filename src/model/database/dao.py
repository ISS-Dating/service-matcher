from typing import Generic, Optional, Type, NoReturn, TypeVar, Generator

from contextlib import contextmanager

from pymongo.collection import Collection

from model.entity import BaseEntity, Partial
from model.database.connection import get_database, get_client

TEntity = TypeVar('TEntity', bound='BaseEntity')


def _get_collection(entity_type: Type[BaseEntity]) -> Collection:
    collection_name = entity_type.__name__[:1].lower() + entity_type.__name__[1:]
    return get_database().get_collection(collection_name)


def raise_(e: Exception, from_: Optional[Exception] = None) -> NoReturn:
    if from_ is not None:
        raise e from from_

    raise e


class DAO(Generic[TEntity]):
    def __init__(self, entity_type: Type[TEntity], collection: Optional[Collection] = None) -> None:
        self._entity_type = entity_type
        self._collection = collection or _get_collection(entity_type)
        self._transaction_session = None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._entity_type.__name__}, {self._collection})'

    def create(self, entity: TEntity) -> None:
        self._collection.insert_one(entity.dict(by_alias=True), session=self._transaction_session)

    def get(self, filter_: Partial[TEntity]) -> Optional[TEntity]:
        filter_dict = filter_.dict(by_alias=True, exclude_unset=True, exclude_none=True)\
                      or raise_(ValueError('Empty filter'))

        document_dict = self._collection.find_one(filter_dict)

        if document_dict is None:
            return None

        return self._entity_type(**document_dict)

    def update(self, filter_: Partial[TEntity], updated_values: Partial[TEntity]) -> None:
        filter_dict = filter_.dict(by_alias=True, exclude_unset=True, exclude_none=True)\
                      or raise_(ValueError('Empty filter'))

        updated_dict = updated_values.dict(by_alias=True, exclude_none=True)
        self._collection.update_one(filter_dict, {'$set': updated_dict}, session=self._transaction_session)

    def replace(self, filter_: Partial[TEntity], entity: TEntity, upsert: bool = True) -> None:
        filter_dict = filter_.dict(by_alias=True, exclude_unset=True, exclude_none=True)\
                      or raise_(ValueError('Empty filter'))
        entity_dict = entity.dict(by_alias=True)
        self._collection.replace_one(filter_dict, entity_dict, upsert=upsert, session=self._transaction_session)


@contextmanager
def transaction(dao: DAO, *dao_list: DAO) -> Generator:
    dao_list = (dao, *dao_list)
    try:
        with get_client().start_session() as session:
            with session.start_transaction():
                for dao_ in dao_list:
                    dao_._transaction_session = session
        yield
    finally:
        for dao_ in dao_list:
            dao_._transaction_session = None
