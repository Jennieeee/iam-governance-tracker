import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def scan_gcp_iam():
    findings = []
    project_id = os.environ.get("GCP_PROJECT_ID")

    creds = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )

    service = build('cloudresourcemanager', 'v1', credentials=creds)
    policy = service.projects().getIamPolicy(resource=project_id, body={}).execute()

    bindings = policy.get("bindings", [])

    for binding in bindings:
        role = binding["role"].lower()
        if any(term in role for term in ["admin", "owner", "editor"]):
            findings.append({
                "role": role,
                "members": binding["members"],
                "issue": "Over-permissive GCP IAM role"
            })

    return {"gcp": findings}
