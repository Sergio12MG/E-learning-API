from dataclasses import dataclass

@dataclass
class Course:
    id: int
    title: str
    description: str
    user_id: int

