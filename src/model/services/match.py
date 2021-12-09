from collections import Counter

from model.entity import UserData, UserPreference, VariableStats
from model.database import DAO


def _normalize_counter(counter: Counter) -> dict[str, float]:
    [(_, max_),] = counter.most_common(1)
    return {key: value / max_ for key, value in counter.items()}


def _score_data_by_preference(user_data: UserData, user_pref: UserPreference) -> float:
    def counter_score(counter: Counter, value: str) -> float:
        return _normalize_counter(counter).get(value, 0)

    def variable_stats_score(stats: VariableStats, value: float) -> float:
        return value / stats.mean

    gender_score = counter_score(user_pref.gender, user_data.gender)
    country_score = counter_score(user_pref.countries, user_data.country)
    city_score = counter_score(user_pref.cities, user_data.city)
    education_score = counter_score(user_pref.education_types, user_data.education)
    status_score = counter_score(user_pref.status, user_data.status)
    age_score = variable_stats_score(user_pref.age, user_data.age)

    return gender_score + country_score + city_score + education_score + status_score + age_score


def calc_matching_score(first_user_id: int, second_user_id: int) -> float:
    user_pref_dao, user_data_dao = DAO(UserPreference), DAO(UserData)

    first_user_data = user_data_dao.get(UserData.partial(user_id=first_user_id))
    second_user_data = user_data_dao.get(UserData.partial(user_id=second_user_id))
    first_user_pref = user_pref_dao.get(UserPreference.partial(user_id=first_user_id))
    second_user_pref = user_pref_dao.get(UserPreference.partial(user_id=second_user_id))

    return min(_score_data_by_preference(first_user_data, second_user_pref),
               _score_data_by_preference(second_user_data, first_user_pref))







