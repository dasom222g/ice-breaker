import os

import requests
from dotenv import load_dotenv

from common.data import dasom_data_url, dasom_linkedin_url

eden_data_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"


# LinkedIn 프로필 데이터 스크래핑
def scrapping_linkedin_profile(url: str, mock: bool = False):
    """
       Args:
           url (str): 스크래핑할 LinkedIn 프로필의 URL
           mock (bool, optional): 실제 API 호출 대신 목(Mock) 데이터 사용 여부.
                                  기본값은 False로 실제 API를 통해 데이터를 가져옴.

       Returns:
           dict: 프로필 데이터

       Raises:
           requests.RequestException: API 요청 중 오류 발생 시
       """
    if mock:
        # 링크드인api 요청없이 gist에서 데이터 가져오기
        print("gist")
        response = requests.get(url=url, timeout=10)
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
    # profile = scrapping_linkedin_profile(dasom_linkedin_url, mock=False)
    profile = scrapping_linkedin_profile(dasom_data_url, mock=True)
    print(profile)


if __name__ == "__main__":
    main()
