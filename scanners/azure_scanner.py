import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

def scan_azure_iam():
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    credential = DefaultAzureCredential()
    client = AuthorizationManagementClient(credential, subscription_id)

    findings = []

    assignments = client.role_assignments.list()

    for assignment in assignments:
        role = client.role_definitions.get(
            scope=assignment.scope,
            role_definition_id=assignment.role_definition_id.split("/")[-1]
        )
        if any(term in role.role_name.lower() for term in ["owner", "contributor", "admin"]):
            findings.append({
                "role": role.role_name,
                "assignee": assignment.principal_id,
                "scope": assignment.scope,
                "issue": "Over-permissive role assigned"
            })

    return {"azure": findings}
