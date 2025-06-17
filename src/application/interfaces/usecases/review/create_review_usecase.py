from abc import ABC, abstractmethod

from application.commands.review.create_review_command import (
    CreateReviewCommand,
)
from application.dtos.review.review_dto import ReviewDTO
from application.dtos.user.user_descriptor import UserDescriptor


class ICreateReviewUseCase(ABC):
    @abstractmethod
    def execute(
        self, command: CreateReviewCommand, descriptor: UserDescriptor
    ) -> ReviewDTO: ...
