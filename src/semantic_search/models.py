from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    id: str = Field(min_length=1)
    content: str
    score: float
    source: str = Field(min_length=1)
