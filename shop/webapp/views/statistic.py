from django.views.generic import TemplateView
import time, datetime


class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics = self.request.session['statistics']
        now = time.time()
        seconds = statistics['entry_time']
        time_diff = now - seconds
        time_format = str(datetime.timedelta(seconds=time_diff))
        context['statistics'] = {'time': time_format, 'count': statistics['count']}
        return context
