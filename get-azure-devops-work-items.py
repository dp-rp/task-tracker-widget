#query workitems from azure devops

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import Wiql
import pprint


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
for item in query_results:
    work_item = work_item_tracking_client.get_work_item(item.id)
    print("-------")
    # print(work_item.__str__())
    # pprint.pprint(work_item.fields['System.Title'])
    print(f"{work_item.id}: {work_item.fields['System.Title']}")
    
    if 'System.AssignedTo' in work_item.fields:
        print(work_item.fields['System.AssignedTo']['uniqueName'])

# TODO: get the output (my in-progress work items) and make it display in a small movable, resizable window that's always-on-top that updates once every 5-10 minutes
# ... (and it should also go invisible for a couple seconds when moused over, just like how I have ElevenClock configured)
