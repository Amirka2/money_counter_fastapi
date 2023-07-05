from schemas import schemas


def is_admin(user: schemas.User):
    return user.is_admin
