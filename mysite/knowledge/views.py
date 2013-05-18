# Create your views here.
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from knowledge.models import Suceso, SucesoForm

def nuevo_suceso(request):
	sucesoForm= modelformset_factory(Suceso)
	if request.method=="POST":
		formset = sucesoForm(request.POST, request.FILES)
		if formset.is_valid():
			formset.save()
	else:
		formset=sucesoForm()
		
		
	return render_to_response("nuevo_suceso.html",{"formset":formset,})

def nuevo_suceso2(request):
	if request.method=="POST":
		form=SucesoForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/kb/")
	else:
		form =SucesoForm()
		
	return render(request,"nuevo_suceso.html",{"formset":form,})