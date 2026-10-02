from django.db import models
from django.utils import timezone


class Post(models.Model):
    """Данные о новости"""

    title = models.CharField(
        'Заголовок записи',
        max_length=100
    )

    description = models.TextField(
        'Текст записи'
    )

    author = models.CharField(
        'Имя автора',
        max_length=100
    )

    date = models.DateField(
        'Дата публикации'
    )

    image = models.ImageField(
        'Изображение',
        upload_to='news/',
        blank=True,
        null=True
    )

    slug = models.SlugField(
        'URL',
        max_length=100,
        unique=True,
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    

class CarouselSlide (models.Model):
    '''Данные о карусели '''
    title = models.CharField('Заголовок', max_length=100)
    subtitle = models.CharField('Подзаголовок', max_length=200, blank=True)
    image = models.ImageField('Изображение', upload_to='carousel/')
    link = models.URLField('Ссылка', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']  
        verbose_name = 'Слайд карусели'
        verbose_name_plural = 'Слайды карусели'

    def __str__(self):
        return self.title


class Projects (models.Model):
    '''Данные о карточках проектов'''
    title = models.CharField('Заголовок записи', max_length=100)
    description = models.TextField('Текст записи')
    image = models.ImageField('Изображение', upload_to='projects/')
    link = models.URLField('Ссылка', blank=True)
    date = models.DateTimeField('Дата реализации', auto_now_add=True,  null=True, blank=True)
    
    

    class Meta:
        ordering = ['-date']
        verbose_name = 'Карточка проекта'
        verbose_name_plural = 'Карточки проектов'

    def __str__(self):
        return self.title
    


class About(models.Model):
    title = models.CharField('ФИО', max_length=100)
    subtitle = models.CharField('Должность', max_length=200, blank=True)
    description = models.TextField('Описание')
    image = models.ImageField('Фото', upload_to='about/')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_ceo = models.BooleanField('Генеральный директор', default=False)  

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    

class CompanyInfo(models.Model):
    title = models.CharField('Заголовок', max_length=200, default='Наша философия')
    text = models.TextField('Описание ценностей')
    background = models.ImageField('Фон (опционально)', upload_to='about/bg/', blank=True, null=True)

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'

    def __str__(self):
        return self.title


class Contacts(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение')
    date = models.DateTimeField('Дата отправки', default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.email})"

