from .models import RequestByUrl, Status
from .setup import session_scope, session_scope_select


class RequestByUrlRepo:
    @classmethod
    def add_new(cls, url,
                status: Status,
                encrypted_api_key):
        request = RequestByUrl(
            url=url,
            status=status,
            api_key=encrypted_api_key,
        )
        with session_scope() as session:
            session.add(request)
        return request

    @classmethod
    def update(cls, request: RequestByUrl, status: Status):
        id = request.id
        with session_scope() as session:
            request.status = status
            session.add(request)
        return cls.get_by_id(id)

    @classmethod
    def get_one_pending_item(cls):
        with session_scope_select() as session:
            res = session.query(RequestByUrl).filter(
                RequestByUrl.status == Status.PENDING).order_by(RequestByUrl.created_at).first()
            return res

    @classmethod
    def get_by_id(cls, id: int):
        with session_scope_select() as session:
            res = session.query(RequestByUrl).filter(RequestByUrl.id == id).first()
            return res

    @classmethod
    def get_all(cls, status=None):
        with session_scope_select() as session:
            query = session.query(RequestByUrl)
            if status is not None:
                query = query.filter(RequestByUrl.status == status)
            res = query.order_by(RequestByUrl.created_at.desc()).all()
            return res
