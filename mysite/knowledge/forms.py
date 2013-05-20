from django import forms
from django.forms.widgets import Widget
from knowledge.models import Suceso,Clasificacion,TipoProblema
from django.utils.regex_helper import Choice
from django.utils.timezone import now
from django.template.defaultfilters import default
from django.utils.datetime_safe import datetime

class nuevoSuceso(forms.Form):
	nombre=forms.CharField(widget=forms.TextInput())
	descripcion=forms.CharField(widget=forms.Textarea())
	fecha=forms.DateField()
	impacto=forms.IntegerField(widget=forms.TextInput())
	urgencia=forms.IntegerField(widget=forms.TextInput())
	contador=forms.IntegerField(widget=forms.TextInput())
	nivel=forms.CharField(widget=forms.TextInput())
	clasificacion=forms.ComboField(Clasificacion.objects.all())
	#tipo_problema=forms.MultipleChoiceField(TipoProblema.objects.all())
	def clean(self):
		return self.cleaned_data