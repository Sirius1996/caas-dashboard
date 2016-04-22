from ..management import client as api_client

def client(request):
		return api_client.Client()

def project_create(request,container):
		return client(request).projects.create(container)

def project_delete(request,p_id):
		client(request).projects.delete(p_id)

def project_stop(request,p_id):
		client(request).projects.stop(p_id)

def project_start(request,p_id):
		client(request).projects.start(p_id)

def image_list(request,username):
		return client(request).images.list(username)

def image_delete(request,img_id):
		client(request).images.delete(img_id)

def image_pull(request,repo,vnc):
		return client(request).images.pull(repo,vnc)

def image_get(request,repo):
		return client(request).images.images(repo_name=repo)

def image_search(request,term):
		return client(request).images.search(term)

def create_image_by_step(request,repo_name,base_image,code,code_path,ports,vnc):
		client(request).images.create_image(repo_name=repo_name,base_image=base_image,
			code=code,code_path=code_path,ports=ports,vnc=vnc)

def create_image_from_dockerfile(request,github_url,repo_name,vnc):
		client(request).images.build(url=github_url,repo_name=repo_name,vnc=vnc)

def container_create(request,repo,ports=None,name=None):
		return client(request).containers.create(repo,ports,name)

def container_delete(request,c_id):
		return client(request).containers.delete(c_id)

def container_commit(request,c_id,repo=None,tag=None):
		return client(request).containers.commit(container=c_id,repository=repo,tag=tag)

