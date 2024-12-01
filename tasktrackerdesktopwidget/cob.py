import os
from datetime import datetime, time


# TODO: pick a random message from a configurable JSON file that contains a big list of different messages to show
# ... next to the COB timer when it's past COB. e.g. "Go home!", "Do some yoga!", "Drink some water!", "Water your
# ... plants!", "Walk your dog!", "Pick up your kids!", "Go watch Netflix!", "Go nap!", "Go make some art!", "Go
# ... call a friend!", "Geddoutta'ere!"
PAST_COB_MESSAGE = "go home!"


def get_time_until_cob_msg():
    # TODO: HACK: would rather not read this from env var every time we call this func - good enough for now
    cob_hour = int(os.environ['COB_TIMER_COB_HOUR'])
    cob_minute = int(os.environ['COB_TIMER_COB_MINUTE'])

    # Calculate the difference in time
    cob = datetime.combine(datetime.now().date(), time(cob_hour, cob_minute))
    time_difference = cob - datetime.now()

    # If the current time is already past 5 PM, calculate for the next day
    # if time_difference.total_seconds() < 0:
    #     cob = cob + timedelta(days=1)
    #     time_difference = cob - now

    # Calculate the number of hours left
    seconds_left = time_difference.total_seconds()
    hours_left = f"{seconds_left / 3600:01.1f}"
    text = (
        f"There are {hours_left} hours left until close of business ({cob_hour:02}:{cob_minute:02})"
        + f"{' ---- ' + PAST_COB_MESSAGE if seconds_left < 0 else ''}"
        + "\n"
    )

    return text
