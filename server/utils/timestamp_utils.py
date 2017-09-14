import pytz
from datetime import datetime, timedelta


# Global variables
epoch = datetime.utcfromtimestamp(0)


class TimestampUtils:

  @classmethod
  def getCurrentMillisecond(sefl):
    now = datetime.utcnow()
    delta = now - epoch
    return int(delta.total_seconds())

  @classmethod
  def getVietNamCurrentHour(sefl):
    tz = pytz.timezone('Asia/Saigon')
    vietnam_now = datetime.now(tz)
    return int(vietnam_now.hour)

  @classmethod
  def getVietnamCurrentMinute(sefl):
    tz = pytz.timezone('Asia/Saigon')
    vietnam_now = datetime.now(tz)
    return int(vietnam_now.minute)