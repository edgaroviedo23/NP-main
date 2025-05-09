from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistroForm, LoginForm, PostForm, CommentForm  # Importamos el CommentForm correctamente
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Tag, Comment
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
#imports para API terceros y cache
import requests
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


# vistas genericas para trabajar CRUD


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"

class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object  # Asociamos el comentario al post
            comment.author = request.user  # Asociamos el comentario al autor
            comment.save()  # Guardamos el comentario
            messages.success(request, "Comentario añadido con éxito")
            return HttpResponseRedirect(self.get_success_url())  # Redirige a la página de detalles del post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm  
    template_name = "post_create.html"
    success_url = reverse_lazy('post_list')
    login_url = "login.html"

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            messages.error(request, "No tienes permiso para editar este post.")
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            messages.error(request, "No puedes eliminar un post que no es tuyo.")
            return redirect(self.success_url)  # Cambié a `redirect` aquí
        return super().dispatch(request, *args, **kwargs)

# resto del código de vistas (Tag, etc.)...

class TagListView(ListView):
    model = Tag
    template_name = "tag_list.html"

class TagCreateView(CreateView):
    model = Tag
    fields = ['name']
    template_name = "tag_create.html"
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)  # ⚠️ Guardamos sin aplicar los tags todavía
        self.object.save()  # Guardamos el post
        form.save_m2m()     # ✅ Ahora sí guardamos los tags correctamente
        return super().form_valid(form)

class TagDeleteView(DeleteView):
    model = Tag
    template_name = 'tag_confirm_delete.html'
    success_url = reverse_lazy('tag_list')

class PostbyTagView(ListView):
    model = Post
    template_name= "post_list_by_tag.html"

# Funciones para login, registro, logout, etc.
def home(request):
    return render(request, 'home.html')

def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Correo no registrado")
                return redirect('login')
            
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
                login(request, user_auth)
                messages.success(request, "Has iniciado sesión correctamente")
                return redirect('home')
            else:
                messages.success(request, "Contraseña incorrecta")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def registroView(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Inicia sesión")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def logoutView(request):
    logout(request)
    messages.info(request, "Has cerrado sesión. Vuelve pronto!")
    return redirect('home')

def politica_cookies(request):
    return render(request, 'politica_cookies.html')


# Vistas para API de terceros OPENWEATHER

#@cache_page(60 * 30)  # Cache por 15 minutos

def weather(request):
    city = request.GET.get('city', 'santander')
    params = {
        'q': city,
        'units': 'metric',
        'appid': settings.OWM_KEY,
        'lang': 'es'
    }
    r = requests.get(
        'https://api.openweathermap.org/data/2.5/weather',
        params=params, timeout=5
    )
    data = r.json()
    respuesta = {
        'city': data['name'],
        'temp': data['main']['temp'],
        'icon': data['weather'][0]['icon'],
        'desc': data['weather'][0]['description'],
    }
    return JsonResponse(respuesta)

# api counrty

def pais_info(request):
    nombre_pais = request.GET.get('pais', 'España')
    url = f"https://restcountries.com/v3.1/name/{nombre_pais}"

    try:
        response = requests.get(url)
        data = response.json()[0]

        contexto = {
            'nombre': data['name']['common'],
            'capital': data['capital'][0] if 'capital' in data else 'No disponible',
            'poblacion': data['population'],
            'area': data['area'],
            'moneda': list(data['currencies'].keys())[0],
            'bandera': data['flags']['png'],
        }
    except Exception:
        contexto = {
            'error': 'No se pudo obtener información del país.'
        }
    return render(request, 'pais.html', contexto)

# API PELICULAS

import requests
from django.conf import settings
from django.shortcuts import render

def peliculas(request):
    query = request.GET.get('query', '')  
    api_key = settings.NUEVO_API_KEY  
    page = request.GET.get('page', 1)
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}&page={page}'
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        
        data = response.json()
        
        if data['results']:
            contexto = {
                'peliculas': data['results'],
                'query': query,
                'page': page, 
                'total_pages': data['total_pages'], 
                'video' : True,
            }
        else:
            contexto = {'error': 'No se encontraron películas.'}
    
    except requests.exceptions.RequestException as e:
        contexto = {'error': f'Error al conectar con la API: {str(e)}'}
    
    return render(request, 'peliculas.html', contexto)


# API DE ROBERTO:

def recipe(request):
    try:
        response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=5)
        data = response.json()
        meal = data['meals'][0]

        respuesta = {
            'name': meal['strMeal'],
            'category': meal['strCategory'],
            'area': meal['strArea'],
            'instructions': meal['strInstructions'],
            'image': meal['strMealThumb'],
            'tags': meal['strTags'],
            'youtube': meal['strYoutube'],
        }
    except Exception as e:
        respuesta = {
            'error': 'No se pudo obtener información de la receta.'
        }

    return JsonResponse(respuesta)