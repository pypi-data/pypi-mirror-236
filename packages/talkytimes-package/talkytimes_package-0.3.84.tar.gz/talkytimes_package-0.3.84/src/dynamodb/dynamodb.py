import uuid
from datetime import datetime, timedelta
from typing import Any, Optional

import pytz

from dynamodb.base import AbstractDynamoDB

COLOMBIA_TZ = pytz.timezone('America/Bogota')


class DynamoDB(AbstractDynamoDB):
    def get_user(self, *, external_id: str, profile_id: str) -> Any:
        data = {"external_id": external_id, "profile_id": profile_id}
        return self.get_item(key=data)

    def get_users(self, profile_id: str) -> dict[str, Any]:
        return self.get_all_items(profile_id=profile_id)

    def get_customers_with_category(self, profile_id: str) -> dict[str, Any]:
        return self.get_all_items_with_category(profile_id=profile_id)

    def create_user(
        self,
        *,
        profile_id: str,
        profile_name: str,
        external_id: str,
        customer_status: str,
    ) -> Any:
        created_at = datetime.now(COLOMBIA_TZ).isoformat()
        data = dict(
            id=str(uuid.uuid4()),
            external_id=external_id,
            profile_id=profile_id,
            profile_name=profile_name,
            created_at=created_at,
            updated_at=created_at,
            ttl=int((datetime.now() + timedelta(days=7)).timestamp()),
            customer_status=customer_status
        )
        self.put_item(data=data)

    def update_user(
        self,
        *,
        profile_id: str,
        external_id: str,
        item: dict[str, Any]
    ) -> None:
        fields = list(map(lambda item: f"{item[0]}=:{item[0]}", item.items()))
        values = dict(map(lambda item: (f":{item[0]}", item[1]), item.items()))
        fields = ", ".join(fields)
        self.table.update_item(
            Key={"external_id": external_id, "profile_id": profile_id},
            UpdateExpression=f"set {fields}",
            ExpressionAttributeValues=values,
            ReturnValues="UPDATED_NEW",
        )

    def create_or_update(
        self,
        *,
        profile_id: str,
        profile_name: str,
        external_id: str,
        status: bool,
        messages: Optional[str] = None,
        emails: Optional[str] = None
    ):
        user = self.get_user(external_id=external_id, profile_id=profile_id)
        status = 'online' if status else 'offline'
        if not user:
            self.create_user(
                external_id=external_id,
                profile_id=profile_id,
                profile_name=profile_name,
                customer_status=status
            )
        else:
            self.update_user(
                profile_id=profile_id,
                external_id=external_id,
                item=dict(
                    customer_status=status,
                    messages=messages,
                    emails=emails,
                    updated_at=datetime.now(COLOMBIA_TZ).isoformat()
                )
            )
