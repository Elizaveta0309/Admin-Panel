from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import FilmWork, GenreFilmWork, Person, PersonFilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        is_actor = Q(personfilmwork__role=PersonFilmWork.Role.ACTOR)
        is_writer = Q(personfilmwork__role=PersonFilmWork.Role.WRITER)
        is_director = Q(personfilmwork__role=PersonFilmWork.Role.DIRECTOR)
        queryset = FilmWork.objects.prefetch_related('genres', 'persons').values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type').annotate(
            genres=ArrayAgg('genres__name', distinct=True)).filter(
            is_actor).annotate(actors=ArrayAgg('persons__full_name', distinct=True)).filter(
            is_writer).annotate(writers=ArrayAgg('persons__full_name', distinct=True)).filter(
            is_director).annotate(directors=ArrayAgg('persons__full_name', distinct=True))

        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )
        if page.has_previous():
            prev = page.previous_page_number()
        else:
            prev = 20  # как бы по кругу идет, перед единичкой будет последняя 20ая страница
        if page.has_next():
            next = page.next_page_number()
        else:
            next = 1  # а следующей после 20ой 1ая
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            "prev": prev,
            "next": next,
            'results': list(paginator.get_page(page.number))
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        context = {
            'results': self.get_queryset().get(pk=self.kwargs.get('pk'))
        }
        return context
