from flask_restful import Resource, reqparse
from db import db
from models.note import NoteModel
from flask_jwt_extended import jwt_required


class NoteLists(Resource):

    @jwt_required()
    def get(self):
        notes = NoteModel.get_all()
        return { "status": 200, "notes": [note.json() for note in notes]}

class CreateNote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "title",
        type=str,
        required=True,
        help="title cannot be blank."
    )
    parser.add_argument(
        "content",
        type=str,
        required=True,
        help="content cannot be blank."
    )
    parser.add_argument(
        "posted_by",
        type=str,
        required=True,
        help="posted_by cannot be blank."
    )

    @jwt_required()
    def post(self):
        data = CreateNote.parser.parse_args()

        note = NoteModel(data["title"], data["content"], data["posted_by"])
        try:
            note.save_to_db()
        except BaseException as error:
            print(error)
            return { "message": "an error occured while creating new note." }, 500
        return { "status": 201, "message": "note successfully created.", "note": note.json() }

class GetNoteByUserId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "user_id",
        type=str,
        required=True,
        help="user_id cannot be blank."
    )

    @jwt_required()
    def post(self):
        data = GetNoteByUserId.parser.parse_args()
        notes = NoteModel.get_note_by_user_id(user_id=data["user_id"])
        return {
            "status": 200,
            "notes": [note.json() for note in notes]
        }
                                                

class UpdateNote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "note_id",
        type=str,
        required=True,
        help="note_id cannot be blank."
    )
    parser.add_argument(
        "title",
        type=str,
        required=True,
        help="title cannot be blank."
    )
    parser.add_argument(
        "content",
        type=str,
        required=True,
        help="content cannot be blank."
    )

    @jwt_required()
    def post(self):
        data = UpdateNote.parser.parse_args()
        old_note = NoteModel.get_note_by_id(note_id=data["note_id"])
        if old_note is None:
            return { "status" : 404, "message": "note does not exisit with this id." }, 404
        try:
            NoteModel.update_note_by_note_id(note_id=data["note_id"], title=data["title"], content=data["content"])
            db.session.commit()
        except:
            return { "status": 500, "message": "an error occured while updating note." }, 500
        return {
            "status": 200,
            "message": "note successfully updated.",
        }


class DeleteNote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "note_id",
        type=str,
        required=True,
        help="note_id cannot be blank."
    )

    @jwt_required()
    def post(self):
        data =DeleteNote.parser.parse_args()
        old_note = NoteModel.get_note_by_id(note_id=data["note_id"])
        if old_note is None:
            return { "status" : 404, "message": "note does not exisit with this id." }, 404
        try:
            NoteModel.delete_note_by_note_id(note_id=data["note_id"])
            db.session.commit()
        except:
            return { "status": 500, "message": "an error occured while deleting note." }, 500
        return {
            "status": 200,
            "message": "note successfully deleted.",
        }
        