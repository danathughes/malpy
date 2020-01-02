## agents.py               Dana Hughes           23-Dec-2019
##
## A set of classes defining agents for use in Malmo.
##
## Revision History:
##    23-Dec-2019    Initial Version.

from container import Container


class AbstractAgent(Container):
	"""
	AbstractAgent is used to define an agent in Minecraft.  The class is
	abstract to provide a common interface to specific agent.
	"""

	def __init__(self):
		"""
		An abstract representation of a Malmo agent.
		"""

		# Call the superclass constructor
		Container.__init__(self)

		raise NotImplementedError


	def constructXml(self):
		"""
		Get the XML representation of the agent to be added to the mission.
		"""

		raise NotImplementedError



class ObserverAgent(AbstractAgent):
	"""
	ObserverAgent is an agent that provides observations of certain regions of
	the environment.
	"""

	def __init__(self):
		"""
		"""

		raise NotImplementedError


	def constructXml(self):
		"""
		"""

		raise NotImplementedError


