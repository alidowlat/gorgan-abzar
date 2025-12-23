from django.views.generic import DetailView
from blog.models import Post, PostVisit, PostCategory
from core.clean import create_visit_clean
from core.http_service import get_request_client_info


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail/main.html'

    def get_queryset(self):
        return (
            Post.objects
            .select_related('category', 'author')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model_fields = [
            ('latest_posts', Post.objects.select_related('category').filter(
                category_id=self.object.category_id).exclude(id=self.object.id).order_by('-created_at').distinct()[:4]
             ),
            ('categories', PostCategory.objects.filter(is_active=True).order_by('-id')[:5]),
        ]
        for field_name, queryset in model_fields:
            context[field_name] = queryset

        create_visit_clean(
            user=self.request.user,
            model=PostVisit,
            request=self.request,
            fk_name='post',
            http_service=get_request_client_info,
            loaded_obj=self.object,
        )

        return context
