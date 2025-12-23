from django.contrib import admin

from blog.models import PostCategory, Post, PostVisit


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_en', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'title_en')
    prepopulated_fields = {'slug': ('title_en',)}
    ordering = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'is_active',
        'featured',
        'visit_count',
        'created_at'
    )

    list_filter = (
        'is_active',
        'featured',
        'category',
        'created_at'
    )

    search_fields = (
        'title',
        'content'
    )

    prepopulated_fields = {'slug': ('title',)}

    raw_id_fields = ('author',)

    readonly_fields = (
        'created_at',
        'updated_at',
        'visit_count'
    )

    list_editable = (
        'is_active',
        'featured'
    )

    ordering = ('-created_at',)

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('محتوا', {
            'fields': ('image', 'content')
        }),
        ('وضعیت', {
            'fields': ('is_active', 'featured')
        }),
        ('سیستم', {
            'fields': ('created_at', 'updated_at', 'visit_count')
        }),
    )

    def visit_count(self, obj):
        return obj.visits.count()

    visit_count.short_description = 'بازدید'


@admin.register(PostVisit)
class PostVisitAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'ip',
        'user',
        'created_at'
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'ip',
        'user_agent',
        'referer'
    )

    readonly_fields = (
        'post',
        'ip',
        'user',
        'user_agent',
        'referer',
        'created_at'
    )

    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
