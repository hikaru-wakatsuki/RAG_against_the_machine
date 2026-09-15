import uuid


from pydantic import BaseModel, Field, model_validator, field_validator
from typing import List


def _validate_not_blank(value: str, field_name: str) -> str:
    """Validate that a string is not empty or whitespace-only."""
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty or contain only whitespace")
    return value


class MinimalSource(BaseModel):
    """Represent a character range in a source file."""
    file_path: str
    first_character_index: int = Field(ge=0)
    last_character_index: int = Field(ge=0)

    @field_validator("file_path")
    @classmethod
    def validate_file_path(cls, value: str) -> str:
        """Validate that the file path is not empty."""
        return _validate_not_blank(value, "file_path")

    @model_validator(mode="after")
    def validate_character_range(self) -> "MinimalSource":
        """Validate that the character range is not empty or reversed."""
        if self.last_character_index <= self.first_character_index:
            raise ValueError("last_character_index must be greater than first_character_index")
        return self


class UnansweredQuestion(BaseModel):
    """Represent a question that has not yet been answered."""
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str

    @field_validator("question_id")
    @classmethod
    def validate_question_id(cls, value: str) -> str:
        """Validate that the question ID is not empty."""
        return _validate_not_blank(value, "question_id")

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        """Validate that the question is not empty."""
        return _validate_not_blank(value, "question")


class AnsweredQuestion(UnansweredQuestion):
    """Represent a question with reference sources and an answer."""
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    """Represent a collection of answered or unanswered questions."""
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    """Represent retrieved sources for a single question."""
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]

    @field_validator("question_id")
    @classmethod
    def validate_question_id(cls, value: str) -> str:
        """Validate that the question ID is not empty."""
        return _validate_not_blank(value, "question_id")

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        """Validate that the question is not empty."""
        return _validate_not_blank(value, "question")


class MinimalAnswer(MinimalSearchResults):
    """Represent retrieved sources and a generated answer for one question."""
    answer: str


class StudentSearchResults(BaseModel):
    """Represent retrieval results for a dataset."""
    search_results: List[MinimalSearchResults]
    k: int = Field(ge=0)


class StudentSearchResultsAndAnswer(BaseModel):
    """Represent retrieval results with generated answers for a dataset."""
    search_results: List[MinimalAnswer]
    k: int = Field(ge=0)
