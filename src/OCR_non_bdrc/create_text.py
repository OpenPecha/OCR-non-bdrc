import os
import json
import gzip
import requests
import logging
from github import Github
from pathlib import Path
from get_text import get_text


ACCESS_TOKEN = os.environ.get('GITHUB_TOKEN')

logging.basicConfig(
    filename="./log/ocr_non-bdrc.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)

def add_description(repo_name, description):
    GITHUB_API_ENDPOINT = f"https://api.github.com/repos/MonlamAI/{repo_name}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {ACCESS_TOKEN}",
    }
    data = {
        "name": repo_name,
        "description": description,
    }
    
    response = requests.patch(GITHUB_API_ENDPOINT, json=data, headers=headers)
    response.raise_for_status()


def create_repo(text, repo_name, title):
    g = Github(ACCESS_TOKEN)
    org = g.get_organization('MonlamAI')
    org.create_repo(repo_name)
    with open(f'{title}.txt', 'w') as file:
        file.write(text)
    repo = g.get_repo(f'MonlamAI/{repo_name}')
    repo.create_file(f'{title}.txt', 'Initial commit', text)
    add_description(repo_name, title)
    logging.info(f"Created repo {repo_name} for {title}")

def get_text_from_OCR(OCR_path):
    final_text = {}
    file_paths = sorted(OCR_path.iterdir())
    for num, file_path in enumerate(file_paths, 1):
        ocr_object = json.load(gzip.open(str(file_path), "rb"))
        text = get_text(ocr_object)
        final_text[num]= {
            "text": text
        }
    return final_text

def create_repo_for_text(OCR_dir_path, repo_name):
    text = ""
    title = OCR_dir_path.stem
    text_dict = get_text_from_OCR(OCR_dir_path)
    for _, info in text_dict.items():
        if info['text'] is not None:
            text += info['text']
    create_repo(text, repo_name, title)


def create_repos_for_books():
    book_list = Path(f"./data/title_to_repo.txt").read_text().splitlines()
    repo_made = Path(f"./data/repo_made.txt").read_text().splitlines()
    for book_info in book_list:
        title, repo_name = book_info.split(',')
        if repo_name in repo_made:
            continue
        else:
            OCR_dir_path = Path(f"./data/OCR/{title}")
            if OCR_dir_path.exists():
                create_repo_for_text(OCR_dir_path, repo_name)
            else:
                print(f"{repo_name} does not exist")



def update_text(repo_name, file_path, new_content):
    commit_msg = f"Updated text file"
    g = Github(ACCESS_TOKEN)
    try:
        repo = g.get_repo(f"MonlamAI/{repo_name}")
        contents = repo.get_contents(f"{file_path}", ref="main")
        repo.update_file(contents.path, commit_msg, new_content, sha=contents.sha, branch="main")
    except Exception as e:
        print( f'Pecha id :{repo_name} not updated with error {e}')

def create_text_from_OCR(title):
    text = ""
    text_dict = get_text_from_OCR(Path(f"./data/OCR/{title}"))
    for _, info in text_dict.items():
        if info['text'] is not None:
            text += info['text']
    Path(f"./{title}.txt").write_text(text)

if __name__ == "__main__":
    ocr_paths = list(Path(f"./data/OCR").iterdir())
    for ocr_path in ocr_paths:
        title = ocr_path.stem
        create_text_from_OCR(title)
    # create_repos_for_books()

