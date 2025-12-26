from django.shortcuts import render
from blog.models import Post
from product.models import Product
from search.models import SearchQuery


def search_view(request):
    query = request.GET.get('search', '').strip()

    results = {
        'posts': [],
        'products': [],
    }

    if query and len(query) >= 2:
        results['posts'] = Post.objects.filter(title__icontains=query)[:7]
        results['products'] = Product.objects.filter(title__icontains=query)[:7]

        SearchQuery.objects.create(
            query=query[:255],
            user=request.user if request.user.is_authenticated else None
        )

    return render(request, 'search/components/search_result.html', {'results': results})
