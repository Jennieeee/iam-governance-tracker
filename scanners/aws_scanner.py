import boto3

def scan_aws_iam():
    client = boto3.client('iam')
    roles = client.list_roles()['Roles']
    findings = []

    for role in roles:
        if "AdministratorAccess" in str(role):
            findings.append({"role": role["RoleName"], "issue": "Has admin access"})
    
    return {"aws": findings}
