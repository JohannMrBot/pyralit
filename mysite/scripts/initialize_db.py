import os
import sys
import transaction

from pyramid_sqlalchemy import Session
from pyramid.config import Configurator
from pyramid_sqlalchemy.meta import metadata
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import create_engine

from mysite.todos.model import ToDo, sample_todos
from mysite.users.model import User, sample_users
from mysite.hobbies.model import Hobby, sample_hobbies

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    config = Configurator(settings=settings)
    config.include('pyramid_sqlalchemy')

    with transaction.manager:
        metadata.create_all(create_engine(settings['sqlalchemy.url']))

        for user in sample_users:
            u = User(username=user["username"],
                     password=user["password"],
                     first_name=user["first_name"],
                     last_name=user["last_name"],
                     groups=user["groups"])
            Session.add(u)

        owner = User.get_by_username(sample_users[0]["username"])

        for todo in sample_todos:
            t = ToDo(title=todo["title"],
                     acl=todo.get('acl'))
            t.owner = owner
            Session.add(t)

        for hobby in sample_hobbies:
            h = Hobby(name=hobby["name"])
            h.owner = owner
            Session.add(h)


