
import requests
import re

def fetch_and_sort_github_repositories(topic, access_token, max_results=200):
    sanitized_topic = re.sub(r'[^\w\-_\. ]', '_', topic)
    output_file = f"{sanitized_topic}_repositories.html"
    
    url = f"https://api.github.com/search/repositories?q={topic}&per_page=100&page="
    headers = {
        "Authorization": f"token {access_token}"
    }
    
    repositories = []
    page = 1
    while len(repositories) < max_results:
        response = requests.get(url + str(page), headers=headers)
        if response.status_code == 200:
            data = response.json()
            if not data["items"]:
                break
            repositories.extend(data["items"])
            page += 1
        else:
            print("Failed to fetch repositories:", response.status_code, response.reason)
            break
    
    # Sort Repo's By The Number Of Starts
    repositories = sorted(repositories, key=lambda x: x['stargazers_count'], reverse=True)
    
    # Save In Html File With URL
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("<html>\n<head>\n<title>GitHub Repositories</title>\n</head>\n<body>\n")
        file.write(f"<h1>Repositories for '{topic}'</h1>\n")
        file.write("<ul>\n")
        
        for repo in repositories[:max_results]:
            file.write(f"<li><a href='{repo['html_url']}' target='_blank'>{repo['name']}</a> - Stars: {repo['stargazers_count']}</li>\n")
        
        file.write("</ul>\n</body>\n</html>")
    
    print(f"Data saved to {output_file}")

topic = ""  # The Sunject You Want To Find!
access_token = ""  # Enter Your Github Token

fetch_and_sort_github_repositories(topic, access_token)


