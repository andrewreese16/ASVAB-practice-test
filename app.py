from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)


# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="quiz_app", user="andrewreese", password="12345", host="localhost"
    )


@app.route("/")
def index():
    """Load the main quiz page."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, options FROM questions;")
    questions = cursor.fetchall()
    cursor.close()
    conn.close()

    # Add alphabetic labels for options
    questions_list = [
        {
            "id": row[0],
            "question": row[1],
            "options": [
                {"label": chr(65 + i), "text": opt} for i, opt in enumerate(row[2])
            ],
        }
        for row in questions
    ]
    return render_template("index.html", questions=questions_list)


@app.route("/submit", methods=["POST"])
def submit():
    """Calculate score from submitted answers."""
    user_answers = request.json.get("answers", {})
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, answer FROM questions;")
    answers = dict(cursor.fetchall())
    cursor.close()
    conn.close()

    # Calculate score
    score = sum(
        1
        for q_id, user_ans in user_answers.items()
        if answers.get(int(q_id)) == user_ans
    )
    return jsonify({"score": score, "total": len(answers)})


if __name__ == "__main__":
    app.run(debug=True)
