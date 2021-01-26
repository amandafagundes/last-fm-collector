from pynamodb.indexes import (LocalSecondaryIndex, AllProjection)
from pynamodb.attributes import (UnicodeAttribute)

class DateIndex(LocalSecondaryIndex):
    class Meta:
        projection = AllProjection()
    user_id = UnicodeAttribute(hash_key=True)
    date = UnicodeAttribute(range_key=True)