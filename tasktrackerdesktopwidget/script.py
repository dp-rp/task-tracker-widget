import pprint
from dotenv import load_dotenv
import os
from .ado.getworkitems import get_ado_work_items

remote_type_envvar_key = "TTW_REMOTE_TYPE"

def main():
    load_dotenv()  # take environment variables

    _remote_type = os.getenv(remote_type_envvar_key)

    if _remote_type == "ado-work-item":
        ado_work_items = get_ado_work_items()
        
        # TODO: remove later - for debugging and testing
        for work_item in ado_work_items:
            print("-------")
            # print(work_item.__str__())
            # pprint.pprint(work_item.fields['System.Title'])
            print(f"{work_item.id}: {work_item.fields['System.Title']}")
            
            if 'System.AssignedTo' in work_item.fields:
                print(work_item.fields['System.AssignedTo']['uniqueName'])

        # TODO: get the output (my in-progress work items) and make it display in a small movable, resizable window that's always-on-top that updates once every 5-10 minutes
        # ... (and it should also go invisible for a couple seconds when moused over, just like how I have ElevenClock configured)
    else:
        raise Exception(f"{remote_type_envvar_key} isn't a supported value")
