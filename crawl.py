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


def get_data():
    tmp = 'method2testkotlin/tmp/tmp'
    output = 'method2testkotlin/tmp/output'
    grammar_file = 'method2testkotlin/kotlin.so'
    urls = search_github_projects('kotlin', 'Kotlin', num_pages=6)
    for repo_id, repo_git in enumerate(urls):
        analyze_project(repo_git,repo_id,grammar_file,tmp,output)
if __name__ == '__main__':
    # clone_repos()
    get_data()
