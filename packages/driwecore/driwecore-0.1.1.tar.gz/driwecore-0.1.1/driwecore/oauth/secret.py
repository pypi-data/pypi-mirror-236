import json
from google.cloud import secretmanager


# This function will return a list with 2 values, first is the latest token secret, and
# the second latest token secret
def get_token_secret():
    project_id = 'dri-be-101' # to change this to variable
    secret_title = 'oauth-settings' # to change this to variable

    secret_name = f"projects/{project_id}/secrets/{secret_title}"

    client = secretmanager.SecretManagerServiceClient()

    versions = list(client.list_secret_versions(
        request={"parent": secret_name}))

    sorted_versions = sorted(
        versions, key=lambda x: x.create_time, reverse=True)

    version_list = []

    for version in sorted_versions:
        if version.state == 1:
            if len(version_list) == 0:
                version_list.append(version.name.split("/")[-1])
            elif len(version_list) == 1:
                version_list.append(version.name.split("/")[-1])
                break

    token_secret_list = []

    for version in version_list:
        response = client.access_secret_version(
            request={"name": f"{secret_name}/versions/{version}"})

        secret_data = response.payload.data.decode("UTF-8")

        lines = secret_data.split('\n')

        for line in lines:
            if line.startswith('TOKEN_SECRET='):
                token_secret_list.append(line[len('TOKEN_SECRET='):])

    return token_secret_list
