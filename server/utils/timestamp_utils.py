import pytz
from datetime import datetime, timedelta


# Global variables
epoch = datetime.utcfromtimestamp(0)


class TimestampUtils:

  @classmethod
  def getCurrentMillisecond(self):
    now = datetime.utcnow()
    delta = now - epoch
    return int(delta.total_seconds())

  @classmethod
  def getVietNamCurrentHour(self):
    tz = pytz.timezone('Asia/Saigon')
    vietnam_now = datetime.now(tz)
    return int(vietnam_now.hour)

  @classmethod
  def getVietnamCurrentMinute(self):
    tz = pytz.timezone('Asia/Saigon')
    vietnam_now = datetime.now(tz)
    return int(vietnam_now.minute)

  @classmethod
  def getCurrentDatetime(self):
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

  @classmethod
  def getDateFromDatetime(self, datetime):
    return datetime.strftime("%d-%m-%Y")