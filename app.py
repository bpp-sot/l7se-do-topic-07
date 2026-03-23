from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['DB_PATH'] = 'studytrack.db'


def get_db_connection():
    conn = sqlite3.connect(app.config['DB_PATH'])
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/students/search', methods=['GET'])
def search_students():
    surname = request.args.get('surname', '')
    conn = get_db_connection()
    query = ("SELECT student_id, first_name, last_name, course, year "
             f"FROM students WHERE last_name = '{surname}'")
    results = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in results])


if __name__ == '__main__':
    app.run(debug=True)
