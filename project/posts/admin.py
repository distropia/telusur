from django.contrib import admin
from tags_input import admin as tags_input_admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Post, Tag, Attachment, Category


class PostAdmin(tags_input_admin.TagsInputAdmin):
    list_display = ('title', 'author', 'publish')
    list_display_links = ('title', )
    list_filter = ('publish', 'author')
    search_fields = ('title', )
    tag_fields = ('tags', 'categories')


UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Attachment)
admin.site.register(Category)
