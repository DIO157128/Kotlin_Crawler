import requests

def search_github_projects(query, language):
    base_url = "https://api.github.com/search/repositories"
    params = {
        "q": f"{query} language:{language}",
        "sort": "stars",
        "order": "desc"
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

if __name__ == "__main__":
    search_query = "kotlin"
    search_language = "Kotlin"
    search_github_projects(search_query, search_language)
