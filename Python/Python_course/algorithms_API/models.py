from sqlmodel import SQLModel, Field


class Request(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    operation: str = Field(description="The operation performed")
    number: int = Field(description="The number provided by the user")
    result: int = Field(description="The result of the operation")
