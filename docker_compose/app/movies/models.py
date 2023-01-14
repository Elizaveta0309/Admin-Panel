import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Персона')
        verbose_name_plural = _('Персоны')


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')


class FilmWork(UUIDMixin, TimeStampedMixin):

    class Type(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('Tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(10)],
                               db_index=True)
    type = models.TextField(_('type'), choices=Type.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Кинопроизведение')
        verbose_name_plural = _('Кинопроизведения')
        indexes = [
            models.Index(fields=['type', 'rating'], name='type_rating_idx'),
        ]


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Жанр фильма')
        verbose_name_plural = _('Жанры фильма')
        models.UniqueConstraint(fields=['genre', 'film_work'], name='unique_genre_film_work')


class PersonFilmWork(UUIDMixin):
    class Role(models.TextChoices):
        ACTOR = 'actor', _('Actor'),
        WRITER = 'writer', _('Writer')
        DIRECTOR = 'director', _('Director')

    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    role = models.TextField(_('role'), choices=Role.choices)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Участник фильма')
        verbose_name_plural = _('Участники фильма')
        indexes = [
            models.Index(fields=['film_work', 'person'], name='film_work_person_idx'),
        ]
