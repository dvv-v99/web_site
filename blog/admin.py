from django.contrib import admin
from .models import Post
from .models import CarouselSlide
from .models import Projects
from .models import About
from .models import CompanyInfo
from .models import Contacts


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','date')
    list_display_links = ('title',)
    ordering = ('-date',)
@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title',  'date')  
@admin.register(About)  
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'order')
    list_editable = ('order',)
@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date')
    search_fields = ('name', 'email')
    list_filter = ('date',)