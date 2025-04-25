from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid_sqlalchemy import metadata
from sqlalchemy import create_engine

from .security import group_finder

def main(global_config, **settings):
    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
        callback=group_finder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          authorization_policy=authz_policy,
                          authentication_policy=authn_policy)

    config.include('pyramid_jinja2')
    config.include('.hobbies', "hobby")
    config.scan()
    config.include('pyramid_sqlalchemy')
    config.add_static_view('static', 'mysite:static')
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')


    config.add_route('todo', '/todo',
                     factory='.todos.model.todo_factory')
    config.add_route('todo_add', '/todo/add',
                     factory='.todos.model.todo_factory')
    config.add_route('todo_view', 'todo/{id}',
                     factory='.todos.model.todo_factory')
    config.add_route('todo_edit', 'todo/{id}/edit',
                     factory='.todos.model.todo_factory')
    config.add_route('todo_delete', 'todo/{id}/delete',
                     factory='.todos.model.todo_factory')

    config.add_route('user', '/user',
                     factory='.users.model.user_factory')
    config.add_route('user_add', '/user/add',
                     factory='.users.model.user_factory')
    config.add_route('user_view', 'user/{username}',
                     factory='.users.model.user_factory')
    config.add_route('user_edit', 'user/{username}/edit',
                     factory='.users.model.user_factory')
    config.add_route('user_delete', 'user/{username}/delete',
                     factory='.users.model.user_factory')

    config.add_route('greeting', '/greeting')

    metadata.create_all(create_engine(settings['sqlalchemy.url']))

    session_secret = settings['session.secret']
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)

    config.add_tween('.timeit.time_it')

    return config.make_wsgi_app()
