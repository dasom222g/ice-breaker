import time

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from agents.lookup_linkedin_url_agent import find_linkedin_profile_url
from common.data import dasom_data_url
from output_parser import summary_parser
from third_parties.linkedin import scrapping_linkedin_profile

# 사람에 대한 정보를 짧은 요약과 두개의 흥미로운 사실로 생성하길 바람
summary_template = """
    given the Linkedin information {info} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    3. please translate and respond in Korean
    \n {format_instruction}
"""
# get_format_instructions: JSON 스키마 설명을 반환하며 이값이 프롬프트({format_instruction}부분)에 추가됨
summary_prompt_template = PromptTemplate(
    input_variables=["info"],  # 동적으로 추가되는 변수
    partial_variables={'format_instruction': summary_parser.get_format_instructions()},  # 정적으로 추가되는 변수
    template=summary_template,  # summary_template안의 info를 변수로 처리
)


def ice_break():
    user_linkedin_url = find_linkedin_profile_url(name="김다솜 동서울대학")
    # info_data = scrapping_linkedin_profile(url=user_linkedin_url, mock=False)
    info_data = scrapping_linkedin_profile(url=dasom_data_url, mock=True)

    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)

    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser

    response = chain.invoke(input={'info': info_data})  # Summary타입
    print('response', response)

    result = response.to_dict()  # 클래스 내부함수를 통해 dict형으로 변환
    print(f'result: {result} {type(result)}')


def korean_chat():
    print(f'{"=" * 30} 한글로 요청 {"=" * 30}')
    prompt = PromptTemplate(
        input_variables=["person"],
        template="{person}라는 인물에 대해서 간단하게 설명해줘",
    )
    chat_gpt = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
    chain = prompt | chat_gpt
    response = chain.invoke(input={"person": "이재명"})

    print(response)


def main():
    # 체이닝

    # 링크드인 데이터로 연결 (gist)
    linkedin_data = scrapping_linkedin_profile(url=dasom_data_url, mock=True)

    # llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=OPENAI_API_KEY) # 명시적으로 key 넘김
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")  # 환경변수 사용
    # llm = ChatOllama(model="llama3")
    # llm = ChatOllama(model="mistral")

    result_prompt = summary_prompt_template.format_prompt(info="제니")

    # 체인으로 프롬프트, LLM 묶음
    chain = summary_prompt_template | llm | StrOutputParser()

    # StrOutputParser: 체이닝에서 llm의 결과값 중 ['output']값만 가져올때 사용

    start_time = time.time()

    response = chain.invoke(
        input={"info": linkedin_data}
    )  # info값에 linkedin_data 할당

    end_time = time.time()

    # print(response)
    print(f"총 소요시간: {(end_time - start_time):.2f}초")
    # korean_chat()


if __name__ == "__main__":
    # main()
    ice_break()
