from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from boto3 import Session
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from pydantic import BaseConfig  # pylint: disable=no-name-in-module
from pydantic import BaseModel, Extra, Field  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

T = TypeVar("T")
D = TypeVar("D", bound="DynaModel")
P = ParamSpec("P")
Operator = Literal["=", ">", "<", ">=", "<=", "begins_with", "between"]


def emptystring() -> str:
    return cast(str, None)


REGION = "us-east-1"
dynamodb = Session().client(service_name="dynamodb", region_name=REGION)  # type: ignore


class LazyProxy(Generic[T], ABC):
    def __init__(self) -> None:
        self.__proxied: T | None = None

    def __getattr__(self, attr: str) -> object:
        return getattr(self.__get_proxied__(), attr)

    def __repr__(self) -> str:
        return repr(self.__get_proxied__())

    def __dir__(self) -> Iterable[str]:
        return self.__get_proxied__().__dir__()

    def __get_proxied__(self) -> T:
        proxied = self.__proxied
        if proxied is not None:
            return proxied

        self.__proxied = proxied = self.__load__()
        return proxied

    def __set_proxied__(self, value: T) -> None:
        self.__proxied = value

    def __as_proxied__(self) -> T:
        return cast(T, self)

    @abstractmethod
    def __load__(self) -> T:
        ...


