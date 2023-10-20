from __future__ import annotations

import asyncio
from datetime import datetime
from typing import (Dict, Generator, Generic, List, Literal, Optional, Type,
                    TypeAlias, TypeVar)

from boto3 import client  # type: ignore
from boto3.dynamodb.types import TypeDeserializer  # type: ignore
from boto3.dynamodb.types import TypeSerializer
from pydantic import BaseConfig  # pylint: disable=no-name-in-module
from pydantic import (BaseModel, Extra,  # pylint: disable=no-name-in-module
                      Field)

from .odm import DynaModel

# TypeAliases

D = TypeVar("D", bound=DynaModel)

StreamStatus: TypeAlias = Literal["ENABLED", "DISABLED", "ENABLING", "DISABLING"]
StreamViewType: TypeAlias = Literal[
    "NEW_IMAGE", "OLD_IMAGE", "NEW_AND_OLD_IMAGES", "KEYS_ONLY"
]
KeySchemaKeyType: TypeAlias = Literal["HASH", "RANGE"]
ShardIteratorType: TypeAlias = Literal[
    "TRIM_HORIZON", "LATEST", "AT_SEQUENCE_NUMBER", "AFTER_SEQUENCE_NUMBER"
]

EventName: TypeAlias = Literal["INSERT", "MODIFY", "REMOVE"]

# TypeDefs


class TypeDef(BaseModel):
    class Config(BaseConfig):
        extra = Extra.allow
        json_encoders = {
            datetime: lambda v: v.astimezone().isoformat(),
        }
        arbitrary_types_allowed = True
        orm_mode = True


class SequenceNumberRangeTypeDef(TypeDef):
    StartingSequenceNumber: Optional[str]
    EndingSequenceNumber: Optional[str]


class ShardTypeDef(TypeDef):
    ShardId: str
    SequenceNumberRange: SequenceNumberRangeTypeDef
    ParentShardId: Optional[str]


class KeySchemaTypeDef(TypeDef):
    AttributeName: str
    KeyType: KeySchemaKeyType


class DynamoValueTypeDef(TypeDef):
    S: Optional[str]
    N: Optional[str]
    B: Optional[bytes]
    SS: Optional[List[str]]
    NS: Optional[List[str]]
    BS: Optional[List[bytes]]
    M: Optional[Dict[str, "DynamoValueTypeDef"]]
    L: Optional[List["DynamoValueTypeDef"]]
    NULL: Optional[bool]
    BOOL: Optional[bool]

    def keys(self):
        return self.__fields__.keys()
    
    def values(self):
        return self.__fields__.values()
    
    def items(self):
        return self.__fields__.items()
    
    def __getitem__(self, key:str):
        return self.dict()[key]

DynamoValueTypeDef.update_forward_refs()


class DynamoDBTypeDef(TypeDef):
    ApproximateCreationDateTime: datetime
    Keys: Dict[str, DynamoValueTypeDef]
    NewImage: Dict[str, DynamoValueTypeDef]
    OldImage: Optional[Dict[str, DynamoValueTypeDef]]
    SequenceNumber: str
    SizeBytes: int
    StreamViewType: StreamViewType


class UserIdentityTypeDef(TypeDef):
    PrincipalId: str
    Type: str


class StreamDescriptionTypeDef(TypeDef):
    StreamArn: str
    StreamLabel: str
    StreamStatus: StreamStatus
    StreamViewType: StreamViewType
    CreationRequestDateTime: datetime
    TableName: str
    KeySchema: List[KeySchemaTypeDef] = Field(
        default=[
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ]
    )
    Shards: List[ShardTypeDef] = Field(default=[])
    LastEvaluatedShardId: Optional[str]
    StreamDescription: Optional[str]


class ListStreamReturnTypeDef(TypeDef):
    StreamArn: str
    StreamLabel: str
    TableName: str


# Request/Response


class DescribeStreamsRequest(TypeDef):
    StreamArn: str
    Limit: Optional[int] = Field(default=None)
    ExclusiveStartShardId: Optional[str] = Field(default=None)


