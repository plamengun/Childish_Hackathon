from data import database
from data.models import JobAd, JobAdRepr


def create(user_id: int, job_descr: JobAd):
    generated_id = database.insert_query('''
        INSERT INTO job_posts(user_id, city_id, job_description, job_sectors_id, employment_type_id)
        VALUES (?,?,?,?,?)''', (user_id, job_descr.city_id, job_descr.description, job_descr.sector_id, job_descr.type_id))

    if generated_id:
        return create_jobad_repr(generated_id) 


def update_job(job_id: int, job_descr: JobAd):
    try:
        database.insert_query('''
        UPDATE job_posts SET city_id = ?, job_description = ?, job_sectors_id = ?, employment_type_id = ?)
        WHERE id = ?''', (job_descr.city_id, job_descr.description, job_descr.sector_id, job_descr.type_id, job_id))

        return create_jobad_repr(job_id)

    except:
        return None


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


def view_jobs(city_id: str|None, sector_id: str|None, type_id: str|None, search: str, offset: int, limit: int):
    if city_id:
        if sector_id:
            if type_id:
                data = _get_jobs_by_city_sector_type(int(city_id), int(sector_id), int(type_id), search, offset, limit)
            else:
                data = _get_jobs_by_city_sector(int(city_id), int(sector_id), search, offset, limit)
        else:
            if type_id:
                data = _get_jobs_by_city_type(int(city_id), int(type_id), search, offset, limit)
            else:
                data = _get_jobs_by_city(int(city_id), search,  offset, limit)
    else:
        if sector_id:
            if type_id:
                data = _get_jobs_by_sector_type(int(sector_id), int(type_id), search,  offset, limit)
            else:
                data = _get_jobs_by_sector(int(sector_id), search,  offset, limit)
        else:
            if type_id:
                data = _get_jobs_by_type(int(type_id), search,  offset, limit)
            else:
                data = _get_jobs_all(search)

    return [JobAdRepr.from_query_result(*row) for row in data]



def _get_jobs_by_city_sector_type(city_id: int, sector_id: int, type_id: int, search: str, offset: int, limit: int):
    if search:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.city_id = ? AND j.job_sectors_id = ? AND j.employment_type_id = ? AND j.job_description LIKE ?
            LIMIT ? OFFSET ?''',
            (city_id, sector_id, type_id, f'%{search}%', limit, offset))
    else:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.city_id = ? AND j.job_sectors_id = ? AND j.employment_type_id = ?
            LIMIT ? OFFSET ?''',
            (city_id, sector_id, type_id, limit, offset))
    return data


def _get_jobs_by_city_sector(city_id: int, sector_id: int, search: str, offset: int, limit: int):
    if search:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.city_id = ? AND j.job_sectors_id = ? AND j.job_description LIKE ?
            LIMIT ? OFFSET ?''',
            (city_id, sector_id, f'%{search}%', limit, offset))
    else:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.city_id = ? AND j.job_sectors_id = ?
            LIMIT ? OFFSET ?''',
            (city_id, sector_id, limit, offset))
    return data


def _get_jobs_by_city_type(city_id: int, type_id:int, search:str, offset: int, limit: int):
    if search:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.city_id = ? AND j.employment_type_id = ? AND j.job_description LIKE ?
            LIMIT ? OFFSET ?''',
            (city_id, type_id, f'%{search}%', limit, offset))
    else:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.city_id = ? AND j.employment_type_id = ?
            LIMIT ? OFFSET ?''',
            (city_id, type_id, limit, offset))
    return data


def _get_jobs_by_city(city_id: int, search: str, offset: int, limit: int):
    if search:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.city_id = ? AND j.job_description LIKE ?
            LIMIT ? OFFSET ?''',
            (city_id, f'%{search}%', limit, offset))
    else:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.city_id = ?
            LIMIT ? OFFSET ?''',
            (city_id, limit, offset))
    return data


def _get_jobs_by_sector_type(sector_id: int, type_id:int, search: str, offset: int, limit: int):
    if search:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.job_sectors_id = ? AND j.employment_type_id = ? AND j.job_description LIKE ?
            LIMIT ? OFFSET ?''',
            (sector_id, type_id, f'%{search}%', limit, offset))
    else:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.job_sectors_id = ? AND j.employment_type_id = ?
            LIMIT ? OFFSET ?''',
            (sector_id, type_id, limit, offset))
    return data

def _get_jobs_by_sector(sector_id: int, search: str, offset: int, limit: int):
    if search:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.job_sectors_id = ? AND j.job_description LIKE ?
            LIMIT ? OFFSET ?''',
            (sector_id, f'%{search}%', limit, offset))
    else:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.job_sectors_id = ?
            LIMIT ? OFFSET ?''',
            (sector_id, limit, offset))
    return data


def _get_jobs_by_type(type_id: int, search: str, offset: int, limit: int):
    if search:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.employment_type_id = ? AND j.job_description LIKE ?
            LIMIT ? OFFSET ?''',
            (type_id, f'%{search}%', limit, offset))
    else:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.employment_type_id = ?
            LIMIT ? OFFSET ?''',
            (type_id, limit, offset))
    return data


def _get_jobs_all(search: str, offset: int, limit: int):
    if search:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            WHERE j.job_description LIKE ?
            LIMIT ? OFFSET ?''',
            (f"%{search}%", limit, offset))
    else:
        data = database.read_query('''
            SELECT j.id, u.id, u.username, c.name, s.sector_name, e.type_name, j.job_description
            FROM job_posts j 
            JOIN users u ON j.user_id = u.id
            JOIN cities c ON j.city_id = c.id
            JOIN job_sectors s ON j.job_sectors_id = s.id
            JOIN employment_type e ON j.employment_type_id = e.id
            LIMIT ? OFFSET ?''', (limit, offset))

    return data