from pydantic import BaseModel, PositiveInt, Field


class Article(BaseModel):
    number: PositiveInt = Field(lt=10**12)


class Good(BaseModel):
    article: PositiveInt = Field(lt=10**12)
    title: str = Field(min_length=1)
    category: str
    price: int = Field(gt=0)
    pictures: list[str]
    specs: dict[str, str]
    description: str = Field(min_length=1)
    rating: float
    feedbacks: int
