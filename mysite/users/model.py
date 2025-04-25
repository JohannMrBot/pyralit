from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import Allow
from sqlalchemy import Column, String, Integer

from pyramid_sqlalchemy import BaseObject, Session
from sqlalchemy.orm import relationship

from mysite.columns.ArrayType import ArrayType

from ..hobbies.model import Hobby

class User(BaseObject):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    password = Column(String(120))
    first_name = Column(String(120))
    last_name = Column(String(120))
    groups = Column(ArrayType)
    todos = relationship('ToDo', back_populates='owner',
                         cascade='all, delete, delete-orphan')
    hobbies = relationship('Hobby', back_populates='owner',
                         cascade='all, delete, delete-orphan')

    def __acl__(self=None):
        acl = [
            (Allow, 'group:admins', ('view', 'edit'))
        ]
        if self is not None:
            # This adds permission to the user to view and edit their own profile
            acl.append((Allow, self.username, ('view', 'edit')))
        return acl

    # Property that can be accessed by templates using {{ context.title }}
    @property
    def title(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_by_username(cls, username):
        return Session.query(cls).filter_by(username=username).first()

    @classmethod
    def get_all(cls):
        return Session.query(cls)

    def __str__(self):
        return f"{self.id}: {self.username} -> {self.groups}"


# This is called for every request that in the config add route has this
# function assigned to the factory parameter
# The returned value is passed to the view constructor as context
def user_factory(request):
    username = request.matchdict.get('username')
    if username is None:
        return User
    user = User.get_by_username(username)
    if not user:
        raise HTTPNotFound()
    return user


sample_users = [
    {'id': 1,
     'username': 'admin',
     'password': 'admin',
     'first_name': 'El Admin',
     'last_name': 'Supremo',
     'groups': ['group:admins', 'group:editors']},
    {'id': 2,
     'username': 'juan',
     'password': '1234',
     'first_name': 'Juan',
     'last_name': 'Zhung',
     'groups': ['group:editors']},
    {'id': 3,
     'username': 'mary',
     'password': '1234',
     'first_name': 'Mary',
     'last_name': 'Piltz',
     'groups': []},
]
