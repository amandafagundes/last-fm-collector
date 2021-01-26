import os
from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, MapAttribute,ListAttribute)
from models.reproduction import Reproduction
from models.base_model import BaseModel

class ItemModel(BaseModel):
    class Meta:
        table_name = os.environ['DYNAMODB_TABLE']

    user_id = UnicodeAttribute(hash_key=True)
    date = UnicodeAttribute(range_key=True)
    date_count = NumberAttribute(default=0)
    created_at = UnicodeAttribute(default=datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'))
    reproductions = ListAttribute(of=Reproduction)
    user = MapAttribute()
