from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, Enum, UUID
import uuid

Base = declarative_base()


class Status(Enum):
    PENDING = 0
    UPLOADED = 10
    PROCESSING = 15
    COMPLETED = 20
    FAILED = 30

    @classmethod
    def to_dict(cls):
        return {
            cls.PENDING: "Pending",
            cls.UPLOADED: "Uploaded",
            cls.PROCESSING: "Processing",
            cls.COMPLETED: "Completed",
            cls.FAILED: "Failed",
        }

    @classmethod
    def get_str(cls, id):
        return cls.to_dict()[id]


class UploadPlatform(Enum):
    NOT_DEFINED = 0
    LOCAL = 10
    S3 = 20

    @classmethod
    def to_dict(cls):
        return {
            cls.NOT_DEFINED: "NA",
            cls.LOCAL: "Local",
            cls.S3: "S3",
        }


class Request(Base):
    __tablename__ = 'requests'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    file_id = Column(String(255))
    status = Column(Integer, default=Status.PENDING)
    upload_platform = Column(Integer,
                             default=UploadPlatform.NOT_DEFINED)
    upload_path = Column(String(255))
    api_key = Column(String(1024))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(),
                        onupdate=func.now())

    def __repr__(self):
        return f"<Request(id={self.id}, file_id={self.file_id}, status={self.status}, " \
               f"upload_platform={self.upload_platform}, upload_path={self.upload_path}, " \
               f"created_at={self.created_at}, updated_at={self.updated_at})>"


class RequestByUrl(Base):
    __tablename__ = 'request_by_urls'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    url = Column(String(1024))
    status = Column(Integer, default=Status.PENDING)
    api_key = Column(String(1024))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(),
                        onupdate=func.now())

    def __repr__(self):
        return f"<RequestByUrl(id={self.id}, url={self.url}, status={self.status}, " \
               f"created_at={self.created_at}, updated_at={self.updated_at})>"
