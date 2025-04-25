import colander
from deform import Form, ValidationFailure
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from mysite.hobbies.model import Hobby
from mysite.users.model import User


class HobbyItem(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())

class HobbiesView:
    def __init__(self, context, request):
        self.request = request
        self.context = context
        self.schema = HobbyItem()
        self.form = Form(self.schema)
        self.messages = request.session.pop_flash()

    @view_config(route_name='hobby', renderer='templates/list2.jinja2',
                 request_method='GET')
    def hobby_list(self):
        return {"add_form": self.form.render(),
                "hobbies": Hobby.get_all()}

    @view_config(route_name='hobby', renderer='json',
                 request_method='POST')
    def hobby_add(self):
        name = self.request.json_body.get('name', "")
        if name is None or len(name) == 0:
            return Response(
                status="400",
                reason="Name is required"
            )

        hobby = Hobby(name=name)
        hobby.owner = User.get_by_username(self.request.authenticated_userid)

        created = Hobby.save(hobby).__json__()
        created["href"] = self.request.route_url('hobby_one', id=created["id"])
        created["owner"]["href"] = self.request.route_url('hobby_owner', id=hobby.owner.id)

        return created

    @view_config(route_name='hobby_one', renderer='json', request_method='PATCH')
    def hobby_one(self, id):
        name = self.request.json_body.get('name', "")
        if name is None or len(name) == 0:
            return Response(
                status="400",
                reason="Name is required"
            )
        self.context["name"] = name
        Hobby.save(self.context)
