from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros', views.LibroListView.as_view(), name='libros'),
    path(r'libro/(?P<pk>\d+)$', views.LibroDetailView.as_view(), name='libro-detail'),
    path(r'^mislibros/$', views.PrestamoListView.as_view(), name='mis-prestamos'),
    path(r'^libro/create/$', views.LibroCreate.as_view(), name='libro_create'),
    path(r'^libro/(?P<pk>\d+)/update/$', views.LibroUpdate.as_view(), name='libro_update'),
    path(r'^libro/(?P<pk>\d+)/delete/$', views.LibroDelete.as_view(), name='libro_delete'),
    path(r'^libro/(?P<pk>\d+)/ejemplar/create/$', views.EjemplarCreate.as_view(), name='ejemplar_create'),
    path(r'^libro/(?P<pk>\d+)/ejemplar/update/$', views.EjemplarUpdate.as_view(), name='ejemplar_update'),
    path(r'^libro/(?P<pk>\d+)/ejemplar/delete/$', views.EjemplarDelete.as_view(), name='ejemplar_delete'),
    path(r'^libro/ejemplar/(?P<pk>\d+)/prestamo/<username>/create/$', views.crear_prestamo, name='crear_prestamo'),
    path(r'^prestamo/(?P<pk>\d+)/<username>/delete/$', views.devolver_prestamo, name='devolver_prestamo'),
    # path('test_template', views.test_template, name='test_template'),
]