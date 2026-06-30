from pydantic import BaseModel

class TaskSchema(BaseModel):
    title: str
    description: str
    is_completed: bool = False
    user_id : int | None = 0


## using this schema to return response after creating a task
class TastResponseSchema(BaseModel):
    id: int
    title: str
