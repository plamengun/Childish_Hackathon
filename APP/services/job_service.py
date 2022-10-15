from data import database
from data.models import JobAd, JobAdRepr


def create(user_id: int, job_descr: JobAd):
    generated_id = database.insert_query('''
        INSERT INTO job_posts(user_id, city_id, job_description, job_sectors_id, employment_type_id)
        VALUES (?,?,?,?,?)''', (user_id, job_descr.city_id, job_descr.description, job_descr.sector_id, job_descr.type_id))

    if generated_id:
        return create_jobad_repr(generated_id) 


def create_jobad_repr(job_id: int):
    data = database.read_query_one('''
        SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
        FROM job_posts j 
        JOIN users u ON j.user_id = u.id
        JOIN cities c ON j.city_id = c.id
        JOIN job_sectors s ON j.job_sectors_id = s.id
        JOIN employment_type e ON j.employment_type_id = e.id
        WHERE j.id = ?''', (job_id,))
    return JobAdRepr.from_query_result(*data)