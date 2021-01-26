from pynamodb.models import Model
from models.track_map import TrackMap
from pynamodb.attributes import (NumberAttribute, ListAttribute, MapAttribute)

class ReproductionMap(MapAttribute):
    reproduction = NumberAttribute()
    tracks = ListAttribute(of=TrackMap)
