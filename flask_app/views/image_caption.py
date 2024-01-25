!pip install openai==1.9.0
!pip install chromadb==0.3.29
!pip install langchain
!pip install langchain_openai
!pip install spacy
!python3 -m spacy download en_core_web_sm
これ見てrequirements.txt書き換えといて

import os
credential = DefaultAzureCredential()
os.environ["OPENAI_API_TYPE"] = "azure_ad"
os.environ['OPENAI_API_KEY'] = ""
os.environ["OPENAI_ENDPOINT"] = ""
os.environ['OPENAI_API_VERSION'] = '2023-05-15'

from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain import PromptTemplate
from langchain.schema import HumanMessage
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.text_splitter import SpacyTextSplitter
from langchain.vectorstores import Chroma

##ここのモデルは4でも構いません。
chat = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="GPT35TURBO",)


prompt = PromptTemplate(
    template="""
    あなたは質問に対して文献を参照して答えを生成するアシスタントです。今からあなたが置かれている状況を
    説明しますのでそれに従って出力してください。\n
    ユーザーは生徒です。ユーザーは調べ学習の後にプレゼンテーションを行い成果を発表しました。生徒の発表を受けて
    他の生徒はその発表のフィードバックをコメントしました。\n
    発表した生徒はあなたに質問をします。あなたは与えられた文献をもとに生徒の質問に答えてください\n
    出力は生徒のプレゼンテーションが改善するようなアドバイスの形式で行い、余計な出力はしないでください。
    また回答は英語で行なってください。\n
    出力が英語であることはとても重要です。英語で解答ができているかどうか出力を生成したあともう一度確認するようにしてください

    ###文献\n
    {documents}\n
    ###質問\n
    {query}\n
    ###出力\n
    """,

    input_variables=[
        "documents",
        "query"
    ]
)
###CSVをおいておくディレクトリはuploads/csvにしたい
loader = CSVLoader(file_path="/content/sample_feedback.csv")

data = loader.load()

text_splitter = SpacyTextSplitter(
    chunk_size=200,
    pipeline="en_core_web_sm"
)

splitted_documents = text_splitter.split_documents(data)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="ADA",
    openai_api_version="2023-05-15"
)
###persist_directoryは/app/instance以下にデータベースとして配置してください
database = Chroma(
    persist_directory="./data",
    embedding_function=embeddings
)

prompt = PromptTemplate(
    template="""
    あなたは質問に対して文献を参照して答えを生成するアシスタントです。今からあなたが置かれている状況を
    説明しますのでそれに従って出力してください。\n
    ユーザーは生徒です。ユーザーは調べ学習の後にプレゼンテーションを行い成果を発表しました。生徒の発表を受けて
    他の生徒はその発表のフィードバックをコメントしました。\n
    発表した生徒はあなたに質問をします。あなたは与えられた文献をもとに生徒の質問に答えてください\n
    出力は生徒のプレゼンテーションが改善するようなアドバイスの形式で行い、余計な出力はしないでください。
    また回答は英語で行なってください。\n
    出力が英語であることはとても重要です。英語で解答ができているかどうか出力を生成したあともう一度確認するようにしてください

    ###文献\n
    {documents}\n
    ###質問\n
    {query}\n
    ###出力\n
    """,

    input_variables=[
        "documents",
        "query"
    ]
)
###話し方についての改善施策の部分はユーザー入力にしてください
result = chat(
    [
        HumanMessage(content=prompt.format(documents=document_text,
                                                query="話し方についての改善施策"))
    ]
)






###削除する関数。
database.delete(ids = "sample_feedback.csv")