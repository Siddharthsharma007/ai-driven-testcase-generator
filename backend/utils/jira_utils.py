import requests

def send_cases_to_jira(cases, jira_url, api_token, project_key):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    # This is a sample payload for Jira Xray import
    payload = {
        "tests": cases,
        "projectKey": project_key
    }
    response = requests.post(jira_url, json=payload, headers=headers)
    return {"status": response.status_code, "response": response.text} 