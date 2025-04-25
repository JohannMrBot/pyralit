class hobby_api:
    def __init__(self, request):
        self.request = request

    @property
    def base_template(self):
        settings = self.request.registry.settings
        return settings['hobby.base_template']

def includeme(config):
    config.add_route('hobby', '/',
                     factory='.model.hobby_factory')
    config.add_route('hobby_one', '/{id}',
                     factory='.model.hobby_factory')
    # config.add_route('hobby', '/hobby',
    #                  factory='.hobbies.model.hobby_factory')
    # config.add_route('hobby', '/hobby',
    #                  factory='.hobbies.model.hobby_factory')

    config.add_request_method(hobby_api, reify=True)