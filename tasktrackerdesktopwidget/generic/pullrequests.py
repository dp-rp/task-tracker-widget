import os
from ..ado.pullrequests import get_ado_pull_requests
import urllib

REMOTE_TYPE_ENVVAR_KEY = "TTW_REMOTE_TYPE"

# ---------------------------------------------------
# TODO: adapt below to be relevant to pull requests
# ---------------------------------------------------


def get_ado_generic(ado_pull_request):
    team_name_url_encoded = urllib.parse.quote(os.environ["SECRET_ADO_TEAM_NAME"])
    iteration_path_for_url = ado_pull_request.fields["System.IterationPath"].replace(
        "\\", "/"
    )
    org_url = os.environ["SECRET_ADO_ORGANIZATION_URL"]
    hours_elapsed_field_name = os.environ["SECRET_ADO_HOURS_ELAPSED_FIELD_NAME"]
    return {
        "uid": ado_pull_request.id,
        "title": ado_pull_request.fields["System.Title"],
        "assigned_to": {
            "unique_name": ado_pull_request.fields["System.AssignedTo"]["uniqueName"]
        },
        "pull_request_web_browser_link": f"{org_url}/{ado_pull_request.fields['System.TeamProject']}/_sprints/backlog/{team_name_url_encoded}/{iteration_path_for_url}?workitem={ado_pull_request.id}",
        "hours_elapsed": ado_pull_request.fields[hours_elapsed_field_name],
    }


def get_generic_pull_requests():
    _remote_type = os.getenv(REMOTE_TYPE_ENVVAR_KEY)

    # TODO: make this look at a different env var, or an env var that's not specific to work item or pull requests, but if do the latter, then allow it to be overridden with a different env var ideally so that people can mix and match (they might use Trello or something for tickets, but GitLab or Azure Devops for PRs)
    if _remote_type == "ado-work-item":
        return [
            get_ado_generic(ado_pull_request)
            for ado_pull_request in get_ado_pull_requests()
        ]
    else:
        raise Exception(f"{REMOTE_TYPE_ENVVAR_KEY} isn't a supported value")
