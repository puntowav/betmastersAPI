from pydantic import BaseModel
from datetime import date

class Bet(BaseModel):
    id: int
    partido: str
    team: str
    bet: str
    win: str