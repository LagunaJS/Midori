from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from datetime import datetime
from models import *
from django.shortcuts import get_object_or_404
#from forms import *
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from account.models import Account
#from actstream import action
from actstream.actions import follow, unfollow, like, unlike

class PublicacionListView(ListView):
	model = Publicacion
	context_object_name = 'publicaciones'
	def get_template_names(self):
		return 'index.html'

class PublicacionDetailView(DetailView):
	model = Publicacion
	def get_template_names(self):
		return 'publicacion.html'	

def home(request):
	categorias = Categoria.objects.all()
	publicaciones = Publicacion.objects.order_by("-votos").all()[:15] #limita a 15 resultados
	template = "index.html"
	return render(request,template,locals())	

def categoria(request,id_categoria):
	categorias = Categoria.objects.all()
	categoria = get_object_or_404(Categoria, pk=id_categoria)
	publicaciones = Publicacion.objects.filter(categoria = categoria)
	template = "index.html"
	return render(request,template,locals())

def post(request, id_publicacion):
	publicacion = Publicacion.objects.get(pk = id_publicacion)
	template = "post.html"
	return render(request,template,locals())

@login_required
def seguir(request,id_usuario):
	usuario = Account.objects.get(pk=id_usuario)
	follow(request.user, usuario)
	return HttpResponseRedirect("/usuario/%s" %id_usuario)

@login_required
def noseguir(request,id_usuario):
	usuario = Account.objects.get(pk=id_usuario)
	unfollow(request.user, usuario)
	return HttpResponseRedirect("/usuario/%s" %id_usuario)

@login_required
def favorito(request,id_publicacion):
	publicacion = Publicacion.objects.get(pk=id_publicacion)
	publicacion.favoritos = publicacion.favoritos + 1
	publicacion.save()
	follow(request.user, publicacion,actor_only=False)
	return HttpResponseRedirect("/")

@login_required
def nofavorito(request,id_publicacion):
	publicacion = Publicacion.objects.get(pk=id_publicacion)
	publicacion.favoritos = publicacion.favoritos - 1
	publicacion.save()
	unfollow(request.user, publicacion)
	return HttpResponseRedirect("/")

@login_required
def mas(request,id_publicacion):
	publicacion = Publicacion.objects.get(pk=id_publicacion)
	publicacion.votos = publicacion.votos + 1
	publicacion.save()
	like(request.user, publicacion)
	return HttpResponseRedirect("/")

@login_required
def nomas(request,id_publicacion):
	publicacion = Publicacion.objects.get(pk=id_publicacion)
	publicacion.votos = publicacion.votos - 1
	publicacion.save()
	unlike(request.user, publicacion)
	return HttpResponseRedirect("/")

def usuario(request,id_usuario):
	categorias = Categoria.objects.all()
	usuario = Account.objects.get(pk=id_usuario)
	publicaciones = Publicacion.objects.filter(usuario = id_usuario)
	template = "user.html"
	return render(request,template,locals())