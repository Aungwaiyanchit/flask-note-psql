from db import db
import uuid

class NoteModel(db.Model):

    __tablename__="notes"

    id = db.Column(db.String(80),primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    posted_by = db.Column(db.String(80), db.ForeignKey('users.id'))
    
    # user = db.relationship("UserModel", back_populates="notes")

    def __init__(self, title, content, posted_by):
        self.title = title
        self.content = content
        self.posted_by = posted_by

    @classmethod
    def get_all(cls):
        return cls.query.all()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def json(self): 
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }

    @classmethod
    def get_note_by_user_id(cls, user_id):
        notes = cls.query.filter(NoteModel.posted_by==user_id)
        return notes

    @classmethod
    def get_note_by_id(cls, note_id):
        note = cls.query.filter(NoteModel.id==note_id).first()
        return note

    @classmethod
    def update_note_by_note_id(cls, note_id, title, content):
        update_notes = cls.query.filter(NoteModel.id==note_id).update(
            {
                "title": title,
                "content": content 
            }
        )
        return update_notes

    @classmethod
    def delete_note_by_note_id(cls, note_id):
        delete_notes = cls.query.filter(NoteModel.id==note_id).delete()
        return delete_notes