##
# MIT License
# 
# Copyright (c) 2020 - 2024 Andrew D. King
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import configparser
import logging
import os
import traceback

from pathlib import Path

from labbenchstudios.pdt.common.Singleton import Singleton

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

class ConfigUtil(metaclass = Singleton):
	"""
	A simple utility wrapper around the built-in Python
	configuration infrastructure.
	
	Implemented as a Singleton using the Singleton metaclass.
	
	"""
	enableConfigFileSearch = True

	configFile   = None
	configParser = configparser.ConfigParser()
	isLoaded	 = False

	failedLoadCounter = 0

	def __init__(self, configFile: str = None):
		"""
		Constructor for ConfigUtil.
		
		@param configFile The name of the configuration file to load.
		"""
		self.configFile = configFile

		logging.info("Creating instance of ConfigUtil: %s", self.configFile)
	
		self._loadConfig()

	#
	# public methods
	#
	def getConfigFileName(self) -> str:
		"""
		Returns the name of the configuration file.
		
		@return The name of the config file.
		"""
		return self.configFile

	def getCredentials(self, section: str) -> dict:
		"""
		Attempts to load a separate configuration 'credential' file comprised
		of simple key = value pairs. The assumption with this call is that
		the credential file key is the same across all sections, so the
		only parameter requires is the section.
		
		If the credential file key has an entry (e.g. the file where the
		credentials are stored in key = value form), the file will be
		loaded if possible, and a dict object will be returned
		to the caller. No caching of the data is made, except within the
		returned dict object.
		
		NOTE: The key case IS preserved.
		
		@param section
		@return dict The dictionary of properties, or None if non-existent.
		"""
		if (self.hasSection(section)):
			credFileName = self.getProperty(section, ConfigConst.CRED_FILE_KEY);
			
			try:
				if os.path.exists(credFileName) and os.path.isfile(credFileName):
					logging.info("Loading credentials from section " + section + " and file " + credFileName)
					
					# read cred data and dump it into a custom section for parsing
					fileRef  = Path(credFileName)
					credData = "[" + ConfigConst.CRED_SECTION + "]\n" + fileRef.read_text()
					
					# create unique ConfigParser that preserves key case
					credParser = configparser.ConfigParser()
					credParser.optionxform = str
					
					# read the stringified file data and generate / return
					# a dict for the section we just created
					credParser.read_string(credData)
					credProps = dict(credParser.items(ConfigConst.CRED_SECTION))
					
					return credProps
				else:
					logging.warn("Credential file doesn't exist: " + credFileName)
			except Exception as e:
				traceback.print_exc()
				logging.warn("Failed to load credentials from file: " + credFileName + ". Exception: " + str(e))
		
		return None
	
	def getProperty(self, section: str, key: str, defaultVal: str = None, forceReload: bool = False):
		"""
		Attempts to retrieve the value of 'key' from the config.
		
		@param section The name of the section to parse.
		@param key The name of the key to lookup in 'section'.
		@param forceReload Defaults to false; if true will reload the config.
		@return The property associated with 'key' in 'section'.
		"""
		return self._getConfig(forceReload).get(section, key, fallback = defaultVal)
	
	def getBoolean(self, section: str, key: str, forceReload: bool = False):
		"""
		Attempts to retrieve the boolean value of 'key' from the config.
		If not found, or not True, False will be returned.
		
		@param section The name of the section to parse.
		@param key The name of the key to lookup in 'section'.
		@param forceReload Defaults to false; if true will reload the config.
		@return The boolean associated with 'key' in 'section', or false.
		"""
		return self._getConfig(forceReload).getboolean(section, key, fallback = False)
		
	def getInteger(self, section: str, key: str, defaultVal: int = 0, forceReload: bool = False):
		"""
		Attempts to retrieve the integer value of 'key' from the config.
		
		@param section The name of the section to parse.
		@param key The name of the key to lookup in 'section'.
		@param defaultVal The default value if section, key, or value doesn't exist (or is invalid).
		@param forceReload Defaults to false; if true will reload the config.
		@return The property associated with 'key' in 'section'.
		"""
		return self._getConfig(forceReload).getint(section, key, fallback = defaultVal)
	
	def getFloat(self, section: str, key: str, defaultVal: float = 0.0, forceReload: bool = False):
		"""
		Attempts to retrieve the float value of 'key' from the config.
		
		@param section The name of the section to parse.
		@param key The name of the key to lookup in 'section'.
		@param defaultVal The default value if section, key, or value doesn't exist (or is invalid).
		@param forceReload Defaults to false; if true will reload the config.
		@return The property associated with 'key' in 'section'.
		"""
		return self._getConfig(forceReload).getfloat(section, key, fallback = defaultVal)
	
	def hasProperty(self, section: str, key: str) -> bool:
		"""
		Checks if a given 'key' exists in the named section of the loaded config.
		
		@param section The name of the section to search.
		@param key The name of the key to lookup in 'section'.
		@return True if 'key' is found in 'section'; False otherwise.
		"""
		return self._getConfig().has_option(section, key)
		
	def hasSection(self, section: str) -> bool:
		"""
		Checks if a given 'section' exists in the loaded config.
		
		@param section The name of the section to search.
		@return True if 'section' exists and has parameters; false otherwise.
		"""
		return self._getConfig().has_section(section)
		
	def isConfigDataLoaded(self) -> bool:
		"""
		Simple boolean check if the config data is loaded or not.
		
		@return boolean True on success; False otherwise.
		"""
		return self.isLoaded
	
	#
	# private methods
	#
	
	def _getConfig(self, forceReload: bool = False) -> configparser:
		"""
		Returns the entire configuration object. If the config file hasn't
		yet been loaded, it will be loaded.
		
		@param forceReload Defaults to false; if true, will reload the config.
		@return The entire configuration file.
		"""
		if (self.isLoaded == False or forceReload):
			self._loadConfig()
		
		return self.configParser
	
	def _loadConfig(self):
		"""
		Attempts to load the config file using the name passed into
		the constructor.
		 
		"""
		if (self.failedLoadCounter == 0):
			if (self.configFile):
				# try to load the config file requested
				self._loadConfigFile(self.configFile)

			elif (self.enableConfigFileSearch):
				# if no config file is specified, search upwards for the
				# 'config' path and - if found - try to load the default
				# config file name (ConfigConst.CONFIG_FILE)
				logging.info("Attempting to locate %s.", ConfigConst.CONFIG_FILE)
				self._locateAndInitDefaultConfigFileName()

		if (not self.isLoaded):
			self.failedLoadCounter += 1
		
	def _loadConfigFile(self, configFile):
		"""
		"""
		if (configFile):
			if (os.path.exists(configFile)):
				logging.info("Attempting to load config file: %s", configFile)

				try:
					self.configParser.read(configFile)
					self.isLoaded = True

					# set the configuration file
					self.configFile = configFile

					logging.info("Successfully loaded configuration at %s.", self.configFile)
					logging.debug("Config: %s", str(self.configParser.sections()))

				except:
					logging.error("Failed to load requested config file at %s.", configFile)
			else:
				logging.error("No file exists for requested config file %s.", configFile)
	
	def _locateAndInitDefaultConfigFileName(self):
		"""
		"""
		modulePath = os.path.dirname(__file__)
		parentPaths = Path(modulePath).parents
		parentPathCount = len(parentPaths)

		for i in range(parentPathCount):
			configFile = \
				os.path.abspath( \
					os.path.join( \
						parentPaths[i], \
						'config', \
						ConfigConst.CONFIG_FILE))
			
			logging.info("Searching path %s for config file.", configFile)

			if (os.path.exists(configFile)):
				logging.info("Found configuration file at %s", configFile)

				self._loadConfigFile(configFile)

				return
