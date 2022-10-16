from fastapi import APIRouter, Header

from common.auth import get_user_or_raise_401
from common.responses import Unauthorized, BadRequest
from data.models import Tags, QA, QAsubject, QABody
from services import qa_services
from services import user_service


qa_router = APIRouter(prefix='/q&a')


@qa_router.get('/', response_model=list[QA], tags=[Tags.qa])
def get_all_qa():
    result = qa_services.qa_all()

    return result


@qa_router.get('/subjects', response_model=list[QAsubject], tags=[Tags.qa])
def get_qa_subjects():
    result = qa_services.all_subjects()

    return result


@qa_router.get('/subjects/{id}', response_model=list[QA], tags=[Tags.qa])
def get_qa_by_subject(id: int):
    result = qa_services.qa_by_subject(id)

    return result


@qa_router.post('/new', tags=[Tags.qa])
def create_new_qa(new_qa: QABody, token=Header()):
    user = get_user_or_raise_401(token)
    if user_service.get_user_type(user.id) != 'mentor':
        return Unauthorized('User should be mentor')

    result = qa_services.create_qa(user.id, new_qa)

    if result:
        return 'Posted.'
    else:
        BadRequest('Something happened.')