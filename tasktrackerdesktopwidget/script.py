import pprint
from dotenv import load_dotenv
from .generic.workitems import get_generic_work_items

def main():
    load_dotenv()  # take environment variables
    
    work_items = get_generic_work_items()
        
    # TODO: remove later - for debugging and testing
    for work_item in work_items:
        print("-------")
        print(f"{work_item['uid']}: {work_item['title']}")
        if 'assigned_to' in work_item: print(work_item['assigned_to']['unique_name'])

    # TODO: get the output (my in-progress work items) and make it display in a small movable, resizable window that's always-on-top that updates once every 5-10 minutes
    # ... (and it should also go invisible for a couple seconds when moused over, just like how I have ElevenClock configured)
