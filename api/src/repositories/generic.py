import uuid

from typing import Generic, TypeVar, Optional, Any

from pydantic import BaseModel

from sqlalchemy import select, insert, update, delete, func, exists, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql.expression import UnaryExpression, BinaryExpression, Select

from ..core.db.base import Base
from ..core.dependencies import PaginationParams


Model = TypeVar("Model", bound=Base)
CreateScheme = TypeVar("CreateScheme", bound=BaseModel)
UpdateScheme = TypeVar("UpdateScheme", bound=BaseModel)


class Repository(Generic[Model]):
    def __init__(self, session: AsyncSession, model: type[Model]) -> None:
        self.session = session
        self.model = model

    async def _add_options_to_query(self, query: Select, options: list[Load]) -> Select:
        """
        Adds options (e.g., joinedload, selectinload) to the query for eager loading.
        """
        for option in options:
            query = query.options(option)
        return query

    async def _add_filters_to_query(self, query: Select, filters: list[BinaryExpression]) -> Select:
        """
        Adds filters (conditions) to the query.
        """
        if filters:
            query = query.where(*filters)
        return query

    async def _add_joins_to_query(
        self,
        query: Select,
        joins: list[InstrumentedAttribute | AliasedClass | tuple[Select, BinaryExpression]],
    ) -> Select:
        """
        Adds joins to the query.
        Supports joins on:
        - InstrumentedAttribute (model attribute)
        - AliasedClass (aliased tables)
        - Subqueries with explicit join conditions (subquery, condition)
        """
        for join in joins:
            if isinstance(join, tuple):  # Handle subquery with condition
                subquery, condition = join
                query = query.join(subquery, condition)
            else:
                query = query.join(join)
        return query

    async def _add_pagination_to_query(
        self,
        query: Select,
        pagination: PaginationParams,
    ) -> Select:
        """
        Adds pagination to the query with the provided page and page_size.
        """
        return query.limit(pagination.size).offset((pagination.page - 1) * pagination.size)

    async def _apply_query_modifiers(
        self,
        *,
        query: Select,
        options: Optional[list[Load]] = None,
        filters: Optional[list[BinaryExpression]] = None,
        order_by: Optional[list[InstrumentedAttribute | UnaryExpression]] = None,
        joins: Optional[
            list[InstrumentedAttribute | AliasedClass | tuple[Select, BinaryExpression]]
        ] = None,
        pagination: Optional[PaginationParams] = None,
        limit: Optional[int] = None,
    ) -> Select:
        """
        Applies query modifiers (options, filters, order_by, joins, pagination) to the query.
        """
        if options:
            query = await self._add_options_to_query(query, options)
        if filters:
            query = await self._add_filters_to_query(query, filters)
        if joins:
            query = await self._add_joins_to_query(query, joins)
        if pagination:
            query = await self._add_pagination_to_query(query, pagination)
        if order_by:
            query = query.order_by(*order_by)
        if limit:
            query = query.limit(limit)
        return query

    async def create(self, *, obj_in: CreateScheme) -> int | uuid.UUID:
        stmt = insert(self.model).values(**obj_in.model_dump()).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def create_instance(self, *, obj_in: CreateScheme, exclude: dict | None = None) -> Model:
        return self.model(**obj_in.model_dump(exclude_unset=True, exclude=exclude))

    async def update(
        self,
        obj_id: int | uuid.UUID,
        obj_in: UpdateScheme,
    ) -> Model:
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def update_by_attr(
        self,
        *,
        attr: InstrumentedAttribute,
        value: Any,
        obj_in: UpdateScheme,
        exclude_unset: bool = True,
    ) -> Model:
        stmt = (
            update(self.model)
            .where(attr == value)
            .values(**obj_in.model_dump(exclude_unset=exclude_unset))
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def update_instance(
        self, *, obj: Model, obj_in: UpdateScheme, exclude_unset: bool = True
    ) -> Model:
        for field, value in obj_in.model_dump(exclude_unset=exclude_unset).items():
            setattr(obj, field, value)
        return obj

    async def delete(self, obj_id: int | uuid.UUID) -> None:
        stmt = delete(self.model).where(self.model.id == obj_id)
        await self.session.execute(stmt)

    async def delete_by_attr(self, *, attr: InstrumentedAttribute, value: Any) -> None:
        stmt = delete(self.model).where(attr == value)
        await self.session.execute(stmt)

    async def get_count(
        self,
        filters: Optional[list[BinaryExpression]] = None,
    ) -> int:
        query = select(func.count()).select_from(self.model)
        if filters:
            query = await self._add_filters_to_query(query, filters)
        res = await self.session.execute(query)
        return res.scalar()

    async def get_list(
        self,
        *,
        options: Optional[list[Load]] = None,
        filters: Optional[list[BinaryExpression]] = None,
        order_by: Optional[list[InstrumentedAttribute | UnaryExpression]] = None,
        joins: Optional[
            list[InstrumentedAttribute | AliasedClass | tuple[Select, BinaryExpression]]
        ] = None,
        pagination: Optional[PaginationParams] = None,
        limit: Optional[int] = None,
    ):
        query = select(self.model)
        query = await self._apply_query_modifiers(
            query=query,
            options=options,
            filters=filters,
            order_by=order_by,
            joins=joins,
            pagination=pagination,
            limit=limit,
        )
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_one_by_attr(
        self,
        *,
        attr: InstrumentedAttribute,
        value: Any,
        options: Optional[list[Load]] = None,
    ) -> Model:
        query = select(self.model).where(attr == value)
        if options:
            query = await self._add_options_to_query(query, options)
        res = await self.session.execute(query)
        return res.scalar()

    async def get_one_by_attrs(
        self,
        *,
        attrs_values: dict[InstrumentedAttribute, Any],
    ):
        query = select(self.model).where(
            and_(*[attr == value for attr, value in attrs_values.items()])
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def get_one_by_id(
        self,
        *,
        obj_id: int | uuid.UUID,
        options: Optional[list[Load]] = None,
    ) -> Model:
        return await self.get_one_by_attr(attr=self.model.id, value=obj_id, options=options)

    async def exists_by_id(self, obj_id: int | uuid.UUID) -> bool:
        query = exists().where(self.model.id == obj_id).select()
        res = await self.session.execute(query)
        return res.scalar()

    async def exists_by_attr(
        self,
        *,
        attr: InstrumentedAttribute,
        value: Any,
    ) -> bool:
        query = exists().where(attr == value).select()
        res = await self.session.execute(query)
        return res.scalar()
