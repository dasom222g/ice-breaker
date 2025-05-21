from langchain import hub
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from tools.tools import get_profile_url_tavily

prompt_template = 'Given the full name of {name_of_person}, get me a link to that person"s LinkedIn profile page. Your answer should contain only the URL.'


# {name_of_person}의 전체 이름이 주어졌을 때, 해당 인물의 LinkedIn 프로필 페이지 링크를 나에게 가져다 주세요. 답변은 URL만 포함해야 합니다.

def find_linkedin_profile_url(name: str) -> str:
    """
    주어진 이름으로 LinkedIn 프로필 URL을 리턴하는 함수

    Args:
        name (str): 검색할 사람의 전체 이름

    Returns:
        str: 찾은 LinkedIn 프로필 URL
             (URL을 찾지 못할 경우 빈 문자열 또는 예외 처리)

    Example:
        # >>> find_linkedin_profile_url("Eden Marco")
        "https://www.linkedin.com/in/eden-marco"
    """
    print("=" * 50)
    # 1. Agent 생성 준비

    # 1-1. LLM 초기화
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 1-2. 프롬프트 로드
    # Agent의 전체적인 추론 전략을 결정
    react_prompt = hub.pull("hwchase17/react")  # PromptTemplate 객체
    print(react_prompt.template)  # 프롬프트

    # 1-3. Tool 정의
    tools = [
        Tool(
            name="Find LinkedIn profile URL via Google",  # Google을 통해 LinkedIn 프로필 URL 찾기
            func=get_profile_url_tavily,  # 1-4. Tool에 연결할 함수 정의
            description="useful for when you need get the Linkedin Page URL",  # LinkedIn 페이지 URL이 필요할 때 유용함
        )
    ]

    # 2. Agent 생성
    agent = create_react_agent(llm=llm, prompt=react_prompt, tools=tools)

    # 3. AgentExecutor 생성
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 4. Agent 실행
    prompt = PromptTemplate(
        input_variables=["name_of_person"],
        template=prompt_template,
    )
    response = agent_executor.invoke({'input': prompt.format_prompt(name_of_person=name).text})

    return response['output']
