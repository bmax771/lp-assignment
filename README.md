# lp-assignment - API processing

## Purpose

REST API functions extended to allow interacting with Harbor Registry API to List/Read projects, repositories and artifacts.

## Features
- The class BaseHarborApiClient should support
- GET, POST, PUT and DELETE requests for interacting with Harbor API.
- Use tenacity package for retrying failed requests 3 times while waiting 2 seconds between each request.
- Proper error handling for network issues, timeouts, and API errors
- A support for pagination in the GET request (if exists)
- A support for params in the GET requests (if exists)
- `Class ProjectApiClient`: Implement an asynchronous method for listing projects.
- `Class RepositoryApiClient`: Implement an asynchronous method for listing repositories within a project.
- `Class ArtifactApiClient`:
- - Implement an asynchronous method for listing artifacts within a given project and repository names.
- - Implement an asynchronous method for deleting tags older than 30 days in each artifact
- Use httpx and asyncio for making asynchronous requests

## File structure

- `main.py` - Main file to start execution from. Provides user input functionality.
- `src/base_api_client.py` - REST API library providing API functions for interacting with APIs.
- `src/artifact_api_client.py` - Library to read artifacts and delete tags older than specified days (default 30 days)
- `src/project_api_client.py` - Library to read projects from Harbor registry.
- `src/repository_api_client.py` - Library to read all authorized repositories or repositories belonging to a project
- `src/constants.py` - Initializing constants to be used in main.py
- `.env` - File containing credentials to connect to Harbor Registry.

## Classes and Functions

1. `[parent]` `BaseHarborApiClient`: Base class with common methods for making HTTP requests to the Harbor registry API.
2. `[child]` `ProjectApiClient`: Inherits from BaseHarborApiClient and adds method for listing available projects.
3. `[child]` `RepositoryApiClient`: Inherits from BaseHarborApiClient and adds method for listing repositories in given project.
4. `[child]` `ArtifactApiClient`: Inherits from BaseHarborApiClient and adds methods for:
   1. Listing available artifacts in given project and repository. 
   2. Deleting tags that pushed more than 30 days to each artifact.

### `src/base_api_client.py` in `BaseHarborApiClient`

- `harbor_get()` [async] - GET REST API function to perform get call on Harbor Registry.
- `harbor_post()` [async] - POST REST API function to perform post call on Harbor Registry.
- `harbor_delete()` [async] - DELETE REST API function to perform delete call on Harbor Registry.
- `harbor_paginated_get()` [async] - GET REST API function to perform recursive get call on Harbor Registry for fetching pages.

### `src/artifact_api_client.py` in `ArtifactApiClient`

- `get_artifacts()` [async] - Gets list of artifacts for a given project and repository.
- `delete_artifact_tag()` [async] - Deletes tags older than specified number of days.

### `src/project_api_client.py` in `ProjectApiClient`

- `get_projects()` [async] - Gets list of projects for a user.

### `src/repository_api_client.py` in `RepositoryApiClient`

- `get_all_authorized_repos()` [async] - Gets list of repositories that user can see.
- `get_specific_project_repos()` [async] - Gets list of repositories for specified project.

## Samples from requests

- Getting inputs:
  - from `main.py`:
    ```bash
    ### Application start. ###Please enter action to perform on Harbor API interface using following options.
    1) list_project: To list projects.
    2) all_repos: To list repos.
    3) project_repos: To list repos.
    4) artifacts: To list artifacts inside the project.
    5) delete: To delete tags that are older than specified days (Default value is 30 days).
    6) exit: To exit the program
    
    Please enter your choice: |
    ```
- Getting project list:
  - from `main.py` -> calls -> `get_projects()` -> calls -> `harbor_paginated_get()` -> calls -> `harbor_get()`
  - ```bash
    Please enter your choice: list_project
    Please enter the project name: 
    [OPTIONAL] Please enter an integer value of number of items per page (default = 100): 1
    [OPTIONAL] Please enter the name of the owner of project: 
    [OPTIONAL] Please enter if project is public or not (true/false/leave blank): 
    [OPTIONAL] Please enter if you want detailed output (true/false/leave blank): 
    OUTPUT:
    [
        {
            "creation_time": "2024-03-17T05:00:19.545Z",
            "current_user_role_ids": null,
            "cve_allowlist": {
                "creation_time": "0001-01-01T00:00:00.000Z",
                "id": 1,
                "items": [],
                "project_id": 1,
                "update_time": "0001-01-01T00:00:00.000Z"
            },
            "metadata": {
                "public": "true"
            },
            "name": "library",
            "owner_id": 1,
            "owner_name": "admin",
            "project_id": 1,
            "repo_count": 0,
            "update_time": "2024-03-17T05:00:19.545Z"
        }
    ]
    ```
    
