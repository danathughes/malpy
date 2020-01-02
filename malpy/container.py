## container.py               Dana Hughes           30-Dec-2019
##
## An abstract representation of elements defining a Mission.  
##
## Revision History:
##    30-Dec-2019    Initial Version.

class Container:
	"""
	A container is an abstract representation of a mission element.  This is 
	simply used to define a common interface for all containers used by malpy.
	"""

	def __init__(self, **kwargs):
		"""
		Create a new container.
		"""

		raise NotImplementedError


	def constructXml(self):
		"""
		Generate an XML string representation of the container.
		"""

		raise NotImplementedError
