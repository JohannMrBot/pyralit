from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import forbidden_view_config, notfound_view_config, view_config
from pyramid_sqlalchemy import Session
from sqlalchemy.exc import NoResultFound

from mysite.users.model import User

import json


class ToDoView:
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.messages = request.session.pop_flash()

    @forbidden_view_config(renderer='templates/forbidden.jinja2')
    def forbidden(self):
        return {}

    @notfound_view_config(renderer='templates/notfound.jinja2')
    def notfound(self):
        return dict()

    @view_config(route_name='home', renderer='templates/home.jinja2')
    def home(self):
        return {}

    @view_config(route_name='login', renderer='templates/login.jinja2')
    def login(self):
        return {}

    @view_config(route_name='login', renderer='templates/login.jinja2',
                 request_method = 'POST')
    def login_post(self):
        request = self.request
        username = request.params.get('username')
        password = request.params.get('password')
        try:
            user = Session.query(User).filter_by(username=username).one()
            if user and user.password == password:
                # info = json.dumps({'username': username, 'groups': user.groups})
                headers = remember(request, username)
                return HTTPFound(location=request.route_url('home'),
                                 headers=headers)
        except NoResultFound:
            return {"form_error": 'Invalid username or password',
                    'username': username}

    @view_config(route_name='logout')
    def logout(self):
        headers = forget(self.request)
        return HTTPFound(
            location=self.request.route_url('home'),
            headers=headers)

    @view_config(route_name='greeting', renderer='templates/greeting.jinja2')
    def greeting(self):
        return {}

    @view_config(route_name='greeting', renderer='json', request_method='POST')
    def greeting_post(self):
        name = self.request.json_body.get('name')
        return {'greeting': f'Hello, {name}!'}
