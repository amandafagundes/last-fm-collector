from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, MapAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, ListAttribute
)

class Track(MapAttribute):
  id=UnicodeAttribute()
  name=UnicodeAttribute()
  album_id=UnicodeAttribute()
  album_name=UnicodeAttribute()
  artist_id=UnicodeAttribute()
  artist_name=UnicodeAttribute()
  duration=NumberAttribute()
  listeners=NumberAttribute()
  playback_date=UTCDateTimeAttribute()
  playcount=UTCDateTimeAttribute()
  reproduction=NumberAttribute()
  total_tracks=NumberAttribute()