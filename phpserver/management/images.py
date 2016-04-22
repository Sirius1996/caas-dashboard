from ..models import Image
import json
from git import Repo
import os
import shutil
from utils import add_new_line as _

GIT_DIR = "/home/roger/workspace/git/caas_base"
join = os.path.join

class ImageManager(object):
    """docstring for ImageManager"""
    def __init__(self,client):
        self.client = client

    def build(self,url,repo_name,tag=None,vnc):
        # for i,ports in enumerate(args.port):
        #     args.port[i] = tuple(ports.split('/'))
        # if not tag:
        #     tag = user+"/"+p_type+":"+str(version) # make_tag()

        # dockerfile = _create_dockerfile(url,p_type,user)
        if tag is None:
            tag = "latest"
        dockerfile_dir = join(GIT_DIR,repo_name)
        Repo.clone_from(url,dockerfile_dir,branch="master")

        temp_id = "djoiadsdaasasdass"
        Image.objects.create(img_id=temp_id,repo=repo_name,tag=tag,github_url=url,
          dockerfile=open(join(dockerfile_dir,"Dockerfile")).read())

        for line in self.client.build(path=dockerfile_dir, rm=True, tag=repo_name):
            print line
        Image.objects.filter(repo=repo_name).update(
          img_id=self.images(repo_name)[0].get("Id")[0:12])

        #Something others to do
        if vnc:
            dockerfile = self.make_dockerfile(base_image=repo_name,vnc=vnc)
            self.git_init(repo_name,dockerfile)
            Image.objects.create(img_id=temp_id,repo=repo_name,tag=tag,github_url=url,
                dockerfile=open(join(dockerfile_dir,"Dockerfile")).read())

            for line in self.client.build(path=dockerfile_dir, rm=True, tag=repo_name):
                print line
            Image.objects.filter(repo=repo_name).update(
              img_id=self.images(repo_name)[0].get("Id")[0:12])

    def create_image(self,repo_name,base_image,code=None,code_path=None,port=None,vnc):

        dockerfile_dir = join(GIT_DIR,repo_name)
        (codepath,codename)=os.path.split(code.name)
        shutil.move(code,join(dockerfile_dir,codename))

        dockerfile = self.make_dockerfile(base_image=base_image,code_name=code_name,
            code_path=code_path,port=port,vnc=vnc)

        self.git_init(repo_name,dockerfile)

        if tag is None:
            tag = "latest"

        temp_id = "djoiadxxsaasdasdass"

        Image.objects.create(img_id=temp_id,repo=repo_name,tag=tag,
          dockerfile=dockerfile)

        for line in self.client.build(path=dockerfile_dir, rm=True, tag=repo_name):
            print line
        Image.objects.filter(repo=repo_name).update(
          img_id=self.images(repo_name)[0].get("Id")[0:12])

    def delete(self,img_id):
        repo_name = Image.objects.get(img_id=img_id).repo
        Image.objects.filter(img_id=img_id).delete()
        dockerfile_dir = join(GIT_DIR,repo_name)
        if os.path.isdir(dockerfile_dir):
            shutil.rmtree(dockerfile_dir)
        try:
            self.client.remove_image(img_id,force=True)
        except Exception, e:
            raise e
            print "Image do not exist"

  	#Search for a image in the DockerHub (Need Api)
    def search(self,term):
        return self.client.search(term=term)

    def push(self,img_repo,tag):
        pass

    #Get an image from DockerHub (Need Api)
    def pull(self,repository,vnc):
        dockerfile = self.make_dockerfile(base_image=repository,vnc=vnc)

        temp_id = "dsadsasasada"
        Image.objects.create(img_id=temp_id,repo=repository,tag="latest",
          status="Pending",github_url="",dockerfile=dockerfile)

        self.git_init(repository,dockerfile)

        try:
            for line in self.client.pull(repository=repository,tag="latest",stream=True):
                image = json.loads(line)
                print image
                # Image.objects.filter(repo=repository).update(status=image.get("status"))
            Image.objects.filter(repo=repository).update(
                img_id=self.images(repository)[0].get("Id")[0:12])
        except Exception, e:
            Image.objects.filter(repo=repository).delete()
            print "Something wrong pulling images"
            raise e


    def tag():
        pass

  	def regist(self,img_path,tag):
    		pass

    #List the images
    def list(self,username,img_name = None):
    	# img_list = []
    	# images = self.client.images(name=img_name)
    	# for image in images:
    	# 	if image.get('RepoTags')[0].split(':')[0] == username:
    	# 		img_list.append(image)
    			# return img_list

    	    return Images.objects.filter(username=username)

      # def _create_dockerfile(self,url,ptype,user):
      # 	dockerfile = tempfile.NamedTemporaryFile()
      # 	#os.system('cat dockerfile_template > ' + dockerfile.name)
      # 	os.system('/usr/local/lib/python2.7/dist-packages/docker/'+ptype+'_init.sh '+dockerfile.name+" "+url+" "+ptype+" "+user)#TODO

      # 	return dockerfile

    def images(self,repo_name):
        return self.client.images(name=repo_name)

    def make_dockerfile(self,base_image,code_name=None,code_path=None,port=None,vnc):
        # dockerfile = "FROM " + base_image + "\n"
        # if vnc:
        #     dockerfile += "RUN apt-get update && apt-get install x11vnc xvfb" + "\n"
        #     dockerfile += "RUN x11vnc -storepasswd 1234 ~/.vnc/passwd" + "\n"
        # if code_name:
        #     dockerfile += "ADD" + code_name + " " + codepath + "\n"
        #     dockerfile += "WORKDIR" + code_name + "\n"
        # if port:
        #     dockerfile += "EXPOSE" + port + "\n"
        # if vnc:
        #     dockerfile += "EXPOSE 5900" + "\n"
        #     dockerfile += 'CMD    ["x11vnc", "-forever", "-usepw", "-create"]' +"\n"
        dockerfile = _("FROM " + base_image)
        if vnc:
            dockerfile += _("RUN apt-get update && apt-get install x11vnc xvfb")
            dockerfile += _("RUN x11vnc -storepasswd 1234 ~/.vnc/passwd")
        if code_name:
            dockerfile += _("ADD" + code_name + " " + codepath)
            dockerfile += _("WORKDIR" + code_name)
        if port:
            dockerfile += _("EXPOSE" + port)
        if vnc:
            dockerfile += _("EXPOSE 5900")
            dockerfile += _('CMD    ["x11vnc", "-forever", "-usepw", "-create"]')
        print dockerfile

        return dockerfile


    def git_init(self,repository,dockerfile):
        repo_dir = join(GIT_DIR, repository)
        file_name = join(repo_dir, 'Dockerfile')
        repo = Repo.init(repo_dir)

        f = open(file_name,'w+')
        f.writelines(dockerfile)
        f.close()

        repo.index.add([file_name])
        repo.index.commit("initial commit")



