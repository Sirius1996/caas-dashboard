from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.utils import timezone
from django.db import models


@python_2_unicode_compatible
class Project(models.Model):
	p_id = models.CharField(max_length=50,primary_key=True) # ??
	name = models.CharField(max_length=50)
	# version = models.FloatField()
	# created_at = models.DateTimeField(auto_now_add=True)
	# # url = models.CharField(max_length=200)
	# state = models.BooleanField(default=True)
	# code = models.ForeignKey(
	# 	'Code',
	# 	on_delete=models.PROTECT)
	container = models.ForeignKey(
		'Container',
		on_delete=models.PROTECT)
	# username = models.ForeignKey(
	# 	'User',
	# 	on_delete=models.PROTECT)

	def __str__(self):
	    return '%s:%s' % (self.name, self.version)

@python_2_unicode_compatible
class Image(models.Model):
	img_id = models.CharField(max_length=50,primary_key=True)
	repo = models.CharField(max_length=50)
	tag = models.CharField(max_length=50)
	status = models.CharField(max_length=200)
	github_url = models.CharField(max_length=200)
	dockerfile = models.TextField()

	def __str__(self):
		return '%s' % self.repo

@python_2_unicode_compatible
class Container(models.Model):
	container_id = models.CharField(max_length=50,primary_key=True)
	name = models.CharField(max_length=50)
	version = models.FloatField()
	description = models.CharField(max_length=200)
	image = models.ForeignKey(
		'Image',
		on_delete=models.PROTECT)

	def __str__(self):
		return '%s:%s' % (self.name,self.version)

@python_2_unicode_compatible
class Code(models.Model):
	code_id = models.CharField(max_length=50,primary_key=True)
	url = models.CharField(max_length=200)
	location = models.CharField(max_length=50)

	def __str__(self):
		return '%s' % self.name

@python_2_unicode_compatible
class User(models.Model):
	"""Model for User"""
	u_id = models.CharField(max_length=50,primary_key=True)
	pwd = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	role = models.ForeignKey(
		'role',
		on_delete=models.PROTECT)

	def __str__(self):
		return '%s' % self.name

@python_2_unicode_compatible
class Role(models.Model):
	r_id = models.CharField(max_length=50,primary_key=True)
	name = models.CharField(max_length=50)
	#privilege

	def __str__(self):
		return '%s' % self.name

