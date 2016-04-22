import projects,images,containers
from docker import client as api_client

class Client(object):
	def __init__(self):
		client = api_client.Client(base_url='unix://var/run/docker.sock')

		self.projects = projects.ProjectManager(client)
		self.images = images.ImageManager(client)
		self.containers = containers.ContainerManager(client)
