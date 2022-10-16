from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest
from data.models import Tags, JobAd, JobAdRepr, Cities, JobSectors, EmplType
from services import job_service
from services import user_service

jobs_router = APIRouter(prefix='/jobs')

@jobs_router.post('/', response_model=JobAdRepr, tags=[Tags.jobs])
def create(job_descr: JobAd, token = Header()):
    user = get_user_or_raise_401(token)
    if user_service.get_user_type(user.id) != 'employer':
        return BadRequest('User is not an employer')

    job_ad = job_service.create(user.id, job_descr)
    return job_ad


@jobs_router.get('/', tags=[Tags.jobs])
def view_jobs(city_id: Cities | None = None, sector_id: JobSectors | None = None, type_id: EmplType| None = None, search: str| None = None, offset: int = 0, limit: int = 10):

    job_ads = job_service.view_jobs(city_id, sector_id, type_id, search, offset, limit)

    return job_ads


@jobs_router.put('/{id}', response_model=JobAdRepr, tags=[Tags.jobs])
def update(id: int, job_descr: JobAd, token = Header()):
    user = get_user_or_raise_401(token)
    if user_service.get_user_type(user.id) != 'employer':
        return BadRequest('User is not an employer')

    job_ad = job_service.update_job(job_id=id, job_descr=job_descr)
    return job_ad or BadRequest(content='Database constrains are violated')