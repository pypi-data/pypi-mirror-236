from pydantic import BaseModel

class Config(BaseModel):
    """Plugin Config Here"""
    choose_both_chance: float = 0.1