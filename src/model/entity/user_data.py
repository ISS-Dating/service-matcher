from model.entity.base_entity import BaseEntity


class UserData(BaseEntity):
    user_id: int
    gender: str
    country: str
    city: str
    education: str
    status: str
    age: int
    photo_score: float
    was_tried_count: int = 0
    was_liked_count: int = 0

    @property
    def liked_percentage(self) -> float:
        return self.was_liked_count / self.was_tried_count if self.was_tried_count > 0 else 0

    def was_liked(self) -> 'UserData':
        return UserData.construct(
            **self.dict(exclude={'was_tried_count', 'was_liked_count'}),
            was_liked_count=self.was_liked_count + 1, was_tried_count=self.was_tried_count + 1
        )

    def was_disliked(self) -> 'UserData':
        return UserData.construct(
            **self.dict(exclude={'was_tried_count'}),
            was_tried_count=self.was_tried_count + 1
        )