class DynamoDB(LazyProxy[Session], Generic[D]):
    entities: Set[Type[D]] = set()
    session: Session

    def __init__(self, model: Type[D]) -> None:
        self.model = model
        self.session = self.__load__()
        super().__init__()

    def __load__(self) -> Session:
        return Session()

    @classmethod
    def __class_getitem__(cls, item: Type[D]) -> Type[DynamoDB[D]]:
        cls.entities.add(item)
        return cls

    @property
    def __table_name__(self) -> str:
        ents: List[str] = []
        for ent in self.entities:
            ents.append(ent.__name__)
            ents.sort()
        return "-".join(ents)

    @property
    def serializer(self) -> TypeSerializer:
        return TypeSerializer()

    @property
    def deserializer(self) -> TypeDeserializer:
        return TypeDeserializer()

    @property
    def client(self):
        return self.session.client(service_name="dynamodb", region_name="us-east-1")  # type: ignore

    @property
    def resource(self):
        return self.session.resource(service_name="dynamodb", region_name="us-east-1")  # type: ignore

    def serialize(self: DynamoDB[D], instance: D) -> Dict[str, Any]:
        return self.serializer.serialize(instance.to_dict())["M"]  # type: ignore

    def deserialize(self: DynamoDB[D], data: Dict[str, Any]) -> D:
        return self.deserializer.deserialize({"M": data})  # type: ignore

    @staticmethod
    def create_all(name: str) -> None:
        tables = dynamodb.list_tables()["TableNames"]
        if name not in tables:
            dynamodb.create_table(
                TableName=name,
                AttributeDefinitions=[
                    {"AttributeName": "pk", "AttributeType": "S"},
                    {"AttributeName": "sk", "AttributeType": "S"},
                ],
                KeySchema=[
                    {"AttributeName": "pk", "KeyType": "HASH"},
                    {"AttributeName": "sk", "KeyType": "RANGE"},
                ],
                BillingMode="PAY_PER_REQUEST",
            )
            dynamodb.get_waiter("table_exists").wait(TableName=name)

    def get(self: DynamoDB[D], pk: str, sk: str) -> D:
        response = self.client.get_item(
            TableName=self.__table_name__,
            Key={
                "pk": self.serializer.serialize(pk),
                "sk": self.serializer.serialize(sk),
            },
        )
        return self.deserialize(response.get("Item", {}))

    def put(self: DynamoDB[D], instance: D) -> None:
        self.client.put_item(
            TableName=self.__table_name__, Item=self.serialize(instance)
        )

    def delete(self: DynamoDB[D], pk: str, sk: str) -> None:
        self.client.delete_item(
            TableName=self.__table_name__,
            Key={
                "pk": self.serializer.serialize(pk),
                "sk": self.serializer.serialize(sk),
            },
        )

    def query(
        self: DynamoDB[D],
        pk: str,
        sk: Optional[str] = None,
        operator: Optional[Operator] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[D]:
        key_condition = "pk = :pk"
        expression_values = {":pk": {"S": pk}}

        if sk:
            if operator == "begins_with" and isinstance(sk, str):
                key_condition += " AND begins_with ( sk, :sk )"
                expression_values[":sk"] = {"S": sk}
            elif operator == "between" and isinstance(sk, str):
                key_condition += " AND sk BETWEEN :sk0 AND :sk1"
                from_, to_ = sk.split("-")
                expression_values[":sk0"] = {"S": from_}
                expression_values[":sk1"] = {"S": to_}
            elif operator in ["=", ">", "<", ">=", "<="] and isinstance(sk, str):
                key_condition += f" AND sk {operator} :sk"
                expression_values[":sk"] = {"S": sk}
            else:
                raise ValueError("Invalid sort key")
        if limit:
            key_condition += f" LIMIT {limit}"
        if offset:
            key_condition += f" OFFSET {offset}"
        response = self.client.query(
            TableName=self.__table_name__,
            KeyConditionExpression=key_condition,
            ExpressionAttributeValues=expression_values,
        )
        return [self.deserialize(item) for item in response.get("Items", [])]

    def scan(
        self: DynamoDB[D], limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[D]:
        scan_kwargs: Dict[str, Any] = {}
        if limit:
            scan_kwargs["Limit"] = limit
        if offset:
            scan_kwargs["Offset"] = offset
        response = self.client.scan(TableName=self.__table_name__, **scan_kwargs)
        return [self.deserialize(item) for item in response.get("Items", [])]


class DynaModel(BaseModel):
    pk: str = Field(default_factory=emptystring, alias="_pk")
    sk: str = Field(default_factory=emptystring, alias="_sk")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.pk = self.pk_
        self.sk = self.sk_

    def to_dict(
        self,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
    ) -> Dict[str, Any]:
        return super().dict(
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def dict(self, **kwargs: Any):
        exclude_set: set[Any] = kwargs.pop("exclude", set()) or set()
        exclude_set.update({"pk", "sk"})
        return super().dict(exclude=exclude_set, **kwargs)

    def json(self, **kwargs: Any):
        exclude_set: set[Any] = kwargs.pop("exclude", set()) or set()
        exclude_set.update({"pk", "sk"})
        return super().json(exclude=exclude_set, **kwargs)

    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.astimezone().isoformat(),
            Decimal: lambda d: float(d),
            UUID: lambda u: str(u),
            Enum: lambda e: e.value,
        }
        use_enum_values = True
        extra = Extra.allow

        @staticmethod
        def schema_extra(schema: Dict[str, Any], model_class: Type[DynaModel]) -> None:  # type: ignore
            schema["properties"].pop("_pk")
            schema["properties"].pop("_sk")

    @classmethod
    def __init_subclass__(cls: Type[D], **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls.db = DynamoDB[cls](cls)

    @property
    def pk_(self) -> str:
        for field in self.__fields__.values():
            if field.field_info.extra.get("pk"):
                key = getattr(self, field.name)
                if isinstance(key, Enum):
                    key = key.value
                return self.__class__.__name__ + "#" + str(key)
        raise ValueError("No partition key found")

    @property
    def sk_(self) -> str:
        keys: List[str] = []
        for field in self.__fields__.values():
            if field.field_info.extra.get("sk"):
                key = getattr(self, field.name)
                if isinstance(key, Enum):
                    key = key.value
                keys.append(str(key))
        if len(keys) == 0:
            raise ValueError("No sort key found")
        return "#".join(keys)

    def put(self: D) -> D:
        self.db.put(self)
        return self

    @classmethod
    def delete(cls: Type[D], pk: str, sk: str) -> None:
        prefix = cls.__name__ + "#"
        cls.db.delete(prefix + pk, sk)

    @classmethod
    def get(cls: Type[D], pk: str, sk: str) -> D:
        prefix = cls.__name__ + "#"
        data = cls.db.get(prefix + pk, sk)
        return cls(**data)

    @classmethod
    def query(
        cls: Type[D],
        pk: str,
        sk: Optional[str] = None,
        operator: Operator = "begins_with",
    ) -> List[D]:
        prefix = cls.__name__ + "#"
        data = cls.db.query(prefix + pk, sk, operator)
        return [cls(**item) for item in data]

    @classmethod
    def scan(cls: Type[D], **kwargs: Any) -> List[D]:
        data = cls.db.scan(**kwargs)
        return [cls(**item) for item in data]

    def __repr__(self) -> str:
        return self.json()

    def __str__(self) -> str:
        return self.json()

    @classmethod
    def __table_name__(cls) -> str:
        ents: List[str] = []
        for ent in cls.__subclasses__():
            ents.append(ent.__name__)
            ents.sort()
        return "-".join(ents)

    @classmethod
    def create_table(cls) -> str:
        try:
            table_name = cls.__table_name__()
            dynamodb.create_table(
                TableName=table_name,
                AttributeDefinitions=[
                    {"AttributeName": "pk", "AttributeType": "S"},
                    {"AttributeName": "sk", "AttributeType": "S"},
                ],
                KeySchema=[
                    {"AttributeName": "pk", "KeyType": "HASH"},
                    {"AttributeName": "sk", "KeyType": "RANGE"},
                ],
                BillingMode="PAY_PER_REQUEST",
                StreamSpecification={
                    "StreamEnabled": True,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
            )
            dynamodb.update_time_to_live(
                TableName=table_name,
                TimeToLiveSpecification={
                    "Enabled": True,
                    "AttributeName": "ttl",
                },
            )
            dynamodb.get_waiter("table_exists").wait(TableName=table_name)
            return f"Table {cls.__table_name__()} created successfully"
        except Exception as e:
            return f"Table {cls.__table_name__()} already exists"

    @classmethod
    def drop_table(cls) -> bool:
        try:
            dynamodb.delete_table(TableName=cls.__table_name__())
            dynamodb.get_waiter("table_not_exists").wait(TableName=cls.__table_name__())
            return True
        except Exception as e:
            return False
