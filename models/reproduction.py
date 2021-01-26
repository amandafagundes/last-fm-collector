from pynamodb.models import Model
from models.track import Track
from pynamodb.attributes import (NumberAttribute, ListAttribute, MapAttribute)

class Reproduction(MapAttribute):
    reproduction = NumberAttribute()
    tracks = ListAttribute(of=Track)
