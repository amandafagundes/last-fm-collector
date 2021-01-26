from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, MapAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, ListAttribute
)

class TrackMap(MapAttribute):
  id=UnicodeAttribute()
  name=UnicodeAttribute()
  album_id=UnicodeAttribute()
  album_name=UnicodeAttribute()
  artist_id=UnicodeAttribute()
  artist_name=UnicodeAttribute()
  duration=NumberAttribute()
  listeners=NumberAttribute()
  playback_date=UnicodeAttribute()
  playcount=UnicodeAttribute()
  reproduction=NumberAttribute()
  total_tracks=NumberAttribute()
  tags=ListAttribute()
  genres=ListAttribute()
  release_date= UnicodeAttribute()