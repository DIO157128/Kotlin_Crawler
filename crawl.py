import os
import subprocess

import requests
from method2testkotlin.find_map_test_cases import analyze_project
def search_github_projects(query, language, num_pages=1):
    base_url = "https://api.github.com/search/repositories"
    urls = []

    for page in range(1, num_pages + 1):
        params = {
            "q": f"{query} language:{language}",
            "sort": "stars",
            "order": "desc",
            "per_page": 30,  # 每页记录数
            "page": page
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if "items" in data:
            projects = data["items"]
            for project in projects:
                repo_name = project["name"]
                repo_url = project["html_url"]
                star_count = project["stargazers_count"]
                print(f"{repo_name} - Stars: {star_count}, URL: {repo_url}")
                urls.append(repo_url)

    return urls


def clone_repos():
    tmp = 'method2testkotlin/tmp/tmp'
    output = 'method2testkotlin/tmp/output'
    log_file = 'method2testkotlin/tmp/clone_errors.log'  # 新增日志文件路径
    urls = search_github_projects('kotlin', 'Kotlin',num_pages=6)

    with open(log_file, 'w') as log:  # 打开日志文件用于写入
        for repo_id, repo_git in enumerate(urls):
            if repo_id<30:
                continue
            repo = {}
            repo["url"] = repo_git
            repo["repo_id"] = repo_id

            # Create folders
            os.makedirs(tmp, exist_ok=True)
            repo_path = os.path.join(tmp, str(repo_id))
            repo_out = os.path.join(output, str(repo_id))
            os.makedirs(repo_out, exist_ok=True)

            # Clone repo
            print("Cloning repository {}...".format(repo_git))
            try:
                subprocess.call(['git', 'clone', repo_git, repo_path], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:  # 处理克隆失败的情况
                log.write("Error cloning repository: {}\n".format(repo_git))
def get_data():
    tmp = 'method2testkotlin/tmp/tmp'
    output = 'method2testkotlin/tmp/output'
    grammar_file = 'method2testkotlin/kotlin.so'
    urls = search_github_projects('kotlin', 'Kotlin', num_pages=6)
    for repo_git, repo_id in enumerate(urls):
        analyze_project(repo_git,repo_id,grammar_file,tmp,output)
if __name__ == '__main__':
    # clone_repos()
    get_data()
