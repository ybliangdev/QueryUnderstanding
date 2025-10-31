from pydantic import BaseModel, Field


class ParseRequest(BaseModel):
	text: str = Field(..., min_length=1, max_length=2048, description="Raw user query text")


