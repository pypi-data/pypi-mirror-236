from .router import CRUDRouter, setup_routes, setup_table
from .schema import DynamoDBStreams, DynaModel, Field
from .services import KinesisStream, StorageBucket

__title__ = "Cloudantic"
__version__ = "0.0.2"
__author__ = "Oscar Bahamonde <o.bahamonde@globant.com>"
__description__ = "FastAPI + AWS (DynamoDB, Kinesis, S3, Dynamo Streams)"
