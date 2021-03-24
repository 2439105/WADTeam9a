from django.contrib import admin
from evaluArt.models import UserProfile, ContactUs, Post, comments, Rating, Category

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(comments)
admin.site.register(Rating)
admin.site.register(Category)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'

admin.site.register(ContactUs, ContactUsAdmin)