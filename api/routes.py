from flask import jsonify, Blueprint, request
import random, string, werkzeug, os, sqlite3
from assembly_ai import assembly_ai
api = Blueprint('api', __name__)
UPLOAD_FOLDER = './audio'


def save_file(number_path, file):
    while True:
        filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.mp3'
        new_path = os.path.join(number_path, filename)
        if not os.path.exists(new_path):
            file.save(new_path)
            return new_path


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@api.route("/", methods=["GET", "POST"])
def default():
    return jsonify({"test": "yes"}), 200


@api.route("/fraudalert/call-logs", methods=["POST"])
def fraudalert():
    input_numbers = request.json.get("numbers", None)
    number_string = ''
    for i in input_numbers:
        if len(number_string) > 0:
            number_string += ', ' + str(i)
        else:
            number_string += str(i)
    conn = get_db_connection()
    db_numbers = conn.execute('SELECT created, number, reported_no \
                            FROM numbers \
                            WHERE number IN (' + number_string + ')').fetchall()
    conn.close()
    res_lst = list()
    for i in input_numbers:
        res = dict()
        res['number'] = i
        res['present_in_db'] = False
        for number in db_numbers:
            if number['number'] == i:
                res['created'] = number['created']
                res['reported_no'] = number['reported_no']
                res['present_in_db'] = True
        res_lst.append(res)
    return jsonify(res_lst), 200


@api.route("/fraudalert/submit_audio", methods=["POST"])
def submit_audio():
    f = request.files['recording']
    number_string = f.filename[:-4]
    number_path = os.path.join(UPLOAD_FOLDER, number_string)
    if os.path.exists(number_path):
        file_path = save_file(number_path, f)
    else:
        os.mkdir(number_path)
        file_path = save_file(number_path, f)

    conn = get_db_connection()
    number = conn.execute('SELECT number FROM numbers WHERE number = (' + number_string + ')').fetchall()
    if len(number) == 0:
        conn.execute("INSERT INTO numbers (number) VALUES (?)", (number_string,))
        conn.commit()
        print("inserted number")
    else:
        print("number is present already")
    upload_url = assembly_ai.upload_file(file_path)
    transcript_id = assembly_ai.transcribe(upload_url)
    conn.execute("INSERT INTO submissions (number, filename, transcript_id) VALUES (?, ?, ?)",
                 (number_string, file_path, transcript_id))
    conn.commit()
    conn.close()
    res = {
        "status": "Submitted Successfully"
    }
    return jsonify(res), 200


@api.route("/fraudalert/get_number_details", methods=["GET"])
def get_number_details():
    conn = get_db_connection()
    numbers = conn.execute('SELECT created, number, reported_no FROM numbers').fetchall()
    conn.close()
    res_lst = list()
    for number in numbers:
        res = dict()
        res['created'] = number['created']
        res['number'] = number['number']
        res['reported_no'] = number['reported_no']
        res_lst.append(res)
    return jsonify(res_lst), 200