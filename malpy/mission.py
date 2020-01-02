## mission.py               Dana Hughes           17-Dec-2019
##
## A set of classes to simpify the interface between Python and  Malmo.
##
## Revision History:
##    17-Dec-2019    Initial Version.
##    23-Dec-2019    Separated server and agent objects into their 
##                   own python files

from __future__ import print_function

from functools import reduce
import operator

from container import Container
from agents import *
from servers import *

import MalmoPython


class ModSettings(Container):
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

		# Process the keyword arguments
		self.ms_per_tick = kwargs.get('ms_per_tick')
		self.render_priority = kwargs.get('render_priority')

		# Keep the xml empty until needed
		self.xml = ""


	def __ms_per_tick_to_xml(self):
		"""
		Validates and converts the ms_per_tick attribute to a value suitable for XML
		"""

		# Do nothing if there isn't the attribute
		if self.ms_per_tick is None:
			return

		# TODO: Validate that the ms_per_tick value can actually be converted to an int
		self.ms_per_tick = int(self.ms_per_tick)

		assert self.ms_per_tick >= 1, "Minimum value of MsPerTick is 1.  Provided value: %d" % self.ms_per_tick

		# Convert to string for use in XML
		self.ms_per_tick = str(self.ms_per_tick)


	def __render_priority_to_xml(self):
		"""
		Validates and converts the render_priority attribute to a value suitable for XML
		"""

		# Do nothing if there isn't the attribute
		if self.render_priority is None:
			return

		# Convert to a "true" or "false" string
		self.render_priority = "true" if self.render_priority else "false"


	def constructXml(self):
		"""
		Construct and return the ModSettings XML element.
		"""

		# Validate each of the attributes
		self.__ms_per_tick_to_xml()
		self.__render_priority_to_xml()

		# Create XML elements for each optional argument
		self.xml_MsPerTick = None
		self.xml_PrioritiseOffscreenRendering = None

		# Fill in the templates if arguments are available.
		if self.ms_per_tick is not None:
			self.xml_MsPerTick = ModSettings.ms_per_tick_xml.format(ms_per_tick=self.ms_per_tick)

		if self.render_priority is not None:
			self.xml_PrioritiseOffscreenRendering = ModSettings.render_priority_xml.format(prioritize_rendering=render_priority)

		# Construct the XML element if either element has been defined
		if self.xml_MsPerTick is not None or self.xml_PrioritiseOffscreenRendering is not None:
			# If either element is None, convert to an empty string
			ms_per_tick_xml = self.xml_MsPerTick if self.xml_MsPerTick is not None else ""
			render_priority_xml = self.xml_PrioritiseOffscreenRendering if self.xml_PrioritiseOffscreenRendering is not None else ""

			self.xml = ModSettings.xml_template.format(ms_per_tick_xml=ms_per_tick_xml, render_priority_xml=render_priority_xml)

		return self.xml




class Mission(Container):
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
		self.server_initial_condition = None
		self.agents = []

		# Parse through the argument list, assigning to attributes based on object type
		for arg in args:

			# Is the argument an instance of ModSettings?
			if isinstance(arg, ModSettings):

				# Only set this argument as the modsettings attribute if one 
				# doesn't exist, otherwise, throw a warning
				if self.modsettings is None:
					self.modsettings = arg
				else:
					print("WARNING: ModSettings instance already provided, ignoring new instance.")

			# Not a supported argument type
			else:
				print("WARNING: Unknown argument type.  Ignoring.")


	def constructXml(self):
		"""
		Construct and return the Mission XML element.  Recursively constructs the modsettings,
		server, and any agents that the container knows about.
		""" 

		# Get the XML string of each element.  At a minimum, modsettings and
		# server need to be defined; throw an error if these are not provided.

		if self.modsettings is None: # or self.server is None:
			print("ERROR: ModSettings not provided, unable to construct XML.")
			return
		
		if self.server is None:
			print("ERROR: Server not provided, unable to construct XML.")
			return

		# Required containers have been provided, construct the XML
		modsettings_xml = self.modsettings.constructXml()
		server_xml = ''

		# Construct the XML for all agents and concatenate to a single XML string
		agents_xml = reduce(operator.add, [agent.constructXml() for agent in self.agents], '')

		# Create the XML
		self.xml = Mission.xml_template.format(summary=self.about_summary,
											   description_xml=self.about_description,
											   modsettings=modsettings_xml,
											   server=server_xml,
											   agents=agents_xml)

		return self.xml