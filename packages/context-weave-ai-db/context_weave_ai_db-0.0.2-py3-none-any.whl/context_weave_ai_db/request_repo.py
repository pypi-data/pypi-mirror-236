from models import Request, Status, UploadPlatform
from setup import session_scope, session_scope_select


class RequestRepo:
    @classmethod
    def add_new(cls, file_id, status: Status,
                upload_platform: UploadPlatform,
                upload_path,
                encrypted_api_key):
        request = Request(
            file_id=file_id,
            status=status,
            upload_platform=upload_platform,
            upload_path=upload_path,
            api_key=encrypted_api_key,
        )
        with session_scope() as session:
            session.add(request)
        return request

    @classmethod
    def update(cls, request: Request, status: Status):
        id = request.id
        with session_scope() as session:
            request.status = status
            session.add(request)
        return cls.get_by_id(id)

    @classmethod
    def get_one_pending_item(cls):
        with session_scope_select() as session:
            res = session.query(Request).filter(
                Request.status == Status.UPLOADED).order_by(Request.created_at).first()
            return res

    @classmethod
    def get_by_id(cls, id: int):
        with session_scope_select() as session:
            res = session.query(Request).filter(Request.id == id).first()
            return res

    @classmethod
    def get_all(cls, status=None):
        with session_scope_select() as session:
            query = session.query(Request)
            if status is not None:
                query = query.filter(Request.status == status)
            res = query.order_by(Request.created_at.desc()).all()
            return res
