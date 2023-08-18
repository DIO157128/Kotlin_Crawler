import math
import os
import subprocess
import time
import requests
from method2testkotlin.find_map_test_cases import analyze_project
import json


def search_github_projects(query, language, num_pages=1,start=1):
    base_url = "https://api.github.com/search/repositories"
    urls = []
    headers = {
        "Authorization": f"Bearer {'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'}"
    }
    for page in range(start, num_pages + 1):
        params = {
            "q": f"{query} language:{language}",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": page
        }

        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()

        if "items" in data:
            projects = data["items"]
            for project in projects:
                repo_name = project["name"]
                repo_url = project["html_url"]
                star_count = project["stargazers_count"]
                print(f"{repo_name} - Stars: {star_count}, URL: {repo_url}")
                urls.append({
                    "name": repo_name,
                    "stars": star_count,
                    "url": repo_url
                })

        time.sleep(2)

    # Save data to a JSON file
    with open("github_projects_{}.json".format(math.floor(start/20)), "a") as json_file:
        json.dump(urls, json_file, indent=4)

    return urls


def read_json_file(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def get_data():
    tmp = '/home/featurize/Kotlin_Crawler/method2testkotlin/tmpnew/tmp'
    output = '/home/featurize/Kotlin_Crawler/method2testkotlin/tmpnew/output'
    grammar_file = '/home/featurize/Kotlin_Crawler/method2testkotlin/kotlin.so'
    # search_github_projects('kotlin', 'Kotlin', num_pages=100)
    urls = read_json_file("github_projects.json")
    for repo_id, repo in enumerate(urls):
        print(repo_id)
        analyze_project(repo['url'],repo_id,grammar_file,tmp,output)

def gatherdata(path):
    data = []
    for dir_name in os.listdir(path):
        jsons = os.listdir(os.path.join(path,dir_name))
        if len(jsons)==1:
            continue
        else:
            for dir_name2 in jsons:
                if dir_name2=='log.txt':
                    continue
                else:
                    this_data = read_json_file(os.path.join(path,dir_name,dir_name2))
                    data.append(this_data)
    with open("kotlin_data.json", "a") as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    # search_github_projects('kotlin', 'Kotlin', num_pages=10,start=1)
    # get_data()
    gatherdata('method2testkotlin/tmpnew/output')