import time

from pyramid.settings import asbool


def time_it(handler, registry):
    if asbool(registry.settings.get('timeit', False)):
        def timing(request):
            start = time.time()
            try:
                result = handler(request)
            finally:
                end = time.time()
            print(f"{handler.__name__} took {end - start} seconds")
            print(f"{request.path_url} -> {result.content_type}")
            print("-"*30)
            return result
        return timing
    return handler
