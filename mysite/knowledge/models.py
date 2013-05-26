# -*- coding: iso-8859-15 -*-
from knowledge import settings

import django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from knowledge.managers import QuestionManager, ResponseManager
from knowledge.signals import knowledge_post_save

URGENCIAS = (
           ("1", "Alta"),
           ("2", "Media"),
           ("3", "Baja"),
           )
STATUSES = (
    ('public', _('Publico')),

)

NIVELES = (
         ("1", "Critico"),
         ("2", "Alto"),
         ("3", "Media"),
         ("4", "Baja"),
         ("5", "Planificada"),
         )
TIEMPO_RESOLUCION = (
                   ("1", "1 Hora"),
                   ("2", "8 Horas"),
                   ("3", "24 Horas"),
                   ("4", "48 Horas"),
                   ("5", "Planificada")
                   )
STATUSES_EXTENDED = STATUSES + (
    ('inherit', _('Heredar')),
)

class TipoProblema(models.Model):
  tipo = models.CharField(max_length=60)
  
  def __unicode__(self):
    return self.tipo
  class Meta:
    verbose_name="Tipo de Problema"
  
class Category(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    lastchanged = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')


class KnowledgeBase(models.Model):
    """
    The base class for Knowledge models.
    """
    is_question, is_response = False, False

    added = models.DateTimeField(auto_now_add=True)
    lastchanged = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('auth.User' if django.VERSION < (1, 5, 0) else django_settings.AUTH_USER_MODEL, blank=True,
                             null=True, db_index=True)
    alert = models.BooleanField(default=settings.ALERTS,
        verbose_name=_('Alerta'),
        help_text=_('Seleccione esta opcion si desea recibir una alerta cuando se agregue'
                        ' una nueva respuesta.'))

    # for anonymous posting, if permitted
    name = models.CharField(max_length=64, blank=True, null=True,
        verbose_name=_('Nombre'),
        help_text=_('Pon tu nombre completo.'))
    email = models.EmailField(blank=True, null=True,
        verbose_name=_('Email'),
        help_text=_('Pon una direccion de correo valida.'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.user and self.name and self.email \
                and not self.id:
            # first time because no id
            self.public(save=False)

        if settings.AUTO_PUBLICIZE and not self.id:
            self.public(save=False)

        super(KnowledgeBase, self).save(*args, **kwargs)

    #########################
    #### GENERIC GETTERS ####
    #########################

    def get_name(self):
        """
        Get local name, then self.user's first/last, and finally
        their username if all else fails.
        """
        name = (self.name or (self.user and (
            u'{0} {1}'.format(self.user.first_name, self.user.last_name).strip()\
            or self.user.username
        )))
        return name.strip() or _("Anonimo")

    get_email = lambda s: s.email or (s.user and s.user.email)
    get_pair = lambda s: (s.get_name(), s.get_email())
    get_user_or_pair = lambda s: s.user or s.get_pair()

    ########################
    #### STATUS METHODS ####
    ########################

    def can_view(self, user):
        """
        Returns a boolean dictating if a User like instance can
        view the current Model instance.
        """

        if self.status == 'inherit' and self.is_response:
            return self.question.can_view(user)

        if self.status == 'internal' and user.is_staff:
            return True

        if self.status == 'private':
            if self.user == user or user.is_staff:
                return True
            if self.is_response and self.question.user == user:
                return True

        if self.status == 'public':
            return True

        return False

    def switch(self, status, save=True):
        self.status = status
        if save:
            self.save()
    switch.alters_data = True

    def public(self, save=True):
        self.switch('public', save)
    public.alters_data = True

    def private(self, save=True):
        self.switch('private', save)
    private.alters_data = True

    def inherit(self, save=True):
        self.switch('inherit', save)
    inherit.alters_data = True

    def internal(self, save=True):
        self.switch('internal', save)
    internal.alters_data = True


class Question(KnowledgeBase):
    is_question = True
    _requesting_user = None

    title = models.CharField(max_length=255,
        verbose_name=_('Suceso'),
        help_text=_('Pon una pregunta o sugerencia.'))
    body = models.TextField(blank=True, null=True,
        verbose_name=_('Descripcion'),
        help_text=_('Detalles del suceso.'))

    status = models.CharField(
        verbose_name=_('Visibilidad'),
        max_length=32, choices=STATUSES,
        default='public', db_index=True)
    
    impacto = models.CharField(verbose_name=("Impacto"), max_length=32, choices=URGENCIAS)
    
    urgencia = models.CharField(verbose_name="Urgencia", choices=URGENCIAS, max_length=32)
    
    contador = models.IntegerField(verbose_name="Contador", default=0)
    
    nivel = models.CharField(verbose_name="Nivel", choices=NIVELES, max_length=32)
    
    tipo_problema= models.ForeignKey("knowledge.TipoProblema")

    locked = models.BooleanField(default=False)

    categories = models.ForeignKey('knowledge.Category', blank=False,verbose_name="Clasificacion")
    
    #adjuntos=models.ManyToManyField("knowledge.Adjunto",verbose_name="Adjuntos")

    objects = QuestionManager()

    class Meta:
        ordering = ['-added']
        verbose_name = _('Suceso')
        verbose_name_plural = _('Sucesos')

    def __unicode__(self):
        return self.title

    def get_nivel(self):
      for a in NIVELES:
        if a[0] == self.nivel:
          return a[1]
      return ""
    def get_tiempo_resolucion(self):
      for a in TIEMPO_RESOLUCION:
        if a[0] == self.nivel:
          return a[1]
      return ""
    

    @models.permalink
    def get_absolute_url(self):
        from django.template.defaultfilters import slugify

        if settings.SLUG_URLS:
            return ('knowledge_thread', [self.id, slugify(self.title)])
        else:
            return ('knowledge_thread_no_slug', [self.id])

    def inherit(self):
        pass

    def internal(self):
        pass

    def lock(self, save=True):
        self.locked = not self.locked
        if save:
            self.save()
    lock.alters_data = True

    ###################
    #### RESPONSES ####
    ###################

    def get_responses(self, user=None):
        user = user or self._requesting_user
        if user:
            return [r for r in self.responses.all().select_related('user') if r.can_view(user)]
        else:
            return self.responses.all().select_related('user')

    def answered(self):
        """
        Returns a boolean indictating whether there any questions.
        """
        return bool(self.get_responses())

    def accepted(self):
        """
        Returns a boolean indictating whether there is a accepted answer
        or not.
        """
        return any([r.accepted for r in self.get_responses()])

    def clear_accepted(self):
        self.get_responses().update(accepted=False)
    clear_accepted.alters_data = True

    def accept(self, response=None):
        """
        Given a response, make that the one and only accepted answer.
        Similar to StackOverflow.
        """
        self.clear_accepted()

        if response and response.question == self:
            response.accepted = True
            response.save()
            return True
        else:
            return False
    accept.alters_data = True

    def states(self):
        """
        Handy for checking for mod bar button state.
        """
        return [self.status, 'lock' if self.locked else None]

    @property
    def url(self):
        return self.get_absolute_url()


class Response(KnowledgeBase):
    is_response = True

    question = models.ForeignKey('knowledge.Question',
        related_name='responses')

    body = models.TextField(blank=True, null=True,
        verbose_name=_('Respuesta'),
        help_text=_('Introduzca su respuesta. Markdown Activado.'))
    status = models.CharField(
        verbose_name=_('Estado'),
        max_length=32, choices=STATUSES_EXTENDED,
        default='inherit', db_index=True)
    accepted = models.BooleanField(default=False)

    objects = ResponseManager()

    class Meta:
        ordering = ['added']
        verbose_name = _('Respuesta')
        verbose_name_plural = _('Respuestas')

    def __unicode__(self):
        return self.body[0:100] + u'...'

    def states(self):
        """
        Handy for checking for mod bar button state.
        """
        return [self.status, 'accept' if self.accepted else None]

    def accept(self):
        self.question.accept(self)
    accept.alters_data = True


class Adjunto(models.Model):
  nombre = models.CharField(max_length=50)
  localizacion=models.FileField(upload_to='./archivos', blank = False)
  #Comentar las opciones para los adjuntos (Documentadores)
  tipo_adjunto= models.CharField(max_length=50)
  

# cannot attach on abstract = True... derp
models.signals.post_save.connect(knowledge_post_save, sender=Question)
models.signals.post_save.connect(knowledge_post_save, sender=Response)
