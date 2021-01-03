import os
from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute,ListAttribute)
from models.track import Track

class Reproduction(Model):
  class Meta:
    table_name = os.environ['DYNAMODB_TABLE']

  user_id = UnicodeAttribute(hash_key=True)
  reproduction = NumberAttribute(range_key=True)
  created_at = UTCDateTimeAttribute(default=datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'))
  tracks = employees = ListAttribute(of=Track)