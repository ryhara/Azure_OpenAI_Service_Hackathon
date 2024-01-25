from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain import PromptTemplate
from langchain.schema import HumanMessage
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.text_splitter import SpacyTextSplitter
from langchain.vectorstores import Chroma


feedback_bp = Blueprint('feedback', __name__)
embeddings = AzureOpenAIEmbeddings(
    azure_deployment="ADA",
    openai_api_version="2023-05-15"
)
database = Chroma(
    persist_directory="/app/instance/lang",
    embedding_function=embeddings
)

@feedback_bp.route('/feedback')
def feedback():
    return render_template('feedback.index.html')

@feedback_bp.route('/feedback/send_message/gpt-3-5', methods=['POST'])
def send_message_3_5():
    ##ここから
    chat = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="GPT35TURBO",)
    
    user_message = request.form.get('message')
    csv_file = request.files.get('csv')
    if csv_file:
        csv_filename = csv_file.filename()
        ###CSVをおいておくディレクトリはuploads/csvにしたい ###これであってます？
        loader = CSVLoader(file_path=("/uploads/csv/" + csv_filename))
        data = loader.load()
        text_splitter = SpacyTextSplitter(
            chunk_size=200,
            pipeline="en_core_web_sm"
        )
        splitted_documents = text_splitter.split_documents(data)
        ###persist_directoryは/app/instance以下にデータベースとして配置してください
        database.add_documents(
            splitted_documents,
        )


    #ここからはユーザ入力がある場合 
    if user_message:   
        documents = database.similarity_search(user_message)
        document_text = ""
        for document in documents:
            document_text += document.page_content

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
                                                        query=user_message))
            ]
        )
        return result

    ###削除する関数。（削除するかはりょうせいにお任せします）
    #database.delete_collection()

    ##ここまで

    return "Feedback GPT3.5 function is not implemented yet."

@feedback_bp.route('/feedback/send_message/gpt-4', methods=['POST'])
def send_message_4():
    user_message = request.form.get('message')
    return "Feedback GPT 4 function is not implemented yet."
