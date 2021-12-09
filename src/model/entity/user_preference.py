from typing import Iterable
from collections import Counter

from model.entity.base_entity import BaseEntity
from model.entity.variable_stats import VariableStats
from model.entity.user_data import UserData


class UserPreference(BaseEntity):
    user_id: int
    gender: Counter
    countries: Counter
    cities: Counter
    education_types: Counter
    status: Counter
    age: VariableStats
    photo_score: VariableStats
    liked_percentage: VariableStats

    @classmethod
    def from_user_data(cls, user_id: int, user_data: UserData) -> 'UserPreference':
        return cls(
            user_id=user_id,
            gender=Counter([user_data.gender]),
            countries=Counter([user_data.country]),
            cities=Counter([user_data.city]),
            education_types=Counter([user_data.education]),
            status=Counter([user_data.status]),
            age=VariableStats.from_value(user_data.age),
            photo_score=VariableStats.from_value(user_data.photo_score),
            liked_percentage=VariableStats.from_value(user_data.liked_percentage),
        )

    def add_like(self, user_data: UserData) -> 'UserPreference':
        return UserPreference.construct(
            user_id=self.user_id,
            gender=_update_counter(self.gender, [user_data.gender]),
            countries=_update_counter(self.countries, [user_data.country]),
            cities=_update_counter(self.cities, [user_data.city]),
            education_types=_update_counter(self.education_types, [user_data.education]),
            status=_update_counter(self.status, [user_data.status]),
            age=self.age.add_value(user_data.age),
            photo_score=self.photo_score.add_value(user_data.photo_score),
            liked_percentage=self.liked_percentage.add_value(user_data.liked_percentage)
        )


def _update_counter(counter: Counter, iterable: Iterable[str]) -> Counter:
    updated_counter = counter.copy()
    updated_counter.update(iterable)
    return updated_counter
