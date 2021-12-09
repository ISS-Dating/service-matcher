from model.entity import UserData, UserPreference
from model.database import DAO, transaction


def add_user(user_data: UserData) -> None:
    DAO(UserData).create(user_data)


def add_like(chooser_id: int, liked_user_id: int) -> None:
    user_pref_dao, user_data_dao = DAO(UserPreference), DAO(UserData)

    user_data = user_data_dao.get(UserData.partial(user_id=liked_user_id))
    user_pref = user_pref_dao.get(UserPreference.partial(user_id=chooser_id))

    user_pref = (user_pref.add_like(user_data) if user_pref
                 else UserPreference.from_user_data(chooser_id, user_data))
    user_data = user_data.was_liked()

    with transaction(user_pref_dao, user_data_dao):
        user_pref_dao.replace(UserPreference.partial(user_id=user_pref.user_id), user_pref)
        user_data_dao.update(UserData.partial(user_id=user_data.user_id), user_data)


def add_dislike(disliked_user_id: int) -> None:
    user_data_dao = DAO(UserData)

    user_data = user_data_dao.get(UserData.partial(user_id=disliked_user_id))
    user_data = user_data.was_disliked()

    user_data_dao.update(UserData.partial(user_id=user_data.user_id), user_data)


