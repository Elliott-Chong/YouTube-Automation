import os
import subprocess
from dotenv import load_dotenv
import requests
load_dotenv()

# Enter your GitHub access token here
ACCESS_TOKEN = os.getenv('GITHUB_TOKEN')
LEETCODE_DIR = '/Users/elliott/Documents/Coding/LeetCode'

def create_directory(folder_name):
    path = os.path.join(LEETCODE_DIR, folder_name)
    os.makedirs(path)
    return path

def create_readme(directory, youtube_link, problem_link):
    readme_path = os.path.join(directory, 'README.md')
    with open(readme_path, 'w') as readme_file:
        readme_file.write(f'# {folder_name}\n\n')
        readme_file.write(f'YouTube Link: [{folder_name}]({youtube_link})\n\n')
        readme_file.write(f'Problem Link: [{folder_name}]({problem_link})\n\n')

def create_solution_file(directory, code):
    solution_path = os.path.join(directory, 'solution-1.py')
    with open(solution_path, 'w') as solution_file:
        solution_file.write(code)

def commit_and_push(folder_name):
    working_dir = os.path.join(LEETCODE_DIR, folder_name)
    git_add_cmd = ['git', 'add', '.']
    git_commit_cmd = ['git', 'commit', '-am', f'Added {folder_name}']
    git_push_cmd = ['git', 'push']

    subprocess.run(git_add_cmd, cwd=working_dir)
    subprocess.run(git_commit_cmd, cwd=working_dir)
    subprocess.run(git_push_cmd, cwd=working_dir)

def create_notion_row(title, video_link, problem_link):
    headers = {
        'Authorization': f'Bearer {os.getenv("NOTION_SECRET")}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'
    }

    data = {
        'parent': {
            'database_id': os.getenv('NOTION_DATABASE_ID')
        },
        'properties': {
            'Title': {
                'title': [
                    {
                        'text': {
                            'content': title
                        }
                    }
                ]
            },
            'Video Link': {
                'url': video_link
            },
            'Link': {
                'url': problem_link
            },
        }
    }

    response = requests.post(
        'https://api.notion.com/v1/pages',
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        print('New row created in Notion table successfully!')
    else:
        print('Failed to create a new row in Notion table.')
        print(response.text)


if __name__ == '__main__':
    folder_name = input("Enter the name of the folder (corresponding to the LeetCode title): ")
    youtube_link = input("Enter the YouTube link for the LeetCode solution: ")
    problem_link = input("Enter the problem link for the LeetCode problem: ")
    print("Enter the code of the solution (use 'END' on a new line to finish):")
    code_lines = []
    while True:
        line = input()
        if line == 'END':
            break
        code_lines.append(line)
    code = '\n'.join(code_lines)
    directory = create_directory(folder_name)
    create_readme(directory, youtube_link, problem_link)
    create_solution_file(directory, code)

    commit_and_push(folder_name)

    print("Code submission to GitHub complete!")
    create_notion_row(folder_name, youtube_link, problem_link)
    print("Notion row created successfully!")
