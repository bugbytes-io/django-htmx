from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from films.forms import RegisterForm
from films.models import Film, UserFilms
from films.utils import get_max_order, reorder
from django.views.generic.list import ListView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


class FilmList(LoginRequiredMixin, ListView):
    template_name = 'films.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        return UserFilms.objects.filter(user=self.request.user)


def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username already exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available</div>")

@login_required
def add_film(request):
    name = request.POST.get('filmname')
    
    # add film
    film = Film.objects.get_or_create(name=name)[0]
    
    # add the film to the user's list
    if not UserFilms.objects.filter(film=film, user=request.user).exists():
        UserFilms.objects.create(
            film=film, 
            user=request.user, 
            order=get_max_order(request.user)
        )

    # return template fragment with all the user's films
    films = UserFilms.objects.filter(user=request.user)
    messages.success(request, f"Added {name} to list of films")
    return render(request, 'partials/film-list.html', {'films': films})

@require_http_methods(['DELETE'])
@login_required
def delete_film(request, pk):
    ...
    # remove the film from the user's list
    UserFilms.objects.get(pk=pk).delete()

    reorder(request.user)

    # return template fragment with all the user's films
    films = UserFilms.objects.filter(user=request.user)
    return render(request, 'partials/film-list.html', {'films': films})

@login_required
def search_film(request):
    search_text = request.POST.get('search')

    # look up all films that contain the text
    # exclude user films
    userfilms = UserFilms.objects.filter(user=request.user)
    results = Film.objects.filter(name__icontains=search_text).exclude(
        name__in=userfilms.values_list('film__name', flat=True)
    )
    context = {"results": results}
    return render(request, 'partials/search-results.html', context)

def clear(request):
    return HttpResponse("")

def sort(request):
    film_pks_order = request.POST.getlist('film_order')
    films = []
    for idx, film_pk in enumerate(film_pks_order, start=1):
        userfilm = UserFilms.objects.get(pk=film_pk)
        userfilm.order = idx
        userfilm.save()
        films.append(userfilm)

    return render(request, 'partials/film-list.html', {'films': films})

@login_required
def detail(request, pk):
    userfilm = get_object_or_404(UserFilms, pk=pk)
    context = {'userfilm': userfilm}
    return render(request, 'partials/film-detail.html', context)

@login_required
def films_partial(request):
    films = UserFilms.objects.filter(user=request.user)
    return render(request, 'partials/film-list.html', {'films': films})

@login_required
def upload_photo(request, pk):
    userfilm = get_object_or_404(UserFilms, pk=pk)
    print(request.FILES)
    photo = request.FILES.get('photo')
    userfilm.film.photo.save(photo.name, photo)
    context = {'userfilm': userfilm}
    return render(request, 'partials/film-detail.html', context)
