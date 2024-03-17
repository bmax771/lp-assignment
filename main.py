from os import getenv
from dotenv import load_dotenv
from src.constants import ENVPATH

from src.artifact_api_client import ArtifactApiClient
from src.project_api_client import ProjectApiClient
from src.repository_api_client import RepositoryApiClient

from anyio import run


def input_processing(input_choice: str) -> list:
    if input_choice in ["artifacts", "delete"]:
        project_name = input("Please enter the project name where the artifact resides: ")
        repo_name = input("Please enter the repository name where the artifact resides: ")
        page_size = input("[OPTIONAL] Please enter an integer value of number of items per page (default = 100): ")
        return_list = [input_choice, str(page_size), str(project_name), str(repo_name)]
        if input_choice == "delete":
            days_threshold_for_deletion = input(
                "[OPTIONAL] Please enter the number of days old tag that should be deleted (enter integer value): ")
            return_list.append(days_threshold_for_deletion)
        return return_list

    if input_choice == "project_repos":
        project_name = input("Please enter the project name: ")
        page_size = input("[OPTIONAL] Please enter an integer value of number of items per page (default = 100): ")
        return [input_choice, str(page_size), str(project_name)]

    if input_choice == "list_project":
        project_name = input("Please enter the project name: ")
        page_size = input("[OPTIONAL] Please enter an integer value of number of items per page (default = 100): ")
        name_of_owner = input("[OPTIONAL] Please enter the name of the owner of project: ")
        is_public = input("[OPTIONAL] Please enter if project is public or not (true/false/leave blank): ")
        with_details = input("[OPTIONAL] Please enter if you want detailed output (true/false/leave blank): ")
        return [input_choice, str(page_size), str(project_name), str(name_of_owner), str(is_public).lower(),
                str(with_details).lower()]

    if input_choice == "all_repos":
        page_size = input("[OPTIONAL] Please enter an integer value of number of items per page (default = 100): ")
        return [input_choice, str(page_size)]


async def input_execution(inputs: list):
    print(f"OUTPUT:")
    if inputs[0] == "artifacts":
        if inputs[2] != "" and inputs[3] != "":

            url_string = (getenv("HARBOR_API_URL") + "/projects/" + inputs[2] + "/repositories/"
                          + inputs[3] + "/artifacts?page=1")
            if inputs[1]:
                url_string += f"&page_size={inputs[1]}"
            else:
                url_string += f"&page_size=100"

            artifact_object = ArtifactApiClient((getenv("HARBOR_USERNAME"), getenv("HARBOR_PASSWORD")))
            response = await artifact_object.get_artifacts(api_url=url_string)
            return response
        else:
            return "Please enter project name and repository name."

    if inputs[0] == "delete":

        if inputs[2] != "" and inputs[3] != "":
            url_string = (getenv("HARBOR_API_URL") + "/projects/" + inputs[2] + "/repositories/"
                          + inputs[3] + "/artifacts?page=1")
            if inputs[1]:
                url_string += f"&page_size={inputs[1]}"
            else:
                url_string += f"&page_size=100"
            days_threshold_for_deletion = None
            if inputs[4]:
                try:
                    days_threshold_for_deletion = int(inputs[4])
                    if days_threshold_for_deletion < 0:
                        raise ValueError
                except ValueError:
                    return "Please enter valid number of days as integer number."
            artifact_object = ArtifactApiClient((getenv("HARBOR_USERNAME"), getenv("HARBOR_PASSWORD")))
            response = await artifact_object.delete_artifact_tag(api_url=url_string,
                                                             days_threshold_for_deletion=days_threshold_for_deletion)
            return response
        else:
            return "Please enter project name and repository name."

    if inputs[0] == "list_project":
        url_string = getenv("HARBOR_API_URL") + "/projects?page=1"
        if inputs[1]:
            url_string += f"&page_size={inputs[1]}"
        else:
            url_string += f"&page_size=100"
        if inputs[2]:
            url_string += f"&name={inputs[2]}"
        if inputs[3]:
            url_string += f"&owner={inputs[3]}"
        if inputs[4] and inputs[4] in ["true", "false"]:
            url_string += f"&public={inputs[4]}"
        if inputs[5] and inputs[5] in ["true", "false"]:
            url_string += f"&with_detail={inputs[5]}"
        projects_object = ProjectApiClient((getenv("HARBOR_USERNAME"), getenv("HARBOR_PASSWORD")))
        response = await projects_object.get_projects(api_url=url_string)
        return response

    if inputs[0] == "all_repos":
        url_string = getenv("HARBOR_API_URL") + "/repositories?page=1"
        if inputs[1]:
            url_string += f"&page_size={inputs[1]}"
        else:
            url_string += f"&page_size=100"
        all_repos_object = RepositoryApiClient((getenv("HARBOR_USERNAME"), getenv("HARBOR_PASSWORD")))
        response = await all_repos_object.get_all_authorized_repos(api_url=url_string)
        return response

    if inputs[0] == "project_repos":

        if inputs[2] != "":
            url_string = getenv("HARBOR_API_URL") + "/projects/" + inputs[2] + "/repositories?page=1"
            if inputs[1]:
                url_string += f"&page_size={inputs[1]}"
            else:
                url_string += f"&page_size=100"
            project_repos_object = RepositoryApiClient((getenv("HARBOR_USERNAME"), getenv("HARBOR_PASSWORD")))
            response = await project_repos_object.get_specific_project_repos(api_url=url_string)
            return response
    else:
        return "Please enter project name."


async def main(input_choice: str):
    inputs = input_processing(input_choice)
    if not inputs:
        return f"Exiting execution due to incorrect input. Please try again."
    try:
        response = await input_execution(inputs)
    except Exception as e:
        return e
    return response


if __name__ == "__main__":
    check_if_env_got_loaded = load_dotenv(dotenv_path=ENVPATH)
    choice = ""
    if check_if_env_got_loaded:
        while choice.lower() != exit:
            print(f"\n### Application start. ###"
                  f"Please enter action to perform on Harbor API interface "
                  f"using following options.\n"
                  f"1) list_project: To list projects.\n"
                  f"2) all_repos: To list repos.\n"
                  f"3) project_repos: To list repos.\n"
                  f"4) artifacts: To list artifacts inside the project.\n"
                  f"5) delete: To delete tags that are older than specified days "
                  f"(Default value is 30 days).\n"
                  f"6) exit: To exit the program\n")
            choice = input("Please enter your choice: ")
            if (choice.lower() == exit or
                    choice.lower() not in ["list_project", "all_repos", "project_repos", "artifacts", "delete"]):
                print("Exiting program...")
                break
            print(run(main, choice))
    else:
        print(".env file not found. Cannot proceed with APIs.")
