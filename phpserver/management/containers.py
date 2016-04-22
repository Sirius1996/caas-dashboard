from ..models import Container

class ContainerManager():
		def __init__(self,client):
				self.client = client

		def create(self,repo,port_bindings=None,name=None):
		# if not port_bindings and (p_type == "php"):
		#       	port_bindings={"80":"8888"}

				ports = []

				if port_bindings:
						for k in port_bindings:
								ports.append(k)

				# username = "rogeryu"
				# img_repo = username + '/' +repo

				host_config = self.client.create_host_config(port_bindings=port_bindings)
				#print host_config
				container = self.client.create_container(image=repo,ports=ports,host_config=host_config,name=name)

				return container

		def delete(self,c_id):
				self.client.remove_container(container=c_id,force=force)
				Container.objects.filter(container_id=c_id).delete()

		def commit(self,container,repository=None,tag=None):
				self.client.remove_container(container=c_id,repository=repository,tag=tag)