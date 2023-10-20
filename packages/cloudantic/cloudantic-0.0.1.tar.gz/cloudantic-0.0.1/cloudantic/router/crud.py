from typing import Generic, Optional, Type, TypeVar

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse

from ..schema import DynaModel, Operator
from ..schema.streams import DynamoDBStreams
from ..utils import async_io, handle

T = TypeVar("T", bound=DynaModel)


class CRUDRouter(APIRouter, Generic[T]):
    schema: Type[T]

    def __init__(self, schema: Type[T], *args, **kwargs):
        super().__init__(
            prefix=f"/{schema.__name__.lower()}",
            tags=[schema.__name__],
            *args,
            **kwargs,
        )
        self.schema = schema
        self.stream = DynamoDBStreams[schema](schema)

        @self.get("/{pk}")
        async def get_one(pk: str, sk: str):
            return await self._get_one(pk, sk)

        @self.get("/{pk}/query")
        async def get_many(
            pk: str, sk: Optional[str] = None, op: Optional[Operator] = None
        ):
            return await self._get_many(pk, sk, op)

        @self.post("/")
        async def create(
            data: self.schema = Body(example=self._example_request_body()),
        ):
            return await self._create(data)

        @self.delete("/{pk}")
        async def delete(pk: str, sk: str):
            return await self._delete(pk, sk)

        @self.get("/")
        async def get_all():
            return await self._get_all()

        @self.get("/stream")
        async def stream():
            async def event_generator():
                async for event in self.stream.generator(self.schema.__table_name__()):
                    yield f"data: {event.json()}\n\n"

            return StreamingResponse(
                content=event_generator(), media_type="text/event-stream"
            )

    @handle
    @async_io
    def _get_one(self, pk: str, sk: str):
        return self.schema.get(pk, sk)

    @handle
    @async_io
    def _get_many(self, pk: str, sk: str, op: Operator):
        return self.schema.query(pk, sk, op)

    @handle
    @async_io
    def _create(self, data: T):
        return self.schema.put(data)

    @handle
    @async_io
    def _delete(self, pk: str, sk: str):
        return self.schema.delete(pk, sk)

    @handle
    @async_io
    def _get_all(self):
        return self.schema.scan()

    def _example_request_body(self):
        _schema = self.schema.schema()
        example = {}
        for k, v in _schema["properties"].items():
            example[k] = v.get("type")
        return example
