try:
	from zohocrmsdk.src.com.zoho.crm.api.exception import SDKException
	from zohocrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
	from zohocrmsdk.src.com.zoho.crm.api.param import Param
except Exception:
	from ..exception import SDKException
	from ..util import APIResponse, CommonAPIHandler, Constants
	from ..param import Param


class RecordLockingOperations(object):
	def __init__(self):
		"""Creates an instance of RecordLockingOperations"""
		pass

	def get_record_lock_information(self, record_id, module_name, param_instance=None):
		"""
		The method to get record lock information

		Parameters:
			record_id (int) : An int representing the record_id
			module_name (string) : A string representing the module_name
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zohocrmsdk.src.com.zoho.crm.api import ParameterMap
		except Exception:
			from ..parameter_map import ParameterMap

		if not isinstance(record_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: record_id EXPECTED TYPE: int', None, None)
		
		if not isinstance(module_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_name EXPECTED TYPE: str', None, None)
		
		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v5/'
		api_path = api_path + str(module_name)
		api_path = api_path + '/'
		api_path = api_path + str(record_id)
		api_path = api_path + '/Locking_Information__s'
		handler_instance.set_api_path(api_path)
		handler_instance.set_http_method(Constants.REQUEST_METHOD_GET)
		handler_instance.set_category_method(Constants.REQUEST_CATEGORY_READ)
		handler_instance.set_param(param_instance)
		try:
			from zohocrmsdk.src.com.zoho.crm.api.record_locking.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def lock_a_record(self, record_id, module_name, request):
		"""
		The method to lock a record

		Parameters:
			record_id (int) : An int representing the record_id
			module_name (string) : A string representing the module_name
			request (BodyWrapper) : An instance of BodyWrapper

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zohocrmsdk.src.com.zoho.crm.api.record_locking.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if not isinstance(record_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: record_id EXPECTED TYPE: int', None, None)
		
		if not isinstance(module_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_name EXPECTED TYPE: str', None, None)
		
		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v5/'
		api_path = api_path + str(module_name)
		api_path = api_path + '/'
		api_path = api_path + str(record_id)
		api_path = api_path + '/Locking_Information__s'
		handler_instance.set_api_path(api_path)
		handler_instance.set_http_method(Constants.REQUEST_METHOD_POST)
		handler_instance.set_category_method(Constants.REQUEST_CATEGORY_CREATE)
		handler_instance.set_content_type('application/json')
		handler_instance.set_request(request)
		handler_instance.set_mandatory_checker(True)
		try:
			from zohocrmsdk.src.com.zoho.crm.api.record_locking.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def get_record_lock_information_by_id(self, lock_id, record_id, module_name, param_instance=None):
		"""
		The method to get record lock information_by_id

		Parameters:
			lock_id (int) : An int representing the lock_id
			record_id (int) : An int representing the record_id
			module_name (string) : A string representing the module_name
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zohocrmsdk.src.com.zoho.crm.api import ParameterMap
		except Exception:
			from ..parameter_map import ParameterMap

		if not isinstance(lock_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: lock_id EXPECTED TYPE: int', None, None)
		
		if not isinstance(record_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: record_id EXPECTED TYPE: int', None, None)
		
		if not isinstance(module_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_name EXPECTED TYPE: str', None, None)
		
		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v5/'
		api_path = api_path + str(module_name)
		api_path = api_path + '/'
		api_path = api_path + str(record_id)
		api_path = api_path + '/Locking_Information__s/'
		api_path = api_path + str(lock_id)
		handler_instance.set_api_path(api_path)
		handler_instance.set_http_method(Constants.REQUEST_METHOD_GET)
		handler_instance.set_category_method(Constants.REQUEST_CATEGORY_READ)
		handler_instance.set_param(param_instance)
		try:
			from zohocrmsdk.src.com.zoho.crm.api.record_locking.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def update_lock_reason_of_a_record(self, lock_id, record_id, module_name, request):
		"""
		The method to update lock reason of a record

		Parameters:
			lock_id (int) : An int representing the lock_id
			record_id (int) : An int representing the record_id
			module_name (string) : A string representing the module_name
			request (BodyWrapper) : An instance of BodyWrapper

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zohocrmsdk.src.com.zoho.crm.api.record_locking.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if not isinstance(lock_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: lock_id EXPECTED TYPE: int', None, None)
		
		if not isinstance(record_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: record_id EXPECTED TYPE: int', None, None)
		
		if not isinstance(module_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_name EXPECTED TYPE: str', None, None)
		
		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v5/'
		api_path = api_path + str(module_name)
		api_path = api_path + '/'
		api_path = api_path + str(record_id)
		api_path = api_path + '/Locking_Information__s/'
		api_path = api_path + str(lock_id)
		handler_instance.set_api_path(api_path)
		handler_instance.set_http_method(Constants.REQUEST_METHOD_PUT)
		handler_instance.set_category_method(Constants.REQUEST_CATEGORY_UPDATE)
		handler_instance.set_content_type('application/json')
		handler_instance.set_request(request)
		handler_instance.set_mandatory_checker(True)
		try:
			from zohocrmsdk.src.com.zoho.crm.api.record_locking.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def remove_lock_for_a_record(self, lock_id, record_id, module_name):
		"""
		The method to remove lock for a record

		Parameters:
			lock_id (int) : An int representing the lock_id
			record_id (int) : An int representing the record_id
			module_name (string) : A string representing the module_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if not isinstance(lock_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: lock_id EXPECTED TYPE: int', None, None)
		
		if not isinstance(record_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: record_id EXPECTED TYPE: int', None, None)
		
		if not isinstance(module_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v5/'
		api_path = api_path + str(module_name)
		api_path = api_path + '/'
		api_path = api_path + str(record_id)
		api_path = api_path + '/Locking_Information__s/'
		api_path = api_path + str(lock_id)
		handler_instance.set_api_path(api_path)
		handler_instance.set_http_method(Constants.REQUEST_METHOD_DELETE)
		handler_instance.set_category_method(Constants.REQUEST_METHOD_DELETE)
		try:
			from zohocrmsdk.src.com.zoho.crm.api.record_locking.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')


class getrecordlockinformationParam(object):
	fields = Param('fields', 'com.zoho.crm.api.RecordLocking.getrecordlockinformationParam')


class getrecordlockinformation_by_idParam(object):
	fields = Param('fields', 'com.zoho.crm.api.RecordLocking.getrecordlockinformation_by_idParam')
