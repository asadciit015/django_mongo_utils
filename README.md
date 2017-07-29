utils using django and mongo engine to make django db operations validated and helping

  	DB = DjangoMongoUtils() #load models and connect to db
	
	# collection_name = <DB model/collection name>
	# logging.info("collection_name: '{}'\n".format(collection_name))


	# logging.info("All Fields with Names for: '{}' are:".format(collection_name))
	# all_fields_names = DB.getALLFieldsNames(
	# 	collection_name = collection_name
	# )
	# logging.info("{}\n".format(all_fields_names))


	# logging.info("All Fields with Names and Types for: '{}' are:".format(collection_name))
	# all_fields_names_types = DB.getALLFieldsNamesTypes(
	# 	collection_name = collection_name
	# )
	# logging.info("{}\n".format(all_fields_names_types))


	# logging.info("All Reference Fields for: '{}' are:".format(collection_name))
	# all_reference_fields = DB.getAllReferenceFields(
	# 	collection_name = collection_name
	# )
	# logging.info("{}\n".format(all_reference_fields))


	
	# logging.info("Field Type of: '{}' is:".format(all_reference_fields[0]))
	# field_type = DB.getFieldType(
	# 	collection_name = collection_name, field_name = all_reference_fields[0]
	# )
	# logging.info("{}\n".format(field_type))



	# logging.info("All Field Attributes for: '{}' are:".format(all_reference_fields[0]))
	# all_reference_fields_attributes = DB.getFieldAttributes(
	# 	collection_name = collection_name, field_name = all_reference_fields[0]
	# )
	# logging.info("{}\n".format(all_reference_fields_attributes))




	# logging.info("Referenced Class Name for: '{}' are:".format(all_reference_fields[0]))
	# referenced_class_name = DB.getReferencedClassName(
	# 	collection_name = collection_name, reference_field_name = all_reference_fields[0]
	# )
	# logging.info("{}\n".format(referenced_class_name))

	print DB.typeCastFieldValue(
		collection_name= <collectionName>, field_name = <field_name> , field_value = <field_value>)
