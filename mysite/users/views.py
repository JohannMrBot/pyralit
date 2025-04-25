from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults

import colander
from deform import Form, ValidationFailure

from pyramid_sqlalchemy import Session

from mysite.users.model import User

class UserItem(colander.MappingSchema):
    username = colander.SchemaNode(colander.String())
    first_name = colander.SchemaNode(colander.String())
    last_name = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(colander.String())

@view_defaults(permission='view')
class UserView:
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.schema = UserItem()
        self.form = Form(self.schema, buttons=("submit",))
        self.messages = request.session.pop_flash()

    @view_config(route_name='user', renderer='templates/list.jinja2')
    def list(self):
        msg = self.request.params.get('msg')
        return {"users": User.get_all(), "msg": msg}

    @view_config(route_name='user_view', renderer='templates/view.jinja2')
    def view(self):
        return {"user": self.context}

    @view_config(route_name='user_add', renderer='templates/add.jinja2')
    def add(self):
        return {"add_form": self.form.render()}

    @view_config(route_name='user_add', renderer='templates/add.jinja2',
                 request_method='POST')
    def add_post(self):
        controls = self.request.POST.items()
        try:
            validated = self.form.validate(controls)
        except ValidationFailure as e:
            return {"add_form": e.render()}
        Session.add(User(**validated))
        new_user = User.get_by_username(validated['username'])
        msg = f'"{new_user.title}" added'
        self.request.session.flash(msg)
        url = self.request.route_url('user')
        return HTTPFound(url)

    @view_config(route_name='user_edit', renderer='templates/edit.jinja2',
                 request_method='GET', permission='edit')
    def edit(self):
        return {"user": self.context,
                "edit_form": self.form.render(self.context.__dict__)}

    @view_config(route_name='user_edit', renderer='templates/edit.jinja2',
                 request_method='POST', permission='edit')
    def edit_post(self):
        # title = self.request.params.get('title')
        controls = self.request.POST.items()
        try:
            validated = self.form.validate(controls)
        except ValidationFailure as e:
            return {"edit_form": e.render(), "user":self.context}
        self.context.title = validated['title']
        self.request.session.flash(f"{self.context.id} edited")
        url = self.request.route_url('user_view', username=self.context.username)
        return HTTPFound(url)

    @view_config(route_name='user_delete')
    def delete(self):
        self.request.session.flash(f"{self.context.id} deleted")
        url = self.request.route_url('user')
        Session.delete(self.context)
        return HTTPFound(url)

