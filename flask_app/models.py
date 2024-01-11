from flask_app import db
from flask_sqlalchemy import SQLAlchemy
from SQLAlchemy import BLOB, Column, Integer, String

class PDFStorage(db.Model):
    id = Column(Integer, primary_key=True)
    pdf_file = Column(BLOB)

    def __init__(self, pdf_file):
        self.pdf_file = pdf_file