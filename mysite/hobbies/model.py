from pyramid.security import Allow, Deny, Everyone
from pyramid_sqlalchemy import BaseObject, Session
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship


class Hobby(BaseObject):
    __tablename__ = 'hobby'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', back_populates='hobbies')

    def __acl__(self=None):
        acl = [
            # (Deny, Everyone, ('view', 'edit')),
            (Allow, 'group:admins', ('view', 'edit'))
        ]
        if self is not None:
            # This adds permission to the user to view and edit their own hobbies
            acl.append((Allow, self.owner.username, ('view', 'edit')))
        return acl

    def __json__(self):
        return {"id": self.id, "name": self.name, "owner": {"id": self.owner_id, "name": self.owner.username}}

    @classmethod
    def get_all(cls):
        return Session.query(cls)

    @classmethod
    def get_by_id(cls, hobby_id):
        return Session.query(cls).filter_by(id=hobby_id)

    @classmethod
    def save(cls, hobby):
        Session.add(hobby)
        Session.flush()
        return hobby

def hobby_factory(request):
    hobby_id = request.matchdict.get('id')
    if hobby_id is None:
        return Hobby
    hobby_id = int(hobby_id)
    hobby = Hobby.get_by_id(hobby_id)
    if hobby is None:
        return Hobby
    return hobby

sample_hobbies = [
    {"name": "Play Guitar"},
    {"name": "Read"},
    {"name": "Work out"},
]