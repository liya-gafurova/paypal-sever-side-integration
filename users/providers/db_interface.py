from django.contrib.auth import get_user_model

UserModel = get_user_model()


class DB_Creator:
    pass


class DB_Updater:
    pass


class DB_Deleter:
    pass


class DB_Selector:

    @staticmethod
    def get_user_by_id(user_id):
        user = UserModel.objects.get(id=user_id)
        return user
