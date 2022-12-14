from db import db
from app import app

db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)