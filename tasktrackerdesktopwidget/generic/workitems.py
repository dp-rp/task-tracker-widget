import os
from ..ado.workitems import get_ado_work_items

REMOTE_TYPE_ENVVAR_KEY = "TTW_REMOTE_TYPE"

def get_generic_work_items():
    _remote_type = os.getenv(REMOTE_TYPE_ENVVAR_KEY)

    if _remote_type == "ado-work-item":
        return [
            {
                "uid": ado_work_item.id,
                "title": ado_work_item.fields['System.Title'],
                "assigned_to": {
                    "unique_name": ado_work_item.fields['System.AssignedTo']['uniqueName']
                }
            }
            for ado_work_item
            in get_ado_work_items()
        ]
    else:
        raise Exception(f"{REMOTE_TYPE_ENVVAR_KEY} isn't a supported value")
