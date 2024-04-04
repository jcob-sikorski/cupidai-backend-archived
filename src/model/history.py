from pydantic import BaseModel
from typing import List

class History(BaseModel):
    team_id: str
    images_generated: int
    deepfakes_generated: int
    ai_verification_generated: int
    content_utilities_uses: int
    people_referred: int