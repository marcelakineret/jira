import requests

# JIRA API configuration
JIRA_URL = "https://your-jira-instance.com"
JIRA_USERNAME = "your-username"
JIRA_PASSWORD = "your-password"

def count_custom_fields_with_zero_use():
    # Fetch all custom fields
    custom_fields_url = f"{JIRA_URL}/rest/api/2/field"
    response = requests.get(custom_fields_url, auth=(JIRA_USERNAME, JIRA_PASSWORD))
    if response.status_code != 200:
        print("Failed to fetch custom fields:", response.text)
        return

    custom_fields = response.json()

    # Count custom fields with zero use
    count = 0
    for field in custom_fields:
        field_id = field["id"]

        # Query JQL to check if the field is used in any issues
        jql = f'"{field_id}" is not empty'
        search_url = f"{JIRA_URL}/rest/api/2/search"
        payload = {
            "jql": jql,
            "maxResults": 0
        }
        response = requests.post(search_url, json=payload, auth=(JIRA_USERNAME, JIRA_PASSWORD))
        if response.status_code != 200:
            print("Failed to execute search:", response.text)
            return

        total_issues = response.json()["total"]
        if total_issues == 0:
            count += 1
            print(f'Field "{field["name"]}" (ID: {field_id}) has zero usage.')

    print(f"Total custom fields with zero usage: {count}")


# Run the script
count_custom_fields_with_zero_use()
