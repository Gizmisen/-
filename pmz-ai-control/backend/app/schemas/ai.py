from pydantic import BaseModel


class AIQueryRequest(BaseModel):
    query: str


class AIQueryResponse(BaseModel):
    answer: str
    data: dict | list | None = None
