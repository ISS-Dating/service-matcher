from model.database import DAO
from model.entity import UserData, UserPreference


def main() -> None:
    #dao = DAO(UserPreference)
    data = UserData(user_id=1,
                    gender='g',
                    country='c',
                    city='c',
                    education='e',
                    status='s',
                    age=2,
                    photo_score=1)
    print(data.liked_percentage)
    print(data.was_liked().was_disliked().was_liked().was_liked().liked_percentage)
    # print(dao.get(UserPreference.partial(user_id=1)))


if __name__ == '__main__':
    main()
