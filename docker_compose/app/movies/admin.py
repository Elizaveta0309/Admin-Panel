from django.contrib import admin

from .models import Genre
from .models import Person
from .models import FilmWork
from .models import GenreFilmWork
from .models import PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ['genre']


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ['person']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = ('title', 'type', 'creation_date', 'rating',)
    list_filter = ('type',)
    search_fields = ('title',)
