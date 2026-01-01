from pydantic import BaseModel

class PortalResponse(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True
