from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Post
from .models import CarouselSlide
from .models import Projects
from .models import About
from .models import CompanyInfo
from .models import Contacts
from .forms import ContactForm




def home(request):
    slides = CarouselSlide.objects.all()
    latest_projects = Projects.objects.all().order_by('-date')[:3] 
    
    return render(request, 'blog/index.html', {
        'slides': slides,
        'latest_projects': latest_projects,
    })

class ProjectsView(View):
    def get(self, request):
        projects = Projects.objects.all()
        return render(request, 'blog/projects.html', {'projects': projects})


class PostView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/blog.html', {'post_list': posts})
    
class AboutView(View):

    def get(self, request):
        ceo = About.objects.filter(is_ceo=True).first()
        employees = About.objects.filter(is_ceo=False).order_by('order')
        company_info = CompanyInfo.objects.first()
        form = ContactForm()

        return render(request, 'blog/about.html', {
            'ceo': ceo,
            'employees': employees,
            'company_info': company_info,
            'form': form,
        })

    def post(self, request):
        ceo = About.objects.filter(is_ceo=True).first()
        employees = About.objects.filter(is_ceo=False).order_by('order')
        company_info = CompanyInfo.objects.first()

        form = ContactForm(request.POST)

        if form.is_valid():
            Contacts.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )

            messages.success(
                request,
                'Ваша заявка успешно отправлена!'
            )

            return redirect('about')

        return render(request, 'blog/about.html', {
            'ceo': ceo,
            'employees': employees,
            'company_info': company_info,
            'form': form,
        })
    


