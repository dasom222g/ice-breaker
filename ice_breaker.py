import time

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 사람에 대한 정보를 짧은 요약과 두개의 흥미로운 사실로 생성하길 바람
summary_template = """
    given the information {info} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    3. please translate and respond in Korean
"""

info = """
    Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman known for his leadership of Tesla, SpaceX, and X (formerly Twitter). Since 2025, he has been a senior advisor to United States president Donald Trump and the de facto head of the Department of Government Efficiency (DOGE). Musk has been the wealthiest person in the world since 2021; as of March 2025, Forbes estimates his net worth to be US$345 billion. He was named Time magazine's Person of the Year in 2021.

    Born to a wealthy family in Pretoria, South Africa, Musk emigrated in 1989 to Canada. He graduated from the University of Pennsylvania in the U.S. before moving to California to pursue business ventures. In 1995, Musk co-founded the software company Zip2. Following its sale in 1999, he co-founded X.com, an online payment company that later merged to form PayPal, which was acquired by eBay in 2002. That year, Musk also became a U.S. citizen.
    
    In 2002, Musk founded the space technology company SpaceX, becoming its CEO and chief engineer; the company has since led innovations in reusable rockets and commercial spaceflight. Musk joined the automaker Tesla as an early investor in 2004 and became its CEO and product architect in 2008; it has since become a leader in electric vehicles. In 2015, he co-founded OpenAI to advance artificial intelligence research but later left; growing discontent with the organization's direction in the 2020s led him to establish xAI. In 2022, he acquired the social network Twitter, implementing significant changes and rebranding it as X in 2023. In January 2025, he was appointed head of Trump's newly created DOGE. His other businesses include the neurotechnology company Neuralink, which he co-founded in 2016, and the tunneling company the Boring Company, which he founded in 2017.
    
    Musk's political activities and views have made him a polarizing figure. He has been criticized for making unscientific and misleading statements, including COVID-19 misinformation and promoting conspiracy theories, and affirming antisemitic, racist, and transphobic comments. His acquisition of Twitter was controversial due to a subsequent increase in hate speech and the spread of misinformation on the service. Especially since the 2024 U.S. presidential election, Musk has been heavily involved in politics as a vocal supporter of Trump. Musk was the largest donor in the 2024 U.S. presidential election and is a supporter of global far-right figures, causes, and political parties. His role in the second Trump administration, particularly in regards to DOGE, has attracted public backlash.
"""


def korean_chat():
    prompt = PromptTemplate(input_variables=['person'], template='{person}라는 인물에 대해서 간단하게 설명해줘')
    chat_gpt = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
    chain = prompt | chat_gpt
    response = chain.invoke(input={'person': '이재명'})

    print(response)


def main():
    print("hello Langchain")

    # .env파일의 환경변수 로드
    load_dotenv()
    # print("key: ", os.getenv("OPENAI_API_KEY"))

    # 체이닝
    summary_prompt_template = PromptTemplate(
        input_variables=["info"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    # 체인으로 프롬프트, LLM 묶음
    chain = summary_prompt_template | llm

    start_time = time.time()

    response = chain.invoke(input={"info": info})

    end_time = time.time()

    print(response)
    print(f"총 소요시간: {(end_time - start_time):.2f}초")
    korean_chat()


if __name__ == "__main__":
    main()
