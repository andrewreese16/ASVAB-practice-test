import json
import psycopg2


def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname="quiz_app",
        user="andrewreese",
        password="12345",
        host="localhost",
    )


def load_questions(file_path):
    """Loads questions from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)


def upload_questions_to_db(questions):
    """Uploads questions to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    for question in questions:
        cursor.execute(
            """
            INSERT INTO questions (question, options, answer)
            VALUES (%s, %s, %s);
            """,
            (question["question"], question["options"], question["answer"]),
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Uploaded {len(questions)} questions to the database.")


if __name__ == "__main__":
    file_path = "data/questions.json"
    questions = load_questions(file_path)
    upload_questions_to_db(questions)
