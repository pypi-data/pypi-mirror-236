from fastapi import FastAPI

from .crud import CRUDRouter, DynaModel, TypeVar, async_io, handle

D = TypeVar("D", bound=DynaModel)


def setupRoutes(app: FastAPI):
    for model in DynaModel.__subclasses__():
        app.include_router(CRUDRouter[model](model))


def setupTable(app: FastAPI):
    @handle
    @async_io
    def _setupTable():
        return DynaModel.create_table()

    @app.on_event("startup")
    async def startup():
        await _setupTable()