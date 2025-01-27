from pydantic import BaseModel, PositiveInt, Field


class Good(BaseModel):
    article: PositiveInt = Field(lt=10**12)
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: int = Field(gt=0)
    pictures: list[str]
    specs: dict[str, str]
    description: str = Field(min_length=1)
    rating: float = Field(ge=0, le=5)
    feedbacks: PositiveInt
