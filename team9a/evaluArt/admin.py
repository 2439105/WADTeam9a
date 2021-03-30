from django.contrib import admin
from evaluArt.models import UserProfile, ContactUs, Artwork, Comments, Rating, Category

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Artwork)
admin.site.register(Comments)
admin.site.register(Rating)
admin.site.register(Category)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'

admin.site.register(ContactUs, ContactUsAdmin)