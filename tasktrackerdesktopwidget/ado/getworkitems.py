from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import Wiql
import os

# TODO: add typehints
def get_ado_work_items():
    # TODO: schema validation

    # get sensitive config
    personal_access_token = os.environ['ADO_PERSONAL_ACCESS_TOKEN']
    organization_url = os.environ['ADO_ORGANIZATION_URL']

    # Create a connection to the org
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)

    # Get a client (the "core" client provides access to projects, teams, etc)
    core_client = connection.clients.get_core_client()

    #query workitems, custom field 'RTCID' has a certain specific unique value
    work_item_tracking_client = connection.clients.get_work_item_tracking_client()
    query  = "SELECT [System.Id], [System.WorkItemType], [System.Title], [System.AssignedTo], [System.State], [System.Tags] FROM workitems WHERE [System.State] = 'In Progress' AND [System.AssignedTo] = @me"
    #convert query str to wiql
    wiql = Wiql(query=query)
    query_results = work_item_tracking_client.query_by_wiql(wiql).work_items
    #get the results via title
    work_items = []
    for item in query_results:
        work_items.append(work_item_tracking_client.get_work_item(item.id))
    return work_items
