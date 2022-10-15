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