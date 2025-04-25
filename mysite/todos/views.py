from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults

import colander
from deform import Form, ValidationFailure

from pyramid_sqlalchemy import Session

from mysite.todos.model import ToDo
from mysite.users.model import User


class ToDoItem(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())

# @view_defaults(permission='view')
class ToDoView:
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.schema = ToDoItem()
        self.form = Form(self.schema, buttons=("submit",))
        self.messages = request.session.pop_flash()

    @view_config(route_name='todo', renderer='templates/list.jinja2')
    def list(self):
        msg = self.request.params.get('msg')
        return {"todos": Session.query(ToDo), "msg": msg}

    @view_config(route_name='todo_view', renderer='templates/view.jinja2')
    def view(self):
        return {"todo": self.context}

    @view_config(route_name='todo_add', renderer='templates/add.jinja2',
                 permission='add')
    def add(self):
        return {"add_form": self.form.render()}

    @view_config(route_name='todo_add', renderer='templates/add.jinja2',
                 request_method='POST',
                 permission='add')
    def add_post(self):
        controls = self.request.POST.items()
        try:
            validated = self.form.validate(controls)
        except ValidationFailure as e:
            return {"add_form": e.render()}
        new_todo = ToDo(title=validated["title"])
        new_todo.owner = User.get_by_username(self.request.authenticated_userid)
        Session.add(new_todo)
        new_todo = Session.query(ToDo).filter_by(title=validated["title"]).one()
        msg = f'"{new_todo.title}" added'
        self.request.session.flash(msg)
        url = self.request.route_url('todo')
        return HTTPFound(url)

    @view_config(route_name='todo_edit', renderer='templates/edit.jinja2',
                 request_method='GET', permission='edit')
    def edit(self):
        return {"todo": self.context,
                "edit_form": self.form.render({"title": self.context.title})}

    @view_config(route_name='todo_edit', renderer='templates/edit.jinja2',
                 request_method='POST', permission='edit')
    def edit_post(self):
        # title = self.request.params.get('title')
        controls = self.request.POST.items()
        try:
            validated = self.form.validate(controls)
        except ValidationFailure as e:
            return {"edit_form": e.render(), "todo":self.context}
        self.context.title = validated['title']
        self.request.session.flash(f"{self.context.id} edited")
        url = self.request.route_url('todo_view', id=self.context.id)
        return HTTPFound(url)

    @view_config(route_name='todo_delete')
    def delete(self):
        self.request.session.flash(f"{self.context.id} deleted")
        url = self.request.route_url('todo')
        Session.delete(self.context)
        return HTTPFound(url)

