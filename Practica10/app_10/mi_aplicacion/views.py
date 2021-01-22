# Alberto: contraseniaA1997
from django.shortcuts import render, HttpResponse
from django.views import generic
from mi_aplicacion.models import Libro, Ejemplar, Prestamo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime
from django.contrib.auth.models import User
from django.template import loader
# Register
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
# Create your views here.

def index(request):
    # Genera contadores de algunos de los objetos principales
    n_libros = Libro.objects.all().count()
    n_ejemplares = Ejemplar.objects.all().count()
    # Libros disponibles (estado = 'd')
    n_ejemplares_disponibles = Ejemplar.objects.filter(estado__exact='d').count()
    context = {'n_libros': n_libros, 'n_ejemplares': n_ejemplares, 'n_ejemplares_disponibles': n_ejemplares_disponibles}   # Aquí van la las variables para la plantilla
    return render(request,'index.html', context)

def maps(request):
    return render(request,'maps.html')

class LibroListView(generic.ListView):
    model = Libro
    paginate_by = 5


class LibroDetailView(generic.DetailView):
    model = Libro


class PrestamoListView(LoginRequiredMixin,generic.ListView):
    model = Prestamo
    paginate_by = 5
    
    def get_queryset(self):
        return Prestamo.objects.filter(prestatario=self.request.user).order_by('devolucion')


class LibroCreate(CreateView):
    model = Libro
    fields = '__all__'
    # initial={'':'',}


class LibroUpdate(UpdateView):
    model = Libro
    fields = ['titulo','autor','portada','resumen','isbn']


class LibroDelete(DeleteView):
    model = Libro
    success_url = reverse_lazy('libros')


class EjemplarCreate(CreateView):
    model = Ejemplar
    fields = ['id','libro','estado']


class EjemplarUpdate(UpdateView):
    model = Ejemplar  
    fields = '__all__'
    # success_url = reverse_lazy('libros')
    # initial={'':'',}


class EjemplarDelete(DeleteView):
    model = Ejemplar
    success_url = reverse_lazy('libros')


def crear_prestamo(request, pk, username):
    prestatario = User.objects.get(username=username)
    ejemplar = Ejemplar.objects.get(id=pk)
    prestamo = Prestamo.objects.create(ejemplar=ejemplar, prestatario=prestatario, devolucion=datetime.date.today()+datetime.timedelta(days=7))
    prestamo.save()
    ejemplar.estado = 'p'
    ejemplar.save()
    template = loader.get_template('mi_aplicacion/prestamo_list.html')
    context = {'prestamo_list': Prestamo.objects.filter(prestatario=prestatario).order_by('devolucion')}
    return HttpResponse(template.render(context,request))


def devolver_prestamo(request, pk, username):
    prestatario = User.objects.get(username=username)
    ejemplar = Ejemplar.objects.get(id=pk)
    Prestamo.objects.filter(ejemplar=ejemplar).delete()
    ejemplar.estado = 'd'
    ejemplar.save()
    template = loader.get_template('mi_aplicacion/prestamo_list.html')
    context = {'prestamo_list': Prestamo.objects.filter(prestatario=prestatario).order_by('devolucion')}
    return HttpResponse(template.render(context,request))


# class PrestamoCreate(CreateView):
    # model = Prestamo
    # fields = '__all__'
    # initial={'devolucion': datetime.date.today()+datetime.timedelta(days=7)}
    # success_url = reverse_lazy('mis-prestamos')

# class PrestamoDelete(DeleteView):
    # model = Prestamo
    # success_url = reverse_lazy('mis-prestamos')


def signup_auth(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})