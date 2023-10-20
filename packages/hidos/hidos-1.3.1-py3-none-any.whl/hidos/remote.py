import requests


def gihub_search_commits(hexsha: str) -> dict[str, str]:
    url = f"https://api.github.com/search/commits"
    query = {"q": "hash%3A" + hexsha}
    query = {"q": "hash:" + hexsha}
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "hidos",
    }
    resp = requests.get(url, params=query, headers=headers)
    resp.raise_for_status()
    pod = resp.json()
    ret = dict()
    for it in pod.get("items", []):
        repo = it["repository"]
        rid = "gh-" + str(repo["id"])
        url = "https://github.com/" + repo["full_name"] + ".git"
        ret[rid] = url
    return ret
