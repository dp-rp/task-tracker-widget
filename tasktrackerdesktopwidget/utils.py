import yaml
import random

# HACK: this path will likely break if the package is installed and will definitely break if not run from the right directory
with open("tasktrackerdesktopwidget/config/messages.yaml") as stream:
    try:
        messages = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("YAML error!")
        print(exc)

def get_random_past_cob_message():
    return random.choice(messages["close_of_business"])
