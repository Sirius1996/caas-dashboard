from django.conf.urls import url

from . import views

app_name='phpserver'
urlpatterns=[
	# url(r'^$',views.index,name='index'),
    url(r'^project/create_project/',views.CreateProjectView.as_view(),name="create_project"),
    url(r'^project/console/novnc/(?P<p_id>[^/]+)',views.NoVNCView.as_view(),name="no_vnc"),
    url(r'^project/console/(?P<p_id>[^/]+)',views.ConsoleView.as_view(),name="console"),
    url(r'^project/details/(?P<p_id>[^/]+)',views.ProjectDetailView.as_view(),name="project_detail"),
    url(r'^project/',views.ProjectView.as_view(),name='project'),
    url(r'^container/create_container/',views.CreateContainerView.as_view(),name="create_container"),
    url(r'^container/details/(?P<container_id>[^/]+)',views.ContainerDetailView.as_view(),name="container_detail"),
    url(r'^container/',views.ContainerView.as_view(),name="container"),
    url(r'^image/create_image_by_step/',views.CreateImageByStepView.as_view(),name="create_image_by_step"),
    url(r'^image/create_image_by_dockerfile/',views.CreateImageByDockerfileView.as_view(),name="create_image_by_dockerfile"),
    url(r'^image/search_image/',views.SearchImageView.as_view(),name="search_image"),
    url(r'^image/details/(?P<img_id>[^/]+)',views.ImageDetailView.as_view(),name="image_detail"),
    url(r'^image/',views.ImageView.as_view(),name="image"),
  	url(r'^test/',views.TestView.as_view(),name="test"),
]