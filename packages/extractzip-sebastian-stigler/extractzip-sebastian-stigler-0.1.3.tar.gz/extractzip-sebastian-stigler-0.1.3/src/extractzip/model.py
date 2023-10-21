from dataclasses import dataclass, field
from enum import Enum
from typing import List


class ZipType(Enum):
    Slides: str = "slides"
    Examples: str = "examples"
    Exercises: str = "exercises"
    Solutions: str = "solutions"
    TestExam: str = "testexam"
    Exam: str = "exam"


@dataclass
class Text:
    base_path_error: str
    config_error: str
    course_error: str
    file_error: str
    zip_file_error: str
    already_exists_text: str
    input_text: str
    bad_password: str
    success_text: str


@dataclass
class Lang:
    de: Text | None
    en: Text | None


@dataclass
class Course:
    name: str
    slides: str | None = field(default=None)
    examples: str | None = field(default=None)
    exercises: str | None = field(default=None)
    solutions: str | None = field(default=None)
    testexam: str | None = field(default=None)
    exam: str | None = field(default=None)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def get(self, zip_type: ZipType) -> str | None:
        return getattr(self, zip_type.value)


@dataclass
class Config:
    base_path: str
    courses: List[Course]

    @classmethod
    def from_dict(cls, data):
        return cls(
            base_path=data["base_path"],
            courses=[Course.from_dict(c) for c in data["courses"]],
        )

    def find(self, course: str) -> Course | None:
        """find the course in the courses list"""
        return next(filter(lambda x: x.name == course, self.courses), None)
