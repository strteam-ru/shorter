from ..logger import logger
from ..models import Users


class User:

    @staticmethod
    def get_user(user) -> Users:
        if user:
            logger.info('detected user - {}'.format('user'))
            return Users.objects.get(id=user)
        else:
            user = Users()
            user.save()
            logger.info('created new user - {}'.format(user.id))
            return user
