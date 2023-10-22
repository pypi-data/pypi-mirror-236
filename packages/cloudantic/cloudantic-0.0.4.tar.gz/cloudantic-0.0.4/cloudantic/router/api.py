from fastapi import FastAPI

from .crud import CRUDRouter, DynaModel, TypeVar

D = TypeVar("D", bound=DynaModel)


def setup_routes(app: FastAPI):
    """Automatically setup CRUD routes for all subclasses of DynaModel."""
    for model in DynaModel.__subclasses__():
        app.include_router(CRUDRouter[model](model))
    return app


def setup_table(app: FastAPI):
    """Automatically hooks up a startup event to create the DynamoDB Single Table and adds the schemas to the openapi spec.
    [NOTE]: It's a chainable function, so you can do setup_table(setup_routes(app))
    """

    async def _setup_table():
        await DynaModel.create_table()

    @app.on_event("startup")
    async def startup():
        await _setup_table()

    return app
