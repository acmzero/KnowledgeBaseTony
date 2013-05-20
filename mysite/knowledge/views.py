# Create your views here.
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from knowledge.models import Suceso, SucesoForm,AdjuntoForm
from knowledge.forms import nuevoSuceso
from django.template.context import RequestContext
from django.utils.datetime_safe import datetime


def nuevo_suceso(request):
	if request.method=="POST":
		form=SucesoForm(request.POST)
		form2=AdjuntoForm()
		info="inicializando"
		
		if form.is_valid():
			salva=Suceso(request.POST)
			salva.save()
			nombre=form.cleaned_data['nombre']
			descripcion=form.cleaned_data['descripcion']
			fecha=datetime.now()
			impacto=form.cleaned_data['impacto']
			urgencia=form.cleaned_data['urgencia']
			contador=form.cleaned_data['contador']
			
			clasificacion=form.cleaned_data['clasificacion']
			tipo_problema=form.cleaned_data['tipo_problema']
			
			s=Suceso()#
			s.nombre=nombre
			s.descripcion=descripcion
			s.fecha=fecha
			s.impacto=impacto
			s.urgencia=urgencia
			s.contador=contador
			s.nivel=nivel(impacto, urgencia)
			s.clasificacion=clasificacion
			s.tipo_problema=tipo_problema
			
			s.save()
			info="se guardo e registro"
		else:
			info="datos erroneos"
		form = SucesoForm()	
		form2=AdjuntoForm()
		contexto={'form':form, 'informacion':info,'form2':form2}
		return render_to_response("nuevo_suceso.html",contexto,context_instance=RequestContext(request))
	else:
		form=SucesoForm()
		form2=AdjuntoForm()
		contexto={'form': form, 'form2':form2}
		return render_to_response("nuevo_suceso.html",contexto,context_instance=RequestContext(request))
def nivel(x,y):
	suma=x+y
	dic= {2:'Critica',3:'Alta',4:'Media',5:'Baja',6:'Planificada'}
	return dic[suma]
