import os
import inquirer
import click
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# reference: https://click.palletsprojects.com/en/7.x/quickstart/#echoing
@click.group()
def cli():
    """A python cli tool to interface with linear.app instance"""
    pass


@cli.command()
def get_issue_branches():
    sample_transport = RequestsHTTPTransport(
        url="https://api.linear.app/graphql",
        use_json=True,
        headers={
            "Content-type": "application/json",
            "Authorization": "V4HEChjkzfY0kCWIQolWmiY2XS220M2FhCU1NFzm",
        },
        verify=False,
    )

    client = Client(
        retries=3, transport=sample_transport, fetch_schema_from_transport=True,
    )

    query = gql(
        """
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
    """
    )

    # Get format
    data = client.execute(query)
    branch_format = data.get("organization").get("gitBranchFormat")
    team_key = data.get("teams").get("nodes")[0].get("key")

    # Build issueIdentifier
    issues = []
    for issue in data.get("viewer").get("assignedIssues").get("nodes"):
        title = issue.get("title").replace(" ", "-").replace("/", "")
        number = issue.get("number")
        issues.append(f"{team_key}-{number}-{title}".lower())
    
    questions = [
        inquirer.List(
            "issue",
            message="What task are you working on?",
            choices=issues,
        ),
    ]


    answers = inquirer.prompt(questions)
    issue_selected = answers.get('issue')

    # Create this branch
    os.system(f"git checkout -b {issue_selected}")
    
    # Sync with gh
    os.system(f"gh pr create {issue_selected}")

# Build issueTitle
# branch_format.format()

# print(client.execute(query))

if __name__ == "__main__":
    cli()
