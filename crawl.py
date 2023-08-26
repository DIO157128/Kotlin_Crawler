import math
import os
import random
import re
import subprocess
import time
import requests
import json
import pandas as pd
from method2testkotlin.find_map_test_cases import analyze_project


def search_github_projects(query, language, num_repos):
    base_url = "https://api.github.com/search/repositories"
    urls = []
    headers = {
        "Authorization": f"Bearer {'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'}"
    }
    epochs = int((num_repos-1000)/1000)
    #first round
    for page in range(1,11):
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
    #start recursive search
    for i in range(epochs):
        last_star = urls[-1]['stars']
        urls = [i for i in urls if i['stars']!=last_star]
        before_last_len = len(urls)
        for page in range(1, 11):
            params = {
                "q": f"{query} language:{language} stars:{last_star}",
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

            time.sleep(10)
        after_Last_len = len(urls)
        if last_star==0:
            with open("github_projects_{}.json".format(num_repos), "a") as json_file:
                json.dump(urls, json_file, indent=4)

            return urls
        if after_Last_len-before_last_len==1000:
            last_star-=1
        for page in range(1, 11):
            params = {
                "q": f"{query} language:{language} stars:<{last_star}",
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

            time.sleep(10)

    # Save data to a JSON file
    with open("github_projects_{}.json".format(num_repos), "a") as json_file:
        json.dump(urls, json_file, indent=4)

    return urls


def read_json_file(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def get_data(num_repos):
    tmp = '/home/featurize/Kotlin_Crawler/method2testkotlin/tmp{}/tmp'.format(num_repos)
    output = '/home/featurize/Kotlin_Crawler/method2testkotlin/tmp{}/output'.format(num_repos)
    grammar_file = '/home/featurize/Kotlin_Crawler/method2testkotlin/kotlin.so'
    # search_github_projects('kotlin', 'Kotlin', num_pages=100)
    urls = read_json_file("github_projects_{}.json".format(num_repos))
    log = open('log.txt','a',encoding ='utf-8')
    for repo_id, repo in enumerate(urls):
        print(repo_id)
        try:
            analyze_project(repo['url'],repo_id,grammar_file,tmp,output)
        except Exception:
            log.write(str(repo_id)+'\n')
            continue

def get_data4test():
    tmp = '/root/ybw/pycharmremote/method2testkotlin/tmpnew/tmp'
    output = '/root/ybw/pycharmremote/method2testkotlin/tmpnew/output'
    grammar_file = '/root/ybw/pycharmremote/method2testkotlin/kotlin.so'
    # search_github_projects('kotlin', 'Kotlin', num_pages=100)
    urls = read_json_file("github_projects.json")
    log = open('log.txt','r',encoding ='utf-8')
    lines = log.read().splitlines()
    lines = [int(l) for l in lines]
    for repo_id, repo in enumerate(urls):
        if repo_id not in lines:
            continue
        print(repo_id)
        print(repo)
        try:
            analyze_project(repo['url'],repo_id,grammar_file,tmp,output)
        except Exception:
            log.write(str(repo_id)+'\n')
            continue


def gatherdata(path,num_repos):
    base_folder = path  # 将此路径替换为您的文件夹路径

    # 创建一个空的字典，用于存储所有的JSON数据
    combined_data = {}

    # 遍历文件夹中的文件夹和文件
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            folder_data = {}
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, "r") as json_file:
                        try:
                            json_data = json.load(json_file)
                            folder_data[file_name] = json_data
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON in {file_path}: {e}")
            combined_data[folder_name] = folder_data

    # 将合并后的数据保存到最终的JSON文件中
    final_json_path = "kotlin_data_{}.json".format(num_repos)  # 将此路径替换为您希望保存最终JSON文件的路径
    with open(final_json_path, "w") as final_json_file:
        json.dump(combined_data, final_json_file, indent=4)
def countassert(test_case_string):
    pattern = re.compile(r'assert\w+\s*')
    matches = pattern.findall(test_case_string)

    # 统计匹配的数量
    assert_count = len(matches)
    return assert_count
def findassert(string):
    assertion_pattern = re.compile(r'.*assert.*')
    lines = string.split('\n')
    for l in lines:
        if assertion_pattern.match(l):
            return l.strip()
def get_csv(path):
    data = read_json_file(path)
    source = []
    target = []
    multiassert = 0
    singleassert = 0
    zeroassert = 0
    len_data = 0
    for folder_idx in data:
        folder_data = data[folder_idx]
        if len(folder_data)==0:
            continue
        else:
            for file_idx in folder_data:
                len_data+=1
                file_data = folder_data[file_idx]
                test_case_body = file_data['test_case']['body']
                focal_method_body = file_data['focal_method']['body']
                if countassert(test_case_body)>1:
                    multiassert+=1
                elif countassert(test_case_body)==1:
                    singleassert+=1
                    cleaned_test_case = re.sub(r'\s+', ' ', test_case_body)
                    cleaned_focal_method = re.sub(r'\s+', ' ', focal_method_body)
                    assert_sentence = findassert(test_case_body)
                    s = cleaned_test_case.replace(assert_sentence,'"<AssertPlaceHolder>"')+' "<FocalMethod>" '+cleaned_focal_method
                    t = assert_sentence
                    source.append(s)
                    target.append(t)
                elif countassert(test_case_body)==0:
                    zeroassert+=1
    print("multiassert:{}".format(multiassert))
    print("singleassert:{}".format(singleassert))
    print("zeroassert:{}".format(zeroassert))
    print(len_data)
    data = [(s,t) for s,t in zip(source,target)]
    random.shuffle(data)
    train = data[:int(len(data)*0.8)]
    val = data[int(len(data) * 0.8):int(len(data) * 0.9)]
    test = data[int(len(data) * 0.9):]
    source_train = [d[0] for d in train]
    target_train = [d[1] for d in train]
    source_val = [d[0] for d in val]
    target_val = [d[1] for d in val]
    source_test = [d[0] for d in test]
    target_test = [d[1] for d in test]
    df_train = pd.DataFrame()
    df_val = pd.DataFrame()
    df_test = pd.DataFrame()
    df_train['source'] = source_train
    df_train['target'] = target_train
    df_val['source'] = source_val
    df_val['target'] = target_val
    df_test['source'] = source_test
    df_test['target'] = target_test
    df_train.to_csv('kotlin_data_train.csv',index=False,encoding='utf-8')
    df_val.to_csv('kotlin_data_val.csv', index=False, encoding='utf-8')
    df_test.to_csv('kotlin_data_test.csv', index=False, encoding='utf-8')






if __name__ == '__main__':
    # search_github_projects('kotlin', 'Kotlin', 5000)
    # get_data(5000)
    # gatherdata('/home/featurize/Kotlin_Crawler/method2testkotlin/tmp5000/output',5000)
    get_data(10000)
    gatherdata('/home/featurize/Kotlin_Crawler/method2testkotlin/tmp10000/output',10000)
    # get_data4test()
    get_csv('kotlin_data.json')
