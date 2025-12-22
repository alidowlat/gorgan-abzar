from django.views.generic import ListView
from django.db.models import Count
from blog.models import Post, PostCategory
from core.actions import apply_filters_blog


class PostListView(ListView):
    model = Post
    template_name = 'blog/list/main.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        mobile_toggles = [
            {'id': 'featured-toggle5', 'name': 'featured', 'label': 'پست های ویژه', 'value': 1,
             'checked': self.request.GET.get('featured') == '1'},
        ]
        context['mobile_toggles'] = mobile_toggles

        desktop_toggles = [
            {'id': 'featured-toggle', 'name': 'featured', 'label': 'پست های ویژه', 'value': 1,
             'checked': self.request.GET.get('featured') == '1'},
        ]
        context['desktop_toggles'] = desktop_toggles

        model_fields = [
            ('categories', PostCategory.objects.filter(is_active=True)),
            ('filtered_posts', apply_filters_blog(self.request, Post.objects.all())),
        ]

        for field_name, queryset in model_fields:
            context[field_name] = queryset

        return context

    def get_queryset(self):
        qs = Post.objects.annotate(
            visit_count=Count('visits', distinct=True)
        )
        filtered_qs = apply_filters_blog(self.request, qs)

        sort_by = self.request.GET.get('sort_by')
        match sort_by:
            case 'most_viewed':
                filtered_qs = filtered_qs.order_by('-visit_count', '-created_at')
            case 'newest':
                filtered_qs = filtered_qs.order_by('-created_at')
            case 'oldest':
                filtered_qs = filtered_qs.order_by('created_at')

        return filtered_qs
