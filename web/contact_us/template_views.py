from main.views import TemplateAPIView


class ContactUsView(TemplateAPIView):
    template_name = 'contact_us/index.html'
