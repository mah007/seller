from runners.price_automatically_runner import PriceAutomaticallyRunner
from config import RunnerConfig


if __name__ == "__main__":
    interval = PriceAutomaticallyRunner(RunnerConfig.TIME_INTEVAL)
    # try:
    #   sleep(RunnerConfig.TIME_INTEVAL + 1)
    # finally:
    #   interval.stop()
