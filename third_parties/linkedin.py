import os

import requests
from dotenv import load_dotenv

eden_data_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
dasom_linkedin_url = "https://www.linkedin.com/in/dasom-kim-611008233"
dasom_data_url = "https://gist.githubusercontent.com/dasom222g/dbc23bafe205ff7985c2d27cafe16338/raw/2cdcdc5b962eac61e749134027eb13f502c5e667/dasom-json"


def scrap_linkedin_profile(url: str, mock: bool = False):
    if mock:
        # 링크드인api 요청없이 gist에서 데이터 가져오기
        print("gist")
        response = requests.get(url=dasom_data_url, timeout=10)
    else:
        print("api")
        # 링크드인 api요청하여 데이터 가져오기
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"

        load_dotenv()
        headers = {"Authorization": "Bearer " + os.getenv("PROXYCURL_API_KEY")}
        params = {"linkedin_profile_url": dasom_linkedin_url}

        response = requests.get(
            api_endpoint, params=params, headers=headers, timeout=10
        )

    data = response.json()

    # 데이터 정제
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "None", None)  # 값이 빈 리스트, 빈 스트링, None인 경우 해당 데이터 제거
           and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


def main():
    profile = scrap_linkedin_profile(dasom_linkedin_url, mock=True)
    print(profile)


if __name__ == "__main__":
    main()
