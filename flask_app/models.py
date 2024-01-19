from flask_app import db
from sqlalchemy import Column, Integer, String

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    label = db.Column(db.String)

    def __init__(self, file_name, label):
        self.file_name = file_name
        self.label = label

    def __repr__(self):
        return '<Image %r>' % self.file_name

    def register(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, file_name):
        if file_name:
            db.session.query(cls).filter(cls.file_name == file_name).delete()
            db.session.commit()

    @classmethod
    def get_all_images_by_label(cls, label_name):
        return cls.query.filter(cls.label.like(f"%{label_name}%")).all()

    @classmethod
    def get_all_images(cls):
        return cls.query.all()

    @classmethod
    def count_images(cls):
        return cls.query.count()