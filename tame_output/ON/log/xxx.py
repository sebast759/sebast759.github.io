# %%
if 0:
    import pip
    pip.main(["install", "PyGithub"])

# %%
from github import Github
import os

access_token = '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'
repository_name = 'tame_crypto/crypto/heroku/graphs'
subfolder_path = 'graphs'

g = Github(access_token)
repos_all=g.get_user().get_repos()

print(f'******************\nWealt Repos in github.io :\n{" | ".join([x.name for x in repos_all if "wealt" in x.full_name ])}')    
print(f'******************\nPersonal Repos in github.io :\n{" | ".join([x.name for x in repos_all if "sebast759/" in x.full_name ])}')    

# %%
import re
def clean_folder_local2github(local_subfolder_path = 'graphs\\',github_repo_path = 'tame_output\\ON\\graphs'):
    # github_repo = 'sebast759.github.io'
    # github_subfolder_path = 'crypto/heroku/'
    github_repo = github_repo_path.split('\\')[0]#'tame_output'
    github_subfolder_path = re.sub(r'^\\|\\$','',github_repo_path[len(github_repo_path.split('\\')[0]):])

    
    g = Github(access_token)
    repo = g.get_user().get_repo(github_repo)

    # Get the main branch
    commit_message = 'Adding subfolder'
    branch = repo.get_branch('main')
    for subdir, dirs, files in os.walk(local_subfolder_path):
        github_path2subdir = os.path.join(github_subfolder_path,subdir.rstrip("//")).replace('\\',"/")

        folder_contents = repo.get_contents(github_path2subdir)
        # Get the list of files in the local folder
        local_files = os.listdir(local_subfolder_path)

        # Iterate over the files in the GitHub repository
        for file in folder_contents:
            if file.type == "file":
                # Get the file name and check if it exists in the local folder
                file_name = os.path.basename(file.path)
                if file_name not in local_files:
                    # Delete the file from the GitHub repository
                    repo.delete_file(file.path, f"Deleting {file}", sha= file.sha)
                    print(f"deleting {file}")

# for folder_toxp in ['graphs','bt','log']:
#     local_subfolder_path = folder_toxp
#     github_repo_path = f'tame_output\\ON'
#     ############################
#     delete_folder_local2github(local_subfolder_path = local_subfolder_path,github_repo_path = github_repo_path)
#     ############################


# %%
import re
def push_folder_local2github(local_subfolder_path = 'graphs\\',github_repo_path = 'tame_output\\graphs'):
    # github_repo = 'sebast759.github.io'
    # github_subfolder_path = 'crypto/heroku/'
    github_repo = github_repo_path.split('\\')[0]#'tame_output'
    github_subfolder_path = re.sub(r'^\\|\\$','',github_repo_path[len(github_repo_path.split('\\')[0]):])

    
    g = Github(access_token)
    repo = g.get_user().get_repo(github_repo)

    # Get the main branch
    commit_message = 'Adding subfolder'
    branch = repo.get_branch('main')

    # Iterate over files in the subfolder
    nfiles = 0
    for subdir, dirs, files in os.walk(local_subfolder_path):
        #----------------------------------------------
        # STEP 1: WE COPY LOCAL FILES TO GITHUB
        if subdir=='bt\\data':
            print(('**'*25+'\n')*2+'We don t push database in bt\\data as it s heavy files\nCan be changed later\n'+('**'*25+'\n')*2)
        else:
            for file in files:
    #             print(f'subdir {subdir}')
    #             print(f'dirs {dirs}')
                local_file_path = os.path.join(subdir, file)
                with open(local_file_path, 'rb') as f:
                    content = f.read()

                github_path2file = os.path.join(github_subfolder_path,subdir,file).replace('\\',"/")
    #             print(github_path2file)

                try:
                    existing_file = repo.get_contents(github_path2file)
                    repo.update_file(existing_file.path, f"Committing {file}", content, existing_file.sha, branch="main")
                    print(f"updating {github_path2file}")
                except:
                    repo.create_file(github_path2file, f"Committing {file}", content, branch="main")
                    print(f"creating {github_path2file}")
                nfiles+=1
            
        #----------------------------------------------
        # STEP 2: WE DELETE DELETED LOCAL FILES FROM GITHUB
        github_path2subdir = os.path.join(github_subfolder_path,subdir.rstrip("//")).replace('\\',"/")

        folder_contents = repo.get_contents(github_path2subdir)
        # Get the list of files in the local folder
        local_files = os.listdir(subdir)

        # Iterate over the files in the GitHub repository
        for file in folder_contents:
            if file.type == "file":
                # Get the file name and check if it exists in the local folder
                file_name = os.path.basename(file.path)
                if file_name not in local_files:
                    try:
                        # Delete the file from the GitHub repository
                        repo.delete_file(file.path, f"Deleting {file}", sha= file.sha)
                        print(f"deleting {file}")
                    except:
                        print(f"couldn t delete {file}")
        #----------------------------------------------
        
    print(f"files updated on github server: #{nfiles}")    

# %%
for folder_toxp in ['graphs','bt','log']:
    local_subfolder_path = 'graphs'
    github_repo_path = 'tame_output\\ON\\graphs'
    
    local_subfolder_path = folder_toxp
    github_repo_path = f'tame_output\\ON'
    ############################
    push_folder_local2github(local_subfolder_path = local_subfolder_path,github_repo_path = github_repo_path)
    ############################
