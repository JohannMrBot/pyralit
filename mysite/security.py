import json

from pyramid_sqlalchemy import Session
from sqlalchemy.exc import NoResultFound

from mysite.users.model import User

# This is used as a callback by the authentication policy
# to retrieve the user groups (roles) associated to a user
def group_finder(user: str, request):
    # print(user)
    # user = json.loads(user)
    # return user.get('groups', [])
    groups = []
    try:
        user = User.get_by_username(user)
    except NoResultFound:
        pass
    else:
        groups = user.groups
    return groups