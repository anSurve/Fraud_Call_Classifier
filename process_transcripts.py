from assembly_ai import assembly_ai
import sqlite3, os
from config import *
TRANSCRIPT_FOLDER = 'transcription'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def save_transcript_file(file, transcript):
    f = open(file, "w")
    f.write(transcript)
    f.close()


def is_scam_call(transcript):
    is_scam = False
    for i in SCAM_KEYWORDS:
        match_cnt = 0
        for j in i:
            if j in transcript:
                match_cnt += 1
        if match_cnt == len(i):
            is_scam = True
    return is_scam


def process_transcripts():
    conn = get_db_connection()
    transcripts = conn.execute("SELECT id, number, transcript_id, filename from submissions where \
                              is_processed = 'N' and transcript_id IS NOT NULL").fetchall()
    conn.close()
    for transcript in transcripts:
        status = assembly_ai.poll_transcription_status(transcript["transcript_id"])
        if status == "completed":
            print("checking for scam - ", str(transcript["transcript_id"]))
            transcription = assembly_ai.get_transcription(transcript["transcript_id"])
            number_path = os.path.join(TRANSCRIPT_FOLDER, str(transcript["number"]))
            if os.path.exists(number_path):
                save_transcript_file(os.path.join(number_path, transcript["filename"][-14:-4] + '.txt'), transcription)
            else:
                os.mkdir(number_path)
                save_transcript_file(os.path.join(number_path, transcript["filename"][-14:-4] + '.txt'), transcription)

            conn = get_db_connection()
            is_scam = is_scam_call(transcription)
            conn.execute("UPDATE submissions SET is_processed = 'Y' \
                         WHERE id = ?", (transcript["id"],))
            conn.commit()

            if is_scam:
                post = conn.execute('SELECT reported_no FROM numbers WHERE number = ?',
                                    (transcript["number"],)).fetchone()
                updated_no = int(post["reported_no"]) + 1
                conn.execute("UPDATE numbers SET reported_no = ? \
                             WHERE number = ?", (updated_no, transcript["number"]))
                conn.commit()
            conn.close()


process_transcripts()
