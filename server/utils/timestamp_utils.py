from datetime import datetime, timedelta


# Global variables
epoch = datetime.utcfromtimestamp(0)


class TimestampUtils:

  @classmethod
  def getCurrentMillisecond(sefl):
    now = datetime.utcnow()
    delta = now - epoch
    return int(delta.total_seconds())