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

import logging

from labbenchstudios.pdt.edge.app.EventDispatchManager import EventDispatchManager
# from labbenchstudios.pdt.edge.connection.InfluxClientConnector import InfluxClientConnector
from labbenchstudios.pdt.edge.connection.MqttClientConnector import MqttClientConnector

from labbenchstudios.pdt.edge.system.WindTurbineAdapterManager import WindTurbineAdapterManager
from labbenchstudios.pdt.edge.system.ActuatorAdapterManager import ActuatorAdapterManager
from labbenchstudios.pdt.edge.system.SensorAdapterManager import SensorAdapterManager
from labbenchstudios.pdt.edge.system.SystemPerformanceManager import SystemPerformanceManager

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener
from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum

from labbenchstudios.pdt.data.DataUtil import DataUtil
from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData

class DeviceDataManager(IDataMessageListener):
	"""
	This class is the entry point for all other managers, such as the SystemPerformanceManager,
	Connection Client(s), and Persistence Utilities used by the main application.
	
	It also implements the data messaging callback interface(s) used for directing data
	from one manager to another. For instance, if system performance data is received
	via one of the implemented callbacks, it can be packaged appropriately and sent
	on to one of the communication mechanisms implemented in the connection client.
	
	NOTE: This is NOT a thread-safe class by design; however, the EventDispatchManager
	is designed to sequentially process incoming and outgoing messages via a sync'd queue
	on a separate thread. All incoming and outgoing messages should be handled via
	the EventDispatchManager to ensure DeviceDataManager calls on the main thread
	are not blocked.
	"""
	
	def __init__(self):
		"""
		Constructor.
		
		"""
		self.configUtil = ConfigUtil()
		
		self.tsdbClient         = None
		self.mqttClient         = None
		self.sysPerfMgr         = None
		self.sensorAdapterMgr   = None
		self.actuatorAdapterMgr = None

		self.windTurbineMgr        = None
		self.roboticManipulatorMgr = None

		self.actuatorResponseCache = None
		self.sensorDataCache = None
		self.sysPerfDataCache = None

		# init config settings first, then init all the manager components
		self._initConfigurationSettings()
		self._initManager()
	
	def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
		"""
		Retrieves the named actuator data (response) item from the internal data cache.
		
		@param name
		@return ActuatorData
		"""
		if name:
			if name in self.actuatorResponseCache:
				return self.actuatorResponseCache[name]
			
		return None
		
	def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
		"""
		Retrieves the named sensor data item from the internal data cache.
		
		@param name
		@return SensorData
		"""
		if name:
			if name in self.sensorDataCache:
				return self.sensorDataCache[name]
			
		return None
	
	def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
		"""
		Retrieves the named system performance data from the internal data cache.
		
		@param name
		@return SystemPerformanceData
		"""
		if name:
			if name in self.sysPerfDataCache:
				return self.sysPerfDataCache
		
		return None
	
	def handleActuatorCommandMessage(self, data: ActuatorData = None) -> ActuatorData:
		"""
		Callback function to handle an actuator command message packaged as a ActuatorData object.
		
		@param data The ActuatorData message received.
		@return bool True on success; False otherwise.
		"""
		if data:
			logging.info( \
				"\n\nvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv" \
				"\n\nactuator command message." \
				"\n\tState: " + str(data.getStateData()) + \
				"\n\tValue: " + str(data.getValue()) + \
				"\n\tData:  " + str(data) + \
				"\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
			
			# we need to do two things:
			# - notify our simulation engine (if it's running),
			#   as this command may reset the simulation dataset
			# - notify our actuator manager so it can handle
			#   the actuation event
			isHandled = False

			if self.enableSimEngineUpdates:
				if (data.getTypeCategoryID() == ConfigConst.ENERGY_TYPE_CATEGORY):
					if self.windTurbineMgr:
						self.windTurbineMgr.updateSimulationData(data = data)
						isHandled = True
				else:
					if self.sensorAdapterMgr:
						self.sensorAdapterMgr.updateSimulationData(data = data)
						isHandled = True

			if (isHandled):
				return data
			else:
				return self.actuatorAdapterMgr.sendActuatorCommand(data = data)
		else:
			logging.warning("Incoming actuator command is invalid (null). Ignoring.")
			
			return None
		
	def handleActuatorCommandResponse(self, data: ActuatorData = None) -> bool:
		"""
		Callback function to handle an actuator command response packaged as a ActuatorData object.
		
		@param data The ActuatorData message received.
		@return bool True on success; False otherwise.
		"""
		if data:
			logging.debug("Incoming actuator response received (likely from internal component): " + str(data))
			
			if not data.isResponseFlagEnabled():
				logging.warning("Incoming actuator response not set as response. Updating.")
				data.setAsResponse()

			# store the data in the cache
			if (self.actuatorResponseCache):
				self.actuatorResponseCache[data.getName()] = data

			# store the data in the TSDB (if enabled)
			if (self.tsdbClient):
				self.tsdbClient.storeActuatorData(data = data)
			
			# convert ActuatorData to JSON and get the msg resource
			actuatorMsg = DataUtil().actuatorDataToJson(data)
			resourceName = ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE
			
			# delegate to the transmit function any potential upstream comm's
			self._processUpstreamTransmission(resource = resourceName, msg = actuatorMsg)
			
			return True
		else:
			logging.warning("Incoming actuator response is invalid (null). Ignoring.")
			
			return False
	
	def handleSensorMessage(self, data: SensorData = None) -> bool:
		"""
		Callback function to handle a sensor message packaged as a SensorData object.
		
		@param data The SensorData message received.
		@return bool True on success; False otherwise.
		"""
		if data:
			logging.info("Incoming sensor data received (from sensor manager): " + str(data))
			
			# store the data in the TSDB (if enabled)
			if (self.tsdbClient):
				self.tsdbClient.storeSensorData(data = data)
			
			# handle any local data analysis (this may trigger an actuation event)
			self._processSensorDataAnalysis(data)
			
			jsonData = DataUtil().sensorDataToJson(data = data)
			self._processUpstreamTransmission(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = jsonData)
			
			return True
		else:
			logging.warning("Incoming sensor data is invalid (null). Ignoring.")
			
			return False
		
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData = None) -> bool:
		"""
		Callback function to handle a system performance message packaged as
		SystemPerformanceData object.
		
		@param data The SystemPerformanceData message received.
		@return bool True on success; False otherwise.
		"""
		if data:
			logging.info("Incoming system performance message received (from sys perf manager): " + str(data))
			
			# store the data in the TSDB (if enabled)
			if (self.tsdbClient):
				self.tsdbClient.storeSystemPerformanceData(data = data)
			
			jsonData = DataUtil().systemPerformanceDataToJson(data = data)
			self._processUpstreamTransmission(resource = ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, msg = jsonData)
			
			return True
		else:
			logging.warning("Incoming system performance data is invalid (null). Ignoring.")
		
			return False
	
	def handleIncomingMessage(self, resource = None, msg: str = None) -> bool:
		"""
		Callback function to handle incoming messages on a given topic with
		a string-based payload.
		
		@param resourceEnum The topic enum associated with this message.
		@param msg The message received. It is expected to be in JSON format.
		@return bool True on success; False otherwise.
		"""
		if resource and msg:
			logging.info("Incoming msg received. Topic: %s  Payload: %s", str(resource), msg)
			
			# delegate the internal analysis / action of the message
			self._processIncomingDataAnalysis(msg)
			
			return True
		else:
			logging.warning("Incoming msg or resource reference is invalid (null). Ignoring.")
			
			return False

	def startManager(self):
		"""
		Starts the manager - this will invoke the start methods on
		the connection client and system performance manager.
		
		"""
		logging.info("Starting DeviceDataManager...")
		
		# Event Dispatch Manager start / stop sequence
		# START: BEFORE any other manager
		if self.eventDispatchMgr:
			logging.info("Starting event dispatch manager...")
			self.eventDispatchMgr.startManager()

		if self.mqttClient:
			self.mqttClient.connectClient()
		
		if self.windTurbineMgr:
			self.windTurbineMgr.startManager()

		if self.sysPerfMgr:
			self.sysPerfMgr.startManager()
		
		if self.sensorAdapterMgr:
			self.sensorAdapterMgr.startManager()

		if self.tsdbClient:
			self.tsdbClient.connectClient()
			
		logging.info("Started DeviceDataManager.")
		
	def stopManager(self):
		"""
		Stops the manager - this will invoke the stop methods on
		the connection client and system performance manager.
		
		"""
		logging.info("Stopping DeviceDataManager...")
		
		if self.windTurbineMgr:
			self.windTurbineMgr.stopManager()

		if self.sysPerfMgr:
			self.sysPerfMgr.stopManager()
		
		if self.sensorAdapterMgr:	
			self.sensorAdapterMgr.stopManager()
			
		# Event Dispatch Manager start / stop sequence
		# STOP: AFTER sim's are stopped (to ingress any remaining sim data items)
		# STOP: BEFORE connections are stopped (to egress any remaining sim data items)
		if self.eventDispatchMgr:
			logging.info("Stopping event dispatch manager...")
			self.eventDispatchMgr.stopManager()
			
		if self.mqttClient:
			self.mqttClient.unsubscribeFromTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)
			self.mqttClient.disconnectClient()
				
		if self.tsdbClient:
			self.tsdbClient.disconnectClient()
		
		logging.info("Stopped DeviceDataManager.")
		
	def _initConfigurationSettings(self):
		"""
		Checks the configuration file to initialize class-scoped var's and properties.
		This will determine which - if any - managers are initialized.
		"""
		self.deviceID     = \
			self.configUtil.getProperty( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.DEVICE_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		self.locationID   = \
			self.configUtil.getProperty( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		self.handleTempChangeOnDevice = \
			self.configUtil.getBoolean( \
				section = ConfigConst.ENVIRONMENTAL_SETTINGS_KEY, key = ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
			
		self.triggerHvacTempFloor     = \
			self.configUtil.getFloat( \
				section = ConfigConst.ENVIRONMENTAL_SETTINGS_KEY, key = ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)
				
		self.triggerHvacTempCeiling   = \
			self.configUtil.getFloat( \
				section = ConfigConst.ENVIRONMENTAL_SETTINGS_KEY, key = ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)
		
		self.enableEnvActuationEvents    = \
			self.configUtil.getBoolean( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.ENABLE_ACTUATION_KEY)
		
		self.enableEnvSensingEvents      = \
			self.configUtil.getBoolean( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.ENABLE_SENSING_KEY)
		
		self.enableMqttClient = \
			self.configUtil.getBoolean( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.ENABLE_MQTT_CLIENT_KEY)
		
		self.enableTsdbClient = \
			self.configUtil.getBoolean( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.ENABLE_TSDB_CLIENT_KEY)
		
		self.enableEventBasedDisplayUpdates = \
			self.configUtil.getBoolean( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.SEND_EVENT_DISPLAY_UPDATES_KEY)
		
		self.enableSimEngineUpdates = \
			self.configUtil.getBoolean( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.ENABLE_SIM_ENGINE_UPDATES)
		
		self.enableSystemPerfEvents   = \
			self.configUtil.getBoolean( \
				section = ConfigConst.SYSTEM_PERF_SETTINGS_KEY, key = ConfigConst.ENABLE_OPERATION_KEY)
			
		self.enableWindTurbineSim   = \
			self.configUtil.getBoolean( \
				section = ConfigConst.WIND_TURBINE_SETTINGS_KEY, key = ConfigConst.ENABLE_OPERATION_KEY)
			
		self.enableFactoryWorkCellSim   = \
			self.configUtil.getBoolean( \
				section = ConfigConst.FACTORY_WORKCELL_SETTINGS_KEY, key = ConfigConst.ENABLE_OPERATION_KEY)
			
	def _initManager(self):
		"""
		Simple method for initializing DeviceDataManager's internally managed managers,
		along with the EventDispatchManager, which will handle all incoming and outgoing
		messages in a thread-safe and orderly fashion.
		
		"""
		# initialize the event dispatch manager
		self.eventDispatchMgr = EventDispatchManager(dataMsgListener = self)

		if self.enableTsdbClient:
			self.tsdbClient = InfluxClientConnector(dataMsgListener = self.eventDispatchMgr)
			logging.info("TSDB connector enabled")

		if self.enableMqttClient:
			self.mqttClient = MqttClientConnector()
			self.mqttClient.setDataMessageListener(self.eventDispatchMgr)
			logging.info("MQTT connector enabled")
			
		if self.enableSystemPerfEvents:
			self.sysPerfMgr = SystemPerformanceManager()
			self.sysPerfMgr.setDataMessageListener(self.eventDispatchMgr)
			logging.info("Local system performance tracking enabled")
		
		if self.enableEnvSensingEvents:
			self.sensorAdapterMgr = SensorAdapterManager()
			self.sensorAdapterMgr.setDataMessageListener(self.eventDispatchMgr)
			logging.info("Local sensor tracking enabled")
			
		if self.enableEnvActuationEvents:
			self.actuatorAdapterMgr = ActuatorAdapterManager(dataMsgListener = self.eventDispatchMgr)
			logging.info("Local actuation capabilities enabled")

		if self.enableWindTurbineSim:
			self.windTurbineMgr = WindTurbineAdapterManager()
			self.windTurbineMgr.setDataMessageListener(self.eventDispatchMgr)
			logging.info("Local wind turbine management enabled")
		
		if self.enableFactoryWorkCellSim:
			#self.factoryWorkcellMgr = FactoryWorkcellManager()
			#self.factoryWorkcellMgr.setDataMessageListener(self.eventDispatchMgr)
			logging.info("TEST LOG MSG ONLY: Factory workcell sim enabled")
		
	def _processIncomingDataAnalysis(self, resource = None, msg: str = None):
		"""
		Check the incoming msg data against known JSON schema's and see
		if there's a way to convert it to an internal object - such as
		an ActuatorData or a SensorData object - and take the appropriate
		action (e.g. send a command to an actuator).
		
		The current implementation assumes msg is JSON and conforms
		to ActuatorData formatting. An attempt will be made to transform
		msg to an ActuatorData instance - on success, it will be
		sent to the actuator manager for processing; on failure,
		a warning message will be logged.
		
		@param msg The JSON data (presumably) that represents an
		ActuatorData formatted object (presumably).
		"""
		try:
			ad = DataUtil().jsonToActuatorData(msg)
			
			if ad:
				logging.info("Sending actuator command to actuator manager: ", msg)
				
				self.actuatorAdapterMgr.sendActuatorCommand(ad)
			else:
				logging.warning("Conversion of message to ActuatorData resulted in null ref: ", msg)
		except:
			logging.warning("Failed to convert message to ActuatorData: ", msg)
		
	def _processSensorDataAnalysis(self, data: SensorData = None):
		"""
		Check if the data requires any internal action (such as
		enabling / disabling an actuator), and execute that action.
		
		The current implementation will check if we received temperature
		data that requires an HVAC state change. This is a VERY simple
		implementation that will trigger an HVAC actuator update to
		raise the temp if the floor value is exceeded, or lower the
		temp if the ceiling value is exceeded.
		
		This function will NOT check current status of the target
		actuator, so if invoked, will always send either an ON
		or OFF ActuatorData command to the actuator manager.
		
		@param data
		"""
		
		if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
			logging.info("Handle temp change: %s - type ID: %s", \
				str(self.handleTempChangeOnDevice), str(data.getTypeID()))
			
			ad = ActuatorData( \
				name = ConfigConst.HVAC_ACTUATOR_NAME, \
				typeCategoryID = ConfigConst.ENV_TYPE_CATEGORY, \
				typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
			
			ad.setDeviceID(self.deviceID)
			ad.setLocationID(self.locationID)

			if data.getValue() > self.triggerHvacTempCeiling:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempCeiling)
			elif data.getValue() < self.triggerHvacTempFloor:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempFloor)
			else:
				ad.setCommand(ConfigConst.COMMAND_OFF)
				
			# NOTE: ActuatorAdapterManager and its associated actuator
			# task implementations contain logic to avoid processing
			# duplicative actuator commands - for the purposes
			# of this exercise, the logic for filtering commands is
			# left to ActuatorAdapterManager and its associated actuator
			# task implementations, and not this function
			self.handleActuatorCommandMessage(ad)

		elif (self.enableEventBasedDisplayUpdates):
			logging.info('Generating LED display message for actuator command [non-actionable]...')

			ad = ActuatorData( \
				name = ConfigConst.LED_ACTUATOR_NAME, \
				typeCategoryID = ConfigConst.SYSTEM_MGMT_TYPE, \
				typeID = ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)

			ad.setDeviceID(self.deviceID)
			ad.setLocationID(self.locationID)
			
			ad.setValue(data.getValue())
			ad.setCommand(ConfigConst.COMMAND_MSG_ONLY)
			ad.setStateData(data.getName() + ': ' + str(data.getValue()))
			
			self.handleActuatorCommandMessage(ad)
	
	def _processUpstreamTransmission(self, resource = None, msg: str = None):
		"""
		Checks if we have a valid MQTT and / or CoAP client connection, and if so,
		transmit the msg data to the resource given using one or both protocols.
		
		@param resourceName The resource to use for the destination.
		@param msg The JSON formatted message to transmit.
		"""
		logging.info("Upstream transmission invoked. Checking comm's integration.")
		
		# NOTE: If using TSDB, the following will attempt to write the message to the TSDB server
		if self.tsdbClient:
			pass
			#if self.tsdbClient.storeData(resource = resource, msg = msg):
			#	logging.debug("Writing incoming data to resource (TSDB): %s", str(resource))
			#else:
			#	logging.warning("Failed to write incoming data to resource (TSDB): %s", str(resource))

		# NOTE: If using MQTT, the following will attempt to publish the message to the broker
		if self.mqttClient:
			if self.mqttClient.publishMessage(resource = resource, msg = msg):
				logging.debug("Published incoming data to resource (MQTT): %s", str(resource))
			else:
				logging.warning("Failed to publish incoming data to resource (MQTT): %s", str(resource))
			