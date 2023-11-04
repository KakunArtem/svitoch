from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class DefaultResponse(BaseModel):
    generated: dict
    debug: Optional[Dict[str, Any]] = None


class ModelRequest(BaseModel):
    text: str = Field(..., min_length=1)
    debug: Optional[bool] = Field(default=False, alias="_debug", exclude=True)

