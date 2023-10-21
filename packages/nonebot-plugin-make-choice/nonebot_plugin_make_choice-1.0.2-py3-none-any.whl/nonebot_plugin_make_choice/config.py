from pydantic import BaseModel, Extra

class ChoiceConfig(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""

    choose_both_chance: float = 0.1