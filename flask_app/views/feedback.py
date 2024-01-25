from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os
import markdown
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
    api_key = os.environ['OPENAI_API_KEY'],
    azure_endpoint = os.environ['OPENAI_ENDPOINT'],
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
    chat = AzureChatOpenAI(
        api_key = current_app.config['OPENAI_API_KEY'],
        azure_endpoint = current_app.config['OPENAI_ENDPOINT'],
        openai_api_version="2023-05-15",
        azure_deployment="GPT35TURBO")

    user_message = request.form.get('message')
    csv_file = request.files.get('csv')
    if csv_file:
        csv_file_path = os.path.join(current_app.config['UPLOAD_FILE_PATH'], "csv", csv_file.filename)
        csv_file.save(csv_file_path)
        loader = CSVLoader(file_path=csv_file_path)
        data = loader.load()
        text_splitter = SpacyTextSplitter(
            chunk_size=200,
            pipeline="en_core_web_sm"
        )
        splitted_documents = text_splitter.split_documents(data)
        database.add_documents(
            splitted_documents,
        )

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
            出力は生徒のプレゼンテーションが改善するようなアドバイスを行い、余計な出力はしないでください。
            回答は英語で行なってください。\n
            出力が英語であることはとても重要です。英語で解答ができているかどうか出力を生成したあともう一度確認するようにしてください
            出力はタイトルと見出し、本文に分けて箇条書きで行います。具体的には以下の指示に従って出力を作成してください。
            また以下に示す例を参考に出力を作成してください。
            最終確認で出力が定められた形式に従っているか確認してください。
            またタイトルが一つだけにまとめられていることはとても大事なので絶対に守ってください。タイトルは一つだけにしてください。
            ##指示
            ・タイトルは### の後にアドバイス全体を包括する内容を示してください。
            ・見出しはアドバイス一つ一つの概要を示し、内容を**で囲んだ後改行してください。
            ・本文は見出しの下に具体的なアドバイスの内容についてしめしてください。
            ・タイトルは一つにしてください。
            ・見出しは三つまでにまとめてください。
            ##例
            \"\"\"
            ### Speak more slowly and use visuals

            **you spoke a bit too fast**

            It made it difficult for some of the audience members to follow along. 
            It would be helpful to slow down your pace and give the audience enough 
            time to process the information.

            **you relied heavily on text-heavy slides**
            While it's important to have visual aids, it's also crusial to engage the audience
            through your words, Instead of reading directly from the slides, try to speak more
            naturally and use the slides as a visual support


            \"\"\"
            ###最終確認
            ・出力は英語で作成されているか
            ・タイトル、見出し、本文の構成になっているか
            ・タイトルは一つまでの制限を守っているか
            ・見出しは箇条書きで書かれているか
            ・見出しは三つまでの制限を守っているか
            ・タイトルは一つにまとめられているか
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
        result = chat(
            [
                HumanMessage(content=prompt.format(documents=document_text,
                                                        query=user_message))
            ]
        )
        text = str(result.content)
        md = markdown.Markdown()
        return md.convert(text)
    ###削除する関数
    #database.delete_collection()

    return csv_file.filename + " Upload successfully !"

@feedback_bp.route('/feedback/send_message/gpt-4', methods=['POST'])
def send_message_4():
    chat = AzureChatOpenAI(
        api_key = current_app.config['OPENAI_API_KEY'],
        azure_endpoint = current_app.config['OPENAI_ENDPOINT'],
        openai_api_version="2023-05-15",
        azure_deployment="GPT4")

    user_message = request.form.get('message')
    csv_file = request.files.get('csv')
    if csv_file:
        csv_file_path = os.path.join(current_app.config['UPLOAD_FILE_PATH'], "csv", csv_file.filename)
        csv_file.save(csv_file_path)
        loader = CSVLoader(file_path=csv_file_path)
        data = loader.load()
        text_splitter = SpacyTextSplitter(
            chunk_size=200,
            pipeline="en_core_web_sm"
        )
        splitted_documents = text_splitter.split_documents(data)
        database.add_documents(
            splitted_documents,
        )

    if user_message:
        documents = database.similarity_search(user_message)
        document_text = ""
        for document in documents:
            document_text += document.page_content

        prompt = PromptTemplate(
            template=
            """
            あなたは質問に対して文献を参照して答えを生成するアシスタントです。今からあなたが置かれている状況を
            説明しますのでそれに従って出力してください。\n
            ユーザーは生徒です。ユーザーは調べ学習の後にプレゼンテーションを行い成果を発表しました。生徒の発表を受けて
            他の生徒はその発表のフィードバックをコメントしました。\n
            発表した生徒はあなたに質問をします。あなたは与えられた文献をもとに生徒の質問に答えてください\n
            出力は生徒のプレゼンテーションが改善するようなアドバイスを行い、余計な出力はしないでください。
            回答は英語で行なってください。\n
            出力が英語であることはとても重要です。英語で解答ができているかどうか出力を生成したあともう一度確認するようにしてください
            出力は見出しとサブ見出し、本文に分けて箇条書きで行います。具体的には以下の指示に従って出力を作成してください。
            また以下に示す例を参考に出力を作成してください。
            最終確認で出力が定められた形式に従っているか確認してください。
            ##指示
            ・見出しは## の後にアドバイス全体を包括する内容を示してください。
            ・サブ見出しは### の後にアドバイス一つ一つの概要を示してください。
            ・本文はサブ見出しの下に具体的なアドバイスの内容についてしめしてください。
            ##例
            \"\"\"
            ## Speak more slowly and use visuals

            ### you spoke a bit too fast
            It made it difficult for some of the audience members to follow along. 
            It would be helpful to slow down your pace and give the audience enough 
            time to process the information.

            ### you relied heavily on text-heavy slides
            While it's important to have visual aids, it's also crusial to engage the audience
            through your words, Instead of reading directly from the slides, try to speak more
            naturally and use the slides as a visual support


            \"\"\"
            ###最終確認
            ・出力は英語で作成されているか
            ・見出し、サブ見出し、本文の構成になっているか
            ・サブ見出しは箇条書きで書かれているか
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
        result = chat(
            [
                HumanMessage(content=prompt.format(documents=document_text,
                                                        query=user_message))
            ]
        )
        text = str(result.content)
        md = markdown.Markdown()
        return md.convert(text)
    #database.delete_collection()
    return csv_file.filename + " Upload successfully !"
