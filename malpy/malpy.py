## malpy.py               Dana Hughes           17-Dec-2019
##
## A set of classes to simpify the interface between Python and  Malmo.
##
## Revision History:
##    17-Dec-2019    Initial Version.

from __future__ import print_function

import MalmoPython
import os
import sys


class AbstractAgent:
	"""
	AbstractAgent is used to define an agent in Minecraft.  The class is
	abstract to provide a common interface to specific agent.
	"""

	def __init__(self):
		"""
		"""

		raise NotImplementedError


	def get_xml(self):
		"""
		Get the XML representation of the agent to be added to the mission
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


class ModSettings:
	"""
	Container for Mission ModSettings.

	Provides optional XML elements for modsettings, specifically, MsPerTick and
	PrioritiseOffscreenRendering.
	"""

	## ModSettings XML template
	xml_template =  """
					<ModSettings>
						{ms_per_tick_xml}
						{render_priority_xml}
					</ModSettings>
					"""

	## Optional XML elements
	ms_per_tick_xml = """<MsPerTick>{ms_per_tick}</MsPerTick>"""
	render_priority_xml = """<PrioritiseOffscreenRendering>{prioritise_rendering}</PrioritiseOffscreenRendering>"""


	def __init__(self, **kwargs):
		"""
		Create a ModSettings element contatiner.  

		ModSettings are used to define how fast the game runs, as well as
		offscreen rendering priority.  This container will only create a ModSettings
		element if one of the optional arguments is provided, and will only
		create elements for the provided arguments.

		Optional Arguments
		------------------
		ms_per_tick (int)         - number of milliseconds between game ticks (i.e., game speed)
		render_priority (boolean) - 
		"""

		self.xml = ModSettings.xml_template

		# 


class Mission:
	"""
	Container for Malmo Mission definitions.

	Mission is used to generate and start an AgentHost.  The purpose
	of the class is to allow for simple composition of mission specs (e.g., 
	observations, mission goals, etc.) using a set of class instances, as 
	opposed to XML definitions
	"""

	## Top-level XML template missions
	xml_template =  """
					<?xml version="1.0" encoding="UTF-8" standalone="no" ?>

					<Mission xmlns="http://ProjectMalmo.microsoft.com" 
					   		 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
					   		 xsi:schemaLocation="http://ProjectMalmo.microsoft.com Mission.xsd">

						<About>
							<Summary>{summary}</Summary>
							{description_xml}
						</About>

						{modsettings}

						{server}

						{agents}
					</Mission>
				    """

	## Optional XML elements
	# description_template - optional description for the About element
	description_template = """<Description>{description}</Description>"""


	def __init__(self, *args, **kwargs):
		"""
		Creates a new instance of a Mission.

		The Mission constructor will accept an arbitrary number of arguments
		defining aspects of the Mission.  Each argument needs to be an instance
		of one of the accepted argument types. 

		Only a the first instance of ModSettings, ServerHandler or ServerInitialConditions
		will be processed, additional instances will be ignored with a warning thrown.
		An arbitrary number of Agent instances will be accepted.

		Additionally, optional keyword arguments providing a summary and description of 
		the mission will be accepted.


		Accepted Argument Types
		-----------------------
			ModSetting
			AbstractServerHandler
			ServerInitialCondition
			AbstractAgent


		Optional Keyword Arguments
		--------------------------
			about (string)       - a summary of the Mission
			                       default = "Malmo Mission"
			description (string) - a description of the Mission 
			                       default = None
		"""


		# Create an instance of the XML template for later population
		self.xml = Mission.xml_template

		# Process the keyword arguments to gather the necessary strings for
		# the About element
		self.about_summary = kwargs.get("about", "Malmo Mission")
		description = kwargs.get("description")

		# Write the Description element in the About element if a description
		# has been provided
		if description is not None:
			self.about_description = Mission.description_template.format(description=description)
		else:
			self.about_description = ""


		# Components 
		self.modsettings = None
		self.server = None
		self.agents = []

