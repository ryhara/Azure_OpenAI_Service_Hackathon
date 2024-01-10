from flask_app.app import app
from flask_app import db
from flask import request
from sqlalchemy import BLOB, Column, Integer, String

class PDFStorage(db.Model):
    id = Column(Integer, primary_key=True)
    pdf_file = Column(BLOB)

    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        pdf_data = file.read()

        # 既存のPDFデータを新しいデータで上書き
        new_pdf = PDFStorage.query.get(1) or PDFStorage(pdf_data)
        new_pdf.pdf_file = pdf_data
        db.session.add(new_pdf)
        db.session.commit()

        return 'File uploaded and saved successfully'
    return 'No file uploaded'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