class RecordTypeDef(TypeDef):
    eventID: str
    eventName: EventName
    eventVersion: str
    eventSource: str
    awsRegion: str
    dynamodb: DynamoDBTypeDef
    userIdentity: Optional[UserIdentityTypeDef]


class DescribeStreamsResponse(TypeDef):
    StreamDescription: StreamDescriptionTypeDef


class GetShardIteratorRequest(TypeDef):
    StreamArn: str
    ShardId: str
    ShardIteratorType: ShardIteratorType
    SequenceNumber: Optional[str] = Field(default=None)


class GetShardIteratorResponse(TypeDef):
    ShardIterator: str


class GetRecordsRequest(TypeDef):
    ShardIterator: str
    Limit: Optional[int] = Field(default=None)


class GetRecordsResponse(TypeDef):
    Records: List[RecordTypeDef] = Field(default=[])
    NextShardIterator: str


class ListStreamsRequest(TypeDef):
    TableName: str
    Limit: Optional[int] = Field(default=None)
    ExclusiveStartStreamArn: Optional[str] = Field(default=None)


class ListStreamResponse(TypeDef):
    Streams: List[ListStreamReturnTypeDef] = Field(default=[])
    LastEvaluatedStreamArn: Optional[str] = Field(default=None)


class DynamoDBStreams(Generic[D]):
    def __init__(self, model: Type[D]):
        self.__table_name__ = model.__table_name__()
        self.model = model

    @property
    def client(self):
        return client("dynamodbstreams")

    def list_streams(self, request: ListStreamsRequest) -> ListStreamResponse:
        all_streams: List[ListStreamReturnTypeDef] = []
        last_evaluated_stream_arn: str | None = None
        while True:
            response = self.client.list_streams(
                **request.dict(exclude_none=True),
            )
            all_streams.extend(response.get("Streams", []))
            last_evaluated_stream_arn = response.get("LastEvaluatedStreamArn", None)
            if last_evaluated_stream_arn is None:  # type: ignore
                break
        return ListStreamResponse(
            Streams=all_streams, LastEvaluatedStreamArn=last_evaluated_stream_arn
        )

    def describe_stream(
        self, request: DescribeStreamsRequest
    ) -> DescribeStreamsResponse:
        response = self.client.describe_stream(**request.dict(exclude_none=True))
        return DescribeStreamsResponse(**response)  # type: ignore

    def get_shard_iterator(
        self, request: GetShardIteratorRequest
    ) -> GetShardIteratorResponse:
        response = self.client.get_shard_iterator(**request.dict(exclude_none=True))
        return GetShardIteratorResponse(**response)  # type: ignore

    def get_records(self, request: GetRecordsRequest) -> GetRecordsResponse:
        response = self.client.get_records(**request.dict(exclude_none=True))
        return GetRecordsResponse(**response)  # type: ignore

    async def generator(self, table_name:str):
        streams = self.list_streams(
            ListStreamsRequest(TableName=table_name)
        ).Streams
        for stream in streams:
            stream_arn = stream.StreamArn
            shards = self.describe_stream(
                DescribeStreamsRequest(StreamArn=stream_arn)
            ).StreamDescription.Shards
            for shard in shards:
                shard_id = shard.ShardId
                shard_iterator = self.get_shard_iterator(
                    GetShardIteratorRequest(
                        StreamArn=stream_arn,
                        ShardId=shard_id,
                        ShardIteratorType="TRIM_HORIZON",
                    )
                ).ShardIterator
                while True:
                    records = self.get_records(
                        GetRecordsRequest(ShardIterator=shard_iterator)
                    ).Records
                    for record in records:
                        data = record.dynamodb.NewImage
                        data_ = TypeDeserializer().deserialize({"M": data})
                        yield self.model(**data_)
                    shard_iterator = self.get_records(
                        GetRecordsRequest(ShardIterator=shard_iterator)
                    ).NextShardIterator
                    await asyncio.sleep(0.1)