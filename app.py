from flask import Flask, jsonify, request, make_response, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="/static", static_folder="static")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.create_all()


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    text = db.Column(db.Text)


# Routing
@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")


@app.route('/note/<id>', methods=['GET'])
def edit_note():
    return render_template("index.html")


# Rest API
@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    notes = Note.query.all()
    output = []
    for note in notes:
        output.append({
            'id': note.id,
            'title': note.title,
            'text': note.text
        })

    return jsonify(output)


@app.route('/api/note/<id>', methods=['GET'])
def get_note(id):
    note = Note.query.filter_by(id=id).first()
    return jsonify({
        'id': note.id,
        'title': note.title,
        'text': note.text
    })


@app.route('/api/notes', methods=['POST'])
def create_post():
    data = request.json
    print(data)

    note = Note(
        title=data['title'],
        text=data['text']
    )
    db.session.add(note)
    db.session.commit()

    return jsonify({
        'id': note.id,
        'title': note.title,
        'text': note.text
    })


@app.route('/api/notes/<note_id>', methods=['DELETE'])
def delete_post(note_id):
    print(note_id)

    note = Note.query.filter_by(id=note_id).first()
    db.session.delete(note)
    db.session.commit()

    return jsonify({
        'Successfully deleted ': note_id,
        'status': 200
    }
    )


@app.route('/api/notes/<note_id>', methods=['PUT'])
def edit_post(note_id):
    data = request.json
    print(data)

    note = Note.query.filter_by(id=note_id).first()
    print(note.id, note.title, note.text)
    title = data['title']
    text = data['text']

    note.title = title
    note.text = text
    db.session.commit()

    return jsonify({
        'id': note.id,
        'title': note.title,
        'text': note.text
    })


if __name__ == "__main__":
    app.run()
