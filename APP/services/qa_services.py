from data import database
from data.models import QA, QABody, QAsubject


def qa_all():
    data = database.read_query('''
            SELECT q.id, u.username, q.question, q.answer, s.subject
            FROM q_a q JOIN users u ON q.author_id = u.id
            JOIN qa_subjects s ON q.qa_subjects_id = s.id
            ORDER BY q.qa_subjects_id''')

    return [QA.from_query_result(*row) for row in data]


def all_subjects():
    data = database.read_query('''SELECT * FROM qa_subjects''')

    return [QAsubject.from_query_result(*row) for row in data]


def qa_by_subject(id: int):
    data = database.read_query('''
            SELECT q.id, u.username, q.question, q.answer, s.subject
            FROM q_a q JOIN users u ON q.author_id = u.id
            JOIN qa_subjects s ON q.qa_subjects_id = s.id
            WHERE q.qa_subjects_id = ?''', (id,))

    return [QA.from_query_result(*row) for row in data]


def create_qa(user_id: int, new_qa: QABody):
    id = database.insert_query('''INSERT INTO q_a(author_id, answer, qa_subjects_id, question)
            VALUES (?,?,?,?)''', (user_id, new_qa.answer, new_qa.qa_subject_id, new_qa.question))
    
    return True if id else False