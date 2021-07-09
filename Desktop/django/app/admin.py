from django.contrib import admin
from .models import Category,BlogPost,Comment,Likes,Notifications,Contact
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=('name','slug')
    
@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    list_display=('title','slug','updated_date','views')
    list_filter=('category',)
    fieldsets = (
        (None, {
            'fields': ( 'title', 'body', 'category','slug')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('image', 'views'),
        }),
    )
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('post','user','created_date')

@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display=('post','user','created_date')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=('email','first_name','last_name','send_date')


admin.site.register(Notifications)