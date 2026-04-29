from pydantic import BaseModel


class AIQueryRequest(BaseModel):
    query: str
    advanced: bool = True


class AIQueryResponse(BaseModel):
    answer: str
    data: dict | list | None = None
    mode: str = "local"
