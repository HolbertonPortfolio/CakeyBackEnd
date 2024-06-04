from pydantic import BaseModel, validator


class StepBase(BaseModel):
    description: str
    timer: int
    step_number: int

    @validator('description')
    def description_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Description must not be empty')
        return v


class StepCreate(StepBase):
    pass


class Step(StepBase):
    id: int

    class Config:
        orm_mode = True
