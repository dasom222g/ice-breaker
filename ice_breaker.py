from dotenv import load_dotenv
import os

if __name__ == "__main__":

    print("Hello Langchain")

    load_dotenv() # .env파일의 환경변수 로드
    print("key: ", os.getenv('OPENAI_API_KEY'))



