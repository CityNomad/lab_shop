import time


class StatSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        statistics = request.session.get('statistics',
                                         {
                                             'entry_time': time.time(),
                                             'count': 0

                                         })
        statistics['count'] += 1
        request.session['statistics'] = statistics
        return response
