from pydantic import BaseModel


# Talep modeli
class Request(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_by: str

# Yeni talep oluşturma için gerekli model
class RequestCreate(BaseModel):
    title: str
    description: str
    created_by: str