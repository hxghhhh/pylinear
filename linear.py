import click
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# reference: https://click.palletsprojects.com/en/7.x/quickstart/#echoing
@click.group()
def cli():
    """An example application that supports aliases."""
    pass

@cli.command()
def get_issue_branches():
    sample_transport=RequestsHTTPTransport(
        url='https://api.linear.app/graphql',
        use_json=True,
        headers={
            "Content-type": "application/json",
            "Authorization": "V4HEChjkzfY0kCWIQolWmiY2XS220M2FhCU1NFzm"
        },
        verify=False
    )

    client = Client(
        retries=3,
        transport=sample_transport,
        fetch_schema_from_transport=True,
    )

    query = gql('''
        query { 
            teams { nodes { key } } 
            organization { gitBranchFormat } 
            viewer {
                id
                name
                email
                assignedIssues (first: 10) { nodes { title number previousIdentifiers } } 
            }
        }
    ''')

    # Get format
    data = client.execute(query)
    branch_format = data.get('organization').get('gitBranchFormat')
    team_key = data.get('teams').get('nodes')[0].get('key')
    print(data)
    print(branch_format)
    
    # Build issueIdentifier
    for issue in data.get('viewer').get('assignedIssues').get('nodes'):
        title = issue.get('title').replace(' ', '-').replace('/', '')
        number = issue.get('number')
        print(f'{team_key}-{number}-{title}'.lower())

    # Build issueTitle
    #branch_format.format()
    

    # print(client.execute(query))

if __name__ == '__main__':
    cli()