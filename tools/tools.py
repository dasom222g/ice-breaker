from langchain_community.tools import TavilySearchResults


def get_profile_url_tavily(name: str = "") -> list:
    search = TavilySearchResults()
    res = search.run(f"{name} Linkedin")  # list타입
    return res
