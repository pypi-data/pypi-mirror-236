try:
	from zohocrmsdk.src.com.zoho.crm.api.exception import SDKException
	from zohocrmsdk.src.com.zoho.crm.api.util import Constants
except Exception:
	from ..exception import SDKException
	from ..util import Constants


class Address(object):
	def __init__(self):
		"""Creates an instance of Address"""

		self.__address_value_map = None
		self.__key_modified = dict()

	def get_address_value_map(self):
		"""
		The method to get the address_value_map

		Returns:
			AddressValueMap: An instance of AddressValueMap
		"""

		return self.__address_value_map

	def set_address_value_map(self, address_value_map):
		"""
		The method to set the value to address_value_map

		Parameters:
			address_value_map (AddressValueMap) : An instance of AddressValueMap
		"""

		try:
			from zohocrmsdk.src.com.zoho.crm.api.mail_merge.address_value_map import AddressValueMap
		except Exception:
			from .address_value_map import AddressValueMap

		if address_value_map is not None and not isinstance(address_value_map, AddressValueMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: address_value_map EXPECTED TYPE: AddressValueMap', None, None)
		
		self.__address_value_map = address_value_map
		self.__key_modified['Address_Value_Map'] = 1

	def is_key_modified(self, key):
		"""
		The method to check if the user has modified the given key

		Parameters:
			key (string) : A string representing the key

		Returns:
			int: An int representing the modification
		"""

		if key is not None and not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if key in self.__key_modified:
			return self.__key_modified.get(key)
		
		return None

	def set_key_modified(self, key, modification):
		"""
		The method to mark the given key as modified

		Parameters:
			key (string) : A string representing the key
			modification (int) : An int representing the modification
		"""

		if key is not None and not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if modification is not None and not isinstance(modification, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: modification EXPECTED TYPE: int', None, None)
		
		self.__key_modified[key] = modification
