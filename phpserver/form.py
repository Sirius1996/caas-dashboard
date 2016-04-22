from django import forms
from django.shortcuts import render
from api import phpserver as api
from models import Image,Container,Project

class SelfHandlingMixin(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        if not hasattr(self, "handle"):
            raise NotImplementedError("%s does not define a handle method."
                                      % self.__class__.__name__)
        super(SelfHandlingMixin, self).__init__(*args, **kwargs)


class CreateProjectForm(SelfHandlingMixin,forms.Form):

    project_name = forms.CharField(max_length=80,
                                   label="Project Name")
    try:
        choices = [(container.container_id,container.name) for container in Container.objects.all()]
    except Exception:
        choices = []

    container = forms.ChoiceField(choices=choices,label="Base Environment")

    # version = forms.CharField(max_length=10,label="Version")

    # code_url = forms.CharField(max_length=100,label="Code URL")

    def __init__(self,request,*args,**kwargs):
        super(CreateProjectForm,self).__init__(request,*args,**kwargs)

    def handle(self,request,data):
        try:
            project_container = Container.objects.get(container_id=data['container'])
            # project_code = Code.objects.filter(url=code_url)
            # project_username = User.object.filter(username="rogeryu")
            p_id = api.project_create(request,project_container)
            return None
        except Exception, e:
            raise e
            return None

class CreateContainerForm(SelfHandlingMixin,forms.Form):

    container_name = forms.CharField(max_length=80,
                                   label="Container Name")
    try:
        choices = [(image.repo,image.repo) for image in Image.objects.all()]
    except Exception:
        choices = []

    base_image = forms.ChoiceField(choices=choices,label="Base Image")

    description = forms.CharField(label="Description",
                                  required=False,
                                  widget=forms.Textarea(attrs={'rows': 4}))

    # version = forms.CharField(max_length=10,label="Version")

    def __init__(self, request, *args, **kwargs):
        super(CreateContainerForm,self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            container_id = api.container_create(request,repo=data['base_image'],name=data['container_name'])
            Container.objects.create(container_id=container_id.get("Id")[0:12],name=data['container_name'],
                version=1.0,image=Image.objects.get(repo=data['base_image']),description=data['description'])
            return None
        except Exception, e:
            raise e
            return None

class CreateImageByStepForm(SelfHandlingMixin,forms.Form):

    repo_name = forms.CharField(label="Repository Name",max_length=20)

    try:
        choices = [(image.repo,image.repo) for image in Image.objects.all()]
    except Exception:
        choices = []
    base_image = forms.ChoiceField(choices=choices,label="Base Image")

    code = forms.FileField(label="Code Package")
    # code_path = forms.FilePathField()
    code_path = forms.CharField(label="Code Path")

    ports = forms.IntegerField(label="Ports")

    vnc = forms.BooleanField(label="Support VNC")

    def __init__(self, request, *args, **kwargs):
        super(CreateImageByStepForm,self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            api.create_image_by_step(request,
                data['repo_name'],
                data['base_image'],
                data['code'],
                data['code_path'],
                data['ports'],
                data['no_vnc'])
            return None
        except Exception, e:
            raise e
            return None


class CreateImageByDockerfileForm(SelfHandlingMixin,forms.Form):

    # try:
    #     choices = [(image.repo,image.repo) for image in Image.objects.all()]
    # except Exception:
    #     choices = []
    # base_image = forms.ChoiceField(choices=choices,label="Base Image")

    github_url = forms.CharField(label="Url",widget=forms.URLInput)

    repo_name = forms.CharField(label="Name",max_length=20)

    vnc = forms.BooleanField(label="Support VNC")

    def __init__(self, request, *args, **kwargs):
        super(CreateImageByDockerfileForm,self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            api.create_image_from_dockerfile(request,
                data['github_url'],
                data['repo_name'],
                data['vnc'])
            return None
        except Exception, e:
            raise e
            return None

class SearchImageForm(SelfHandlingMixin,forms.Form):

    def __init__(self, request, *args, **kwargs):
        super(SearchImageForm,self).__init__(request, *args, **kwargs)
    def handle(self, request, data):
        try:
            if 'image_pull' in request.POST:
                api.image_pull(request,repo=request.POST.get('image_pull'))#image.status
                return None

            if 'image_search' in request.POST:
                result =  api.image_search(request,request.POST.get('image_search'))

                return render(request,'phpserver/table_image.html',
                     {'image_list':result,'term':request.POST.get('image_search')})
            return None
        except Exception, e:
            raise e
            return None