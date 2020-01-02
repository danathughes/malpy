## servers.py               Dana Hughes           23-Dec-2019
##
## A set of classes defining servers for use in Malmo.
##
## Revision History:
##    23-Dec-2019    Initial Version.

from container import Container

class AbstractServer(Container):
	"""
	"""

	xml_template =  """
					<ServerSection>
						{initial_conditions}
						<ServerHandlers>
							{generator}
							{decorator}
							{quit_from_time_up}
							{quit_when_agent_finishes}
						</ServerHandlers>
					</ServerSection>
					"""

	quit_from_time_up_template = """<ServerQuitFromTimeUp timeLimitMs="{time_limit}" {description_xml} />"""
	quit_when_agent_finishes_template = """<ServerQuitWhenAnyAgentFinishes {description_xml} />"""

	quit_description_xml = """description="{description}" """


	def __init__(self):
		"""
		"""

		raise NotImplementedError


	def constructXml(self):
		"""
		"""

		raise NotImplementedError


class FlatWorldServer(AbstractServer):
	"""
	"""

	def __init__(self):
		"""
		"""


	def constructXml(self):
		"""
		"""

