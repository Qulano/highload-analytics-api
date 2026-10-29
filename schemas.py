from pydantic import BaseModel, Field

class OrderCreateSchema(BaseModel):
    item: str = Field(min_length=2, max_length=100)
    price: int = Field(gt=0)
    client_id: int = Field(gt=0)