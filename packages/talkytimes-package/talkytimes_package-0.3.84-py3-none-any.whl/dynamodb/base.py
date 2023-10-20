import abc
from functools import reduce
from typing import Any, Optional

import boto3
from boto3.dynamodb.conditions import And, Key, Attr

ITEMS_LIMIT = 1000


class AbstractDynamoDB(abc.ABC):
    def __init__(self, table: str):
        db = boto3.resource("dynamodb")
        self.table_name = table
        self.table = db.Table(self.table_name)

    def put_item(self, *, data: dict[str, Any]) -> None:
        self.table.put_item(Item=data)

    def get_item(self, *, key: dict[str, Any]) -> Optional[Any]:
        item = self.table.get_item(Key=key)
        item = item.get("Item", None)
        if isinstance(item, dict) and len(item) > 0:
            return item
        return None

    def get_all_items(self, **kwargs) -> Optional[Any]:
        key = reduce(
            And, ([Key(k).eq(v) for k, v in kwargs.items()])
        )
        query = dict(
            KeyConditionExpression=key,
            FilterExpression=Attr("customer_status").eq("online"),
            Limit=ITEMS_LIMIT
        )
        response = self.table.query(**query)
        items: list = response.get("Items", None)
        return items

    def get_all_items_with_category(self, **kwargs) -> Optional[Any]:
        key = reduce(
            And, ([Key(k).eq(v) for k, v in kwargs.items()])
        )
        query = dict(
            KeyConditionExpression=key,
            FilterExpression=Attr("customer_category").exists(),
            Limit=ITEMS_LIMIT
        )
        response = self.table.query(**query)
        items: list = response.get("Items", None)
        return items
