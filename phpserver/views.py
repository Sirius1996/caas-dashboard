from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
import json

from lib import forms
from lib import workflows
from lib import base

from phpserver import form as form_class

#from phpserver.api import phpserver as client
from api import phpserver as api
from management import client as client
from .models import Project,Image,Container

class ProjectView(base.CaasTemplateView):
    page_title = _("Project Management")
    template_name = "phpserver/project/project.html"

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
						c_id = request.POST.get('delete')
						api.project_delete(request,c_id)

        if 'stop' in request.POST:
						c_id = request.POST.get('stop')
						api.project_stop(request,c_id)

        if 'start' in request.POST:
						c_id = request.POST.get('start')
						api.project_start(request,c_id)

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['form_url'] = "phpserver/project/project.html"
        context['project_list'] = Project.objects.all()
        context['container_list'] = Container.objects.all()
        return context

class CreateProjectView(forms.ModalFormView):
		template_name = "phpserver/project/create_project.html"
		form_class = form_class.CreateProjectForm
		success_url = reverse_lazy("phpserver:project")
		page_title = _("Create Project")

class ProjectDetailView(base.CaasTemplateView):
		page_title = _("Project Details")
		template_name = "phpserver/project/details.html"

		def get_context_data(self, **kwargs):
				context = super(ProjectDetailView, self).get_context_data(**kwargs)
				project = Project.objects.get(p_id=kwargs['p_id'])
				context['project'] = project
				return context

class ImageView(base.CaasTemplateView):
		page_title = _("Image Management")
		template_name = "phpserver/image/image.html"

		def get_context_data(self, **kwargs):
				context = super(ImageView, self).get_context_data(**kwargs)
				context['form_url'] = "phpserver/image/image.html"
				context['image_list'] = Image.objects.all()
				return context

		def post(self, request, *args, **kwargs):
				if 'delete' in request.POST:
						try:
								api.image_delete(request,request.POST.get('delete'))
						except Exception, e:
								print "Error during deleting images"
								raise e
						return render(request,'phpserver/image/image.html',{'image_list':Image.objects.all()})

class CreateImageByStepView(forms.ModalFormView):
		template_name = "phpserver/image/create_image_by_step.html"
		form_class = form_class.CreateImageByStepForm
		success_url = reverse_lazy("phpserver:image")
		page_title = _("Create Image By Step")

class CreateImageByDockerfileView(forms.ModalFormView):
		template_name = "phpserver/image/create_image_by_dockerfile.html"
		form_class = form_class.CreateImageByDockerfileForm
		success_url = reverse_lazy("phpserver:image")
		page_title = _("Create Image By Dockerfile")

class SearchImageView(forms.ModalFormView):
		template_name = "phpserver/image/search_image.html"
		form_class = form_class.SearchImageForm
		success_url = reverse_lazy("phpserver:image")
		page_title = _("Search Image")

class ImageDetailView(base.CaasTemplateView):
		page_title = _("Image Details")
		template_name = "phpserver/image/details.html"

		def get_context_data(self, **kwargs):
				context = super(ImageDetailView, self).get_context_data(**kwargs)
				image = Image.objects.get(img_id=kwargs['img_id'])
				context['image'] = image
				return context

class ContainerView(base.CaasTemplateView):
		page_title = _("Container Management")
		template_name = "phpserver/container/container.html"

		def get_context_data(self, **kwargs):
				context = super(ContainerView, self).get_context_data(**kwargs)
				context['form_url'] = "phpserver/container/container.html"
				context['container_list'] = Container.objects.all()
				return context

		def post(self, request, *args, **kwargs):
				if 'delete' in request.POST:
						try:
								api.container_delete(request,request.POST.get('delete'))
						except Exception, e:
								print "Error during deleting container"
								raise e
						return render(request,'phpserver/container/container.html',{'container_list':Container.objects.all()})

				if 'trans_image' in request.POST:
						try:
						    api.container_commit(request,request.POST.get('trans_image'))
						except Exception, e:
							raise e

class CreateContainerView(forms.ModalFormView):
		template_name = "phpserver/container/create_container.html"
		form_class = form_class.CreateContainerForm
		success_url = reverse_lazy("phpserver:container")
		page_title = _("Create Container")

class ContainerDetailView(base.CaasTemplateView):
		page_title = _("Container Details")
		template_name = "phpserver/container/details.html"

		def get_context_data(self, **kwargs):
				context = super(ContainerDetailView, self).get_context_data(**kwargs)
				container = Container.objects.get(container_id=kwargs['container_id'])
				context['container'] = container
				return context

class ConsoleView(base.CaasTemplateView):
		page_title = _("Console")
		template_name = "phpserver/console.html"

		def get_context_data(self, **kwargs):
				context = super(ConsoleView,self).get_context_data(**kwargs)
				context['console_url'] = "/phpserver/project/console/novnc/"+kwargs['p_id']
				context['project_id'] = kwargs['p_id']
				return context

class NoVNCView(TemplateView):
		template_name = "phpserver/noVNC/vnc_auto.html"

		def get_context_data(self,**kwargs):
				context = super(NoVNCView,self).get_context_data(**kwargs)

def container(request):
	if 'image' in request.POST:
		image = request.POST['image']
		img_repo,img_tag = image.split[':']

	if 'env_ports' in request.POST:
		env_ports = json.loads(request.POST.get('env_ports'))

		env = api.create(img_repo,env_ports)
		Container.objects.create(env_id=env.id,name=env.name)

	return render(request,'phpserver/container.html',{'env_list':Container.objects.all()})

class TestView(workflows.WorkflowView):
		workflow_class = " "
		success_url = ""
		template_name = ""
		page_title = ""