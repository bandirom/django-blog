from main.views import TemplateAPIView


class BlogListView(TemplateAPIView):
    template_name = 'blog/post_list.html'


class BlogDetailView(TemplateAPIView):
    template_name = 'blog/detail.html'
