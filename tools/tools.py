from langchain_community.tools import TavilySearchResults


def get_profile_url_tavily(name: str = ''):
    search = TavilySearchResults()
    res = search.run(f'{name} site: linkedin')
    print('type: ', type(res))
    return res
