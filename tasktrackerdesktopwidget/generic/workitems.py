import os
from ..ado.workitems import get_ado_work_items
import urllib

REMOTE_TYPE_ENVVAR_KEY = "TTW_REMOTE_TYPE"


def get_ado_generic(ado_work_item):
    team_name_url_encoded = urllib.parse.quote(os.environ["SECRET_ADO_TEAM_NAME"])
    iteration_path_for_url = ado_work_item.fields["System.IterationPath"].replace(
        "\\", "/"
    )
    org_url = os.environ["SECRET_ADO_ORGANIZATION_URL"]
    return {
        "uid": ado_work_item.id,
        "title": ado_work_item.fields["System.Title"],
        "assigned_to": {
            "unique_name": ado_work_item.fields["System.AssignedTo"]["uniqueName"]
        },
        "work_item_web_browser_link": f"{org_url}/{ado_work_item.fields['System.TeamProject']}/_sprints/backlog/{team_name_url_encoded}/{iteration_path_for_url}?workitem={ado_work_item.id}",
    }


def get_generic_work_items():
    _remote_type = os.getenv(REMOTE_TYPE_ENVVAR_KEY)

    if _remote_type == "ado-work-item":
        return [
            get_ado_generic(ado_work_item) for ado_work_item in get_ado_work_items()
        ]
    else:
        raise Exception(f"{REMOTE_TYPE_ENVVAR_KEY} isn't a supported value")
