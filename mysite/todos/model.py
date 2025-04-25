from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import Allow, Everyone, Authenticated
from sqlalchemy import Column, Integer, Text, ForeignKey
from pyramid_sqlalchemy import BaseObject, Session

from sqlalchemy.orm import relationship

from mysite.columns.ArrayType import ArrayType


class ToDo(BaseObject):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    title = Column(Text, unique=True, nullable=False)
    acl = Column(ArrayType) # Object-level security
    default_acl = [
        (Allow, 'group:admins', ('view', 'edit')),
        (Allow, Authenticated, 'add'),
    ]
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', back_populates='todos')

    def __acl__(self=None):
        if self is not None:
            acl = ToDo.default_acl + (self.acl or [])
            acl.append((Allow, self.owner.username, ('view', 'edit')))
            return acl
        print("ToDo acl self not None")
        return getattr(self, 'acl', None) or ToDo.default_acl

# This is called for every request that in the config add route has this
# function assigned to the factory parameter
# The returned value is passed to the view constructor as context
def todo_factory(request):
    todo_id = request.matchdict.get('id')
    if todo_id is None:
        return ToDo
    todo_id = int(todo_id)
    todo = Session.query(ToDo).filter_by(id=todo_id).first()
    if not todo:
        raise HTTPNotFound()
    return todo


sample_todos = [
    {"title": 'Get Milk'},
    {"title": 'Erase board'},
    {"title": "Secure Task",
     "acl": [
         (Allow, 'group:admins', 'view'),
         (Allow, 'group:admins', 'edit')
     ]}
]
