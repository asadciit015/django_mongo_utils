"""
Author: Assad Nadeem
Created Date: 27-07-2017
"""
import os, sys
import logging
import importlib
import ast
# from django_utils import *
from django.utils import *
import mongoengine
from mongoengine import *

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
logging.basicConfig(
	format='[%(asctime)s | %(module)s %(levelname)s]:%(message)s',	
	level=logging.INFO,
	datefmt='%m/%d/%Y %I:%M:%S %p'
)

def str2bool(v):
	import argparse
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	if v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')

# Django_Models_PATH > refers to app/models/path by default
Django_Models_PATH = "app/models/path" #change it to refer to any other app models
Database_Name = 'database_name'
Username = ''
Password = ''
IP = 'localhost'
Port = 27017


class DjangoMongoUtils(object):
	def __init__(
		self,
		models_path = Django_Models_PATH ,
		db = Database_Name ,
		username = Username ,
	    password = Password ,
		ip = IP ,
		port = Port, 
	):
		self.connection = connect(
			db, username=username, password=password, host=ip, port=port
		)
		logging.info(self.connection)
		self.models_module = importlib.import_module(models_path)

	def getCollectionClass(self, collection_name):
		return getattr(self.models_module, collection_name)

	def getALLFields(self, collection_name):
		return self.getCollectionClass(collection_name = collection_name)._fields

	def getFieldType(self, collection_name, field_name):
		return type(self.getALLFields(
			collection_name = collection_name).get(field_name)).__name__

	def getALLFieldsNames(self, collection_name):
		return self.getALLFields(collection_name = collection_name).keys()

	def getALLFieldsNamesTypes(self, collection_name):
		data = {}
		for k, v in self.getALLFields(collection_name = collection_name).iteritems():
			data[k] = type(v).__name__ 
		return data

	def getFieldAttributes(self, collection_name, field_name):
		return self.getALLFields(
			collection_name = collection_name).get(field_name).__dict__

	def getAllReferenceFields(self, collection_name):
		return [
			k for k, v in self.getALLFields(collection_name = collection_name).iteritems()
			if type(v) == ReferenceField
		]

	def getReferencedClassName(self, collection_name, reference_field_name):
		return self.getCollectionClass(
			collection_name = collection_name)._fields.get(
			reference_field_name).__dict__.get('document_type_obj').__name__
	
	def typeCastFieldValue(self, collection_name, field_name, field_value):
		try:
			collection_class = self.getCollectionClass(collection_name ) 
		except Exception as e:
			msg = "<{0}> Class doesn't exists".format(collection_name)
			raise DoesNotExist(msg)

		field_type = self.getFieldType(collection_name, field_name)
		
		try:
			isinstance(
				getattr(collection_class, field_name),
				getattr(mongoengine.fields, field_type)
			)
			#isinstance(getattr(Company,'coName'),getattr(mongoengine.fields,'StringField'))
		except:
			msg = "'{0}' isn't a Field of Class <{1}>".format(field_name, collection_class.__name__)
			raise DoesNotExist(msg)
		
		try:	
			if field_type == 'ReferenceField':
				return self.getCollectionClass(collection_name = self.getReferencedClassName(
						collection_name = collection_name,reference_field_name = field_name) 
						).objects.get(id = field_value)
			elif field_type == 'IntField':
				return int(field_value)  if not type(field_value) == int else field_value
			elif field_type == 'BooleanField':
				return str2bool(field_value) if not type(field_value) == bool else field_value
			elif field_type == 'StringField':
				return str(field_value) if not type(field_value) == str else field_value
			elif field_type == 'ListField':
				return list(field_value) if not type(field_value) == list else field_value
			elif field_type == 'DictField':
				return ast.literal_eval(field_value) if not type(field_value) == dict else field_value
			elif field_type == 'DateTimeField':
				#not implemented yet
				return field_value
			elif field_type == 'ObjectIdField':
				return field_value	

		except Exception as msg:
				#print (type(msg))
				if isinstance(msg, mongoengine.connection.MongoEngineConnectionError):
					raise MongoEngineConnectionError(msg)
				elif isinstance(msg, mongoengine.errors.DoesNotExist):
					msg = str(msg) + " ReferenceField Given: < {0}={1} > ".format(
						field_name, field_value)
					raise DoesNotExist(msg)
				else:
					raise ValidationError(msg)

	def dictCollectionMap(self, collection_name, dict_object):
		result = {}
		fields = self.getALLFieldsNamesTypes(
			collection_name = collection_name
		)
		for key, value in dict_object.iteritems():
			if not key in fields.keys():
				msg = "'{0}' isn't a Field of Class <{1}>".format(key, collection_name)
				raise DoesNotExist(msg)

			if value:
				result[key] = self.typeCastFieldValue(
					collection_name = collection_name,
					field_name = key,
					field_value = dict_object.get(key)
				) 
		return result