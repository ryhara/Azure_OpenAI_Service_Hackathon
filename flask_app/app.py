from flask import render_template
from flask_app import create_app

app = create_app()

@app.route('/')
def home():
    return render_template('home.index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# TODO : 多分使わない
# #databaseの更新
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     file = request.files['file']
#     if file:
#         pdf_data = file.read()

#         new_pdf = PDFStorage.query.get(1) or PDFStorage(pdf_data)
#         new_pdf.pdf_file = pdf_data
#         db.session.add(new_pdf)
#         db.session.commit()

#         return 'File uploaded and saved successfully'
#     return 'No file uploaded'

if __name__ == '__main__':
    app.run()
