from pydantic import BaseModel


class BaseVo(BaseModel):
    def __str__(self) -> str:
        return repr(self)