- Getting repository list:
  - from `main.py` -> calls -> `get_specific_project_repos()` -> calls -> `harbor_paginated_get()` -> calls -> `harbor_get()`
  - ```bash
    ### Application start. ###Please enter action to perform on Harbor API interface using following options.
     1) list_project: To list projects.
     2) all_repos: To list repos.
     3) project_repos: To list repos.
     4) artifacts: To list artifacts inside the project.
     5) delete: To delete tags that are older than specified days (Default value is 30 days).
     6) exit: To exit the program

    Please enter your choice: project_repos
    Please enter the project name: usr
    [OPTIONAL] Please enter an integer value of number of items per page (default = 100): 
    OUTPUT:
    [
        {
            "artifact_count": 1,
            "creation_time": "2024-03-17T05:45:19.709Z",
            "id": 2,
            "name": "usr/ubuntu-1",
            "project_id": 3,
            "pull_count": 0,
            "update_time": "2024-03-17T05:45:19.709Z"
        },
        {
            "artifact_count": 1,
            "creation_time": "2024-03-17T05:44:13.328Z",
            "id": 1,
            "name": "usr/wordpress-2",
            "project_id": 3,
            "pull_count": 0,
            "update_time": "2024-03-17T05:44:13.328Z"
        }
    ]
    ```
    
  - from `main.py` -> calls -> `get_all_authorized_repos()` -> calls -> `harbor_paginated_get()` -> calls -> `harbor_get()`
  - ```bash
    ### Application start. ###Please enter action to perform on Harbor API interface using following options.
    1) list_project: To list projects.
    2) all_repos: To list repos.
    3) project_repos: To list repos.
    4) artifacts: To list artifacts inside the project.
    5) delete: To delete tags that are older than specified days (Default value is 30 days).
    6) exit: To exit the program

    Please enter your choice: all_repos
    [OPTIONAL] Please enter an integer value of number of items per page (default = 100): 2
    OUTPUT:
    [
        {
            "artifact_count": 1,
            "creation_time": "2024-03-17T05:49:16.191Z",
            "id": 7,
            "name": "usr/maven-2",
            "project_id": 3,
            "pull_count": 0,
            "update_time": "2024-03-17T05:49:16.191Z"
        },
        {
            "artifact_count": 1,
            "creation_time": "2024-03-17T05:48:49.463Z",
            "id": 6,
            "name": "usr/maven-1",
            "project_id": 3,
            "pull_count": 0,
            "update_time": "2024-03-17T05:48:49.463Z"
        },
        {
            "artifact_count": 1,
            "creation_time": "2024-03-17T05:47:46.069Z",
            "id": 5,
            "name": "usr/ruby-4",
            "project_id": 3,
            "pull_count": 0,
            "update_time": "2024-03-17T05:47:46.069Z"
        },
        {
            "artifact_count": 1,
            "creation_time": "2024-03-17T05:47:17.959Z",
            "id": 4,
            "name": "usr/ruby-3",
            "project_id": 3,
            "pull_count": 0,
            "update_time": "2024-03-17T05:47:17.959Z"
        },
        {
            "artifact_count": 1,
            "creation_time": "2024-03-17T05:45:54.496Z",
            "id": 3,
            "name": "usr/ruby-1",
            "project_id": 3,
            "pull_count": 0,
            "update_time": "2024-03-17T05:45:54.496Z"
        },
        {
            "artifact_count": 1,
            "creation_time": "2024-03-17T05:45:19.709Z",
            "id": 2,
            "name": "usr/ubuntu-1",
            "project_id": 3,
            "pull_count": 0,
            "update_time": "2024-03-17T05:45:19.709Z"
        },
        {
            "artifact_count": 1,
            "creation_time": "2024-03-17T05:44:13.328Z",
            "id": 1,
            "name": "usr/wordpress-2",
            "project_id": 3,
            "pull_count": 0,
            "update_time": "2024-03-17T05:44:13.328Z"
        }
    ]
    ```
    
  - Getting artifacts from a project and repository:
    - from `main.py` -> calls -> `get_artifacts()` -> calls -> `harbor_paginated_get()` -> calls -> `harbor_get()`
    ```bash
    ### Application start. ###Please enter action to perform on Harbor API interface using following options.
    1) list_project: To list projects.
    2) all_repos: To list repos.
    3) project_repos: To list repos.
    4) artifacts: To list artifacts inside the project.
    5) delete: To delete tags that are older than specified days (Default value is 30 days).
    6) exit: To exit the program

    Please enter your choice: artifacts
    Please enter the project name where the artifact resides: usr
    Please enter the repository name where the artifact resides: maven-4
    [OPTIONAL] Please enter an integer value of number of items per page (default = 100): 2
    OUTPUT:
    [
        {
            "accessories": null,
            "addition_links": {
                "build_history": {
                    "absolute": false,
                    "href": "/api/v2.0/projects/usr/repositories/maven-4/artifacts/sha256:22a8fc6284b823ddc0382bebd69c85a72f3ae0d057f6c6bd89c8b3edb279c2bd/additions/build_history"
                },
                "vulnerabilities": {
                    "absolute": false,
                    "href": "/api/v2.0/projects/usr/repositories/maven-4/artifacts/sha256:22a8fc6284b823ddc0382bebd69c85a72f3ae0d057f6c6bd89c8b3edb279c2bd/additions/vulnerabilities"
                }
            },
            "digest": "sha256:22a8fc6284b823ddc0382bebd69c85a72f3ae0d057f6c6bd89c8b3edb279c2bd",
            "extra_attrs": {
                "architecture": "amd64",
                "author": "jhon doe",
                "config": {
                    "ArgsEscaped": true,
                    "Cmd": [
                        "/bin/bash"
                    ],
                    "Env": [
                        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                        "DEBIAN_FRONTEND=noninteractive",
                        "LANG=en_US.UTF-8",
                        "LANGUAGE=en_US:en",
                        "LC_ALL=en_US.UTF-8",
                        "JAVA_VERSION=7"
                    ]
                },
                "created": "2024-03-12T11:08:36.088101689Z",
                "os": "linux"
            },
            "icon": "sha256:0048162a053eef4d4ce3fe7518615bef084403614f8bca43b40ae2e762e11e06",
            "id": 9,
            "labels": null,
            "manifest_media_type": "application/vnd.docker.distribution.manifest.v2+json",
            "media_type": "application/vnd.docker.container.image.v1+json",
            "project_id": 3,
            "pull_time": "0001-01-01T00:00:00.000Z",
            "push_time": "2024-03-17T05:50:12.971Z",
            "references": null,
            "repository_id": 9,
            "size": 344582380,
            "tags": [
                {
                    "artifact_id": 9,
                    "id": 9,
                    "immutable": false,
                    "name": "latest",
                    "pull_time": "0001-01-01T00:00:00.000Z",
                    "push_time": "2024-03-17T05:50:12.988Z",
                    "repository_id": 9
                }
            ],
            "type": "IMAGE"
        }
    ]
    ```
  - from `main.py` -> calls -> `delete_artifact_tag()` -> calls -> `harbor_delete()`
  ```bash
  ### Application start. ###Please enter action to perform on Harbor API interface using following options.
  1) list_project: To list projects.
  2) all_repos: To list repos.
  3) project_repos: To list repos.
  4) artifacts: To list artifacts inside the project.
  5) delete: To delete tags that are older than specified days (Default value is 30 days).
  6) exit: To exit the program

    Please enter your choice: delete
    Please enter the project name where the artifact resides: usr
    Please enter the repository name where the artifact resides: maven-4
    [OPTIONAL] Please enter an integer value of number of items per page (default = 100): 2
    [OPTIONAL] Please enter the number of days old tag that should be deleted (enter integer value): 0
    OUTPUT:
    ['Deleting tag: newTag-2', <Response [200 OK]>, 'Deleting tag: newTag-1', <Response [200 OK]>, 'Deleting tag: newTag', <Response [200 OK]>, 'Deleting tag: latest', <Response [200 OK]>]
  ```
