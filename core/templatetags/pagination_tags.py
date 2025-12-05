from django import template

register = template.Library()

@register.filter
@register.inclusion_tag('core/partials/pagination.html')
def render_pagination(page_obj):
    pages = []
    current = page_obj.number
    total = page_obj.paginator.num_pages

    if total <= 4:
        pages = list(range(1, total + 1))
    else:
        if current <= 2:
            pages = [1, 2, '...', total]
        elif current >= total - 1:
            pages = [1, '...', total - 1, total]
        else:
            pages = [current, current + 1, '...', total]

    return {
        'page_obj': page_obj,
        'pages': pages
    }
