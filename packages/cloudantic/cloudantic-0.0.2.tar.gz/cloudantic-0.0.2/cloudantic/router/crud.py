from typing import Generic, Optional, Type, TypeVar

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse

from ..schema import DynaModel, Operator
from ..schema.streams import DynamoDBStreams
from ..utils import async_io, handle

T = TypeVar("T", bound=DynaModel)


class CRUDRouter(APIRouter, Generic[T]):
    """
    A router that provides CRUD (Create, Read, Update, Delete) operations for a given schema.

    Attributes:
    - schema (Type[T]): The schema to be used for the CRUD operations.
    """

    schema: Type[T]

    def __init__(self, schema: Type[T], *args, **kwargs):
        """
        Initializes the CRUDRouter with the given schema.

        Parameters:
        - schema (Type[T]): The schema to be used for the CRUD operations.
        - *args: Additional arguments to be passed to the APIRouter constructor.
        - **kwargs: Additional keyword arguments to be passed to the APIRouter constructor.
        """
        super().__init__(
            prefix=f"/{schema.__name__.lower()}",
            tags=[schema.__name__],
            *args,
            **kwargs,
        )
        self.schema = schema
        self.stream = DynamoDBStreams[schema](schema)

        @self.get("/get/{pk}")
        async def get_one(pk: str, sk: str):
            return await self._get_one(pk, sk)

        @self.get("/query/{pk}")
        async def get_many(
            pk: str, sk: Optional[str] = None, op: Optional[Operator] = None
        ):
            return await self._get_many(pk, sk, op)

        @self.post("/")
        async def create(
            data: self.schema = Body(example=self._example_request_body()), # type: ignore / Ohhh silly mypy, I still love you
        ):
            return await self._create(data)

        @self.delete("/{pk}")
        async def delete(pk: str, sk: str):
            return await self._delete(pk, sk)

        @self.get("/all")
        async def get_all():
            return await self._get_all()

        @self.get("/stream")
        async def stream():
            async def event_generator():
                for event in self.stream.generator(DynaModel.__table_name__()):
                    yield f"data: {event.json()}\n\n"

            return StreamingResponse(
                content=event_generator(), media_type="text/event-stream"
            )

    @handle
    @async_io
    def _get_one(self, pk: str, sk: str):
        """
        Retrieves a single item from the database.

        Parameters:
        - pk (str): The partition key of the item to retrieve.
        - sk (str): The sort key of the item to retrieve.

        Returns:
        The retrieved item.
        """
        return self.schema.get(pk, sk)

    @handle
    @async_io
    def _get_many(self, pk: str, sk: Optional[str] = None, op: Optional[Operator] = None):
        """
        Retrieves multiple items from the database.

        Parameters:
        - pk (str): The partition key of the items to retrieve.
        - sk (str): The sort key of the items to retrieve.
        - op (Optional[Operator]): The operator to use for the query.

        Returns:
        The retrieved items.
        """
        return self.schema.query(pk, sk, op)

    @handle
    @async_io
    def _create(self, data: T):
        """
        Creates a new item in the database.

        Parameters:
        - data (T): The data to be stored in the new item.

        Returns:
        The created item.
        """
        return self.schema.put(data)

    @handle
    @async_io
    def _delete(self, pk: str, sk: str):
        """
        Deletes an item from the database.

        Parameters:
        - pk (str): The partition key of the item to delete.
        - sk (str): The sort key of the item to delete.

        Returns:
        The deleted item.
        """
        return self.schema.delete(pk, sk)

    @handle
    @async_io
    def _get_all(self):
        """
        Retrieves all items from the database.

        Returns:
        All items in the database.
        """
        return self.schema.scan()

    def _example_request_body(self):
        """
        Generates an example request body based on the schema.

        Returns:
        An example request body.
        """
        _schema = self.schema.schema()
        example = {}
        for k, v in _schema["properties"].items():
            example[k] = v.get("type")
        return example
