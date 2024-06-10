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

    @validator('step_number')
    def step_number_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Step number must be a positive integer')
        return v


class StepCreate(StepBase):
    pass


class Step(StepBase):
    id: int

    class Config:
        orm_mode = True
