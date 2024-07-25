from django.views.generic import TemplateView
from .models import Menu


class IndexView(TemplateView):
    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menus'] = Menu.objects.all()
        return context