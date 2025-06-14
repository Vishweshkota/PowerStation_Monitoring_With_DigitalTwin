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

"""
Configuration and other constants for use when looking up
configuration values or when default values may be needed.
 
"""

#####
# General Names and Defaults
#

NOT_SET = 'Not Set'
RESOURCE_SEPARATOR_CHAR = '/'
SUB_TYPE_SEPARATOR_CHAR = '-'

DEFAULT_HOST             = 'localhost'
DEFAULT_COAP_PORT        = 5683
DEFAULT_COAP_SECURE_PORT = 5684
DEFAULT_MQTT_PORT        = 1883
DEFAULT_MQTT_SECURE_PORT = 8883
DEFAULT_TSDB_PORT        = 8086
DEFAULT_RTSP_STREAM_PORT = 8554
DEFAULT_KEEP_ALIVE       = 60
DEFAULT_POLL_CYCLES      = 60
DEFAULT_VAL              = 0.0
DEFAULT_COMMAND          = 0
DEFAULT_STATUS           = 0
DEFAULT_TIMEOUT          = 5
DEFAULT_TTL              = 300
DEFAULT_QOS              = 0

# for purposes of this library, float precision is more then sufficient
DEFAULT_LAT = DEFAULT_VAL
DEFAULT_LON = DEFAULT_VAL
DEFAULT_ELEVATION = DEFAULT_VAL

DEFAULT_ACTION_ID = 0
INITIAL_SEQUENCE_NUMBER = 0

DEFAULT_STREAM_FPS             =    30
DEFAULT_MIN_STREAM_FPS         =     8
DEFAULT_MAX_STREAM_FPS         =    60
DEFAULT_STREAM_FRAME_WIDTH     =  1440
DEFAULT_STREAM_FRAME_HEIGHT    =  1080
DEFAULT_MIN_MOTION_PIXELS_DIFF = 12000
DEFAULT_MAX_CACHED_FRAMES      =    10
DEFAULT_STREAM_PROTOCOL        = 'rtsp'
DEFAULT_STREAM_FPS = 30
DEFAULT_MIN_MOTION_PIXELS_DIFF = 10000
DEFAULT_STREAM_PROTOCOL = 'rtsp'

PRODUCT_NAME = 'PDT'
CLOUD        = 'Cloud'
GATEWAY      = 'Gateway'
EDGE         = 'Edge'
CONSTRAINED  = EDGE
# NOTE: CONSTRAINED global name has been changed to use EDGE for PDT
#CONSTRAINED  = 'Constrained'
DEVICE       = 'Device'
SERVICE      = 'Service'

# CONSTRAINED_DEVICE and EDGE_DEVICE will be the same
# They're both used for backwards compatability
CONSTRAINED_DEVICE = CONSTRAINED + DEVICE
EDGE_DEVICE        = EDGE + DEVICE
GATEWAY_SERVICE    = GATEWAY + SERVICE
CLOUD_SERVICE      = CLOUD + SERVICE

#####
# Property Names
#

NAME_PROP        = 'name'
DEVICE_ID_PROP   = 'deviceID'
TYPE_CATEGORY_ID_PROP = 'typeCategoryID'
TYPE_ID_PROP     = 'typeID'
TYPE_NAME_PROP   = 'typeName'
TIMESTAMP_PROP   = 'timeStamp'
HAS_ERROR_PROP   = 'hasError'
STATUS_CODE_PROP = 'statusCode'
LOCATION_ID_PROP = 'locationID'
LATITUDE_PROP    = 'latitude'
LONGITUDE_PROP   = 'longitude'
ELEVATION_PROP   = 'elevation'

COMMAND_PROP     = 'command'
COMMAND_NAME_PROP = 'commandName'
STATE_DATA_PROP  = 'stateData'
IS_RESPONSE_PROP = 'isResponse'

DATA_VALUES_PROP  = 'dataValues'
UNIT_PROP         = 'unit'
VALUE_PROP        = 'value'
TARGET_VALUE_PROP = 'targetValue'
RANGE_NOMINAL_FLOOR_PROP   = 'rangeNominalFloor'
RANGE_NOMINAL_CEILING_PROP = 'rangeNominalCeiling'
RANGE_MAX_FLOOR_PROP       = 'rangeMaxFloor'
RANGE_MAX_CEILING_PROP     = 'rangeMaxCeiling'
NOMINAL_VALUE_DELTA_PROP   = 'nominalValueDelta'
MAX_VALUE_DELTA_PROP       = 'maxValueDelta'

CPU_UTIL_PROP    = 'cpuUtil'
DISK_UTIL_PROP   = 'diskUtil'
MEM_UTIL_PROP    = 'memUtil'

ACTION_ID_PROP             = 'actionID'
DATA_URI_PROP              = 'dataURI'
MESSAGE_PROP               = 'message'
ENCODING_NAME_PROP         = 'encodingName'
RAW_DATA_PROP              = 'rawData'
SEQUENCE_NUMBER_PROP       = 'seqNo'
USE_SEQUENCE_NUMBER_PROP   = 'useSeqNo'
SEQUENCE_NUMBER_TOTAL_PROP = 'seqNoTotal'

SEND_RESOURCE_NAME_PROP    = 'sendResourceName'
RECEIVE_RESOURCE_NAME_PROP = 'receiveResourceName'
IS_PING_PROP               = 'isPing'

MESSAGE_DATA_PROP          = 'msgData'

HOST_NAME_PROP             = 'hostName'
MESSAGE_IN_COUNT_PROP      = 'msgInCount'
MESSAGE_OUT_COUNT_PROP     = 'msgOutCount'
IS_CONNECTING_PROP         = 'isConnecting'
IS_CONNECTED_PROP          = 'isConnected'
IS_DISCONNECTED_PROP       = 'isDisconnected'

CMD_DATA_PERSISTENCE_NAME    = 'pdt-cmd-data'
CONN_DATA_PERSISTENCE_NAME   = 'pdt-conn-data'
SENSOR_DATA_PERSISTENCE_NAME = 'pdt-sensor-data'
SYS_DATA_PERSISTENCE_NAME    = 'pdt-sys-data'

#####
# Resource and Topic Names
#

MSG = 'Msg'

ACTUATOR_CMD      = 'ActuatorCmd'
ACTUATOR_RESPONSE = 'ActuatorResponse'
MGMT_STATUS_MSG   = 'MgmtStatusMsg'
MGMT_STATUS_CMD   = 'MgmtStatusCmd'
MEDIA_MSG         = 'MediaMsg'
SENSOR_MSG        = 'SensorMsg'
SYSTEM_PERF_MSG   = 'SystemPerfMsg'

UPDATE_NOTIFICATIONS_MSG      = 'UpdateMsg'
RESOURCE_REGISTRATION_REQUEST = 'ResourceRegRequest'

LED_ACTUATOR_NAME        = 'Lighting'
HUMIDIFIER_ACTUATOR_NAME = 'Humidifier'
HVAC_ACTUATOR_NAME       = 'HVAC'
#HVAC_ACTUATOR_NAME       = 'Thermostat'

SETTINGS_SECTION_NAME = 'Settings'

HUMIDITY_SENSOR_NAME = 'Humidifier'
PRESSURE_SENSOR_NAME = 'BarometricPressure'
#PRESSURE_SENSOR_NAME = 'Barometer'
TEMP_SENSOR_NAME     = 'Temperature'
#TEMP_SENSOR_NAME     = 'Thermostat'
BAROMETER_NAME       = 'Barometer'
THERMOSTAT_NAME      = 'Thermostat'
HYGROMETER_NAME      = 'Hygrometer'
HVAC_NAME            = 'HVAC'
WIND_TURBINE_NAME    = 'WindTurbine'
SYSTEM_MGMT_NAME     = 'EdgeComputingDevice'
SYSTEM_PERF_NAME     = 'EdgeComputingDevice'
CAMERA_SENSOR_NAME   = 'Camera'

POWER_OUTPUT_NAME     = 'PowerOutput'
ROTATIONAL_SPEED_NAME = 'RotationalSpeed'
WIND_SPEED_NAME       = 'WindSpeed'
BRAKE_SYSTEM_NAME     = 'BrakeSystem'

COMMAND_ON  = 1
COMMAND_OFF = 2
COMMAND_UPDATE = 3
COMMAND_MSG_ONLY = 5

DEFAULT_TYPE_ID           =    0
DEFAULT_TYPE_CATEGORY_ID  =    0
DEFAULT_ACTUATOR_TYPE     = DEFAULT_TYPE_ID
DEFAULT_SENSOR_TYPE       = DEFAULT_TYPE_ID

ENV_TYPE_CATEGORY         = 1000
ENV_DEVICE_TYPE           = ENV_TYPE_CATEGORY
HVAC_ACTUATOR_TYPE        = 1001
HUMIDIFIER_ACTUATOR_TYPE  = 1002
HUMIDIFIER_TYPE           = HUMIDIFIER_ACTUATOR_TYPE
BAROMETER_TYPE            = 1003
THERMOSTAT_TYPE           = 1004

HUMIDITY_SENSOR_TYPE      = 1010
PRESSURE_SENSOR_TYPE      = 1012
TEMP_SENSOR_TYPE          = 1013

DISPLAY_CATEGORY_TYPE     = 2000
DISPLAY_DEVICE_TYPE       = DISPLAY_CATEGORY_TYPE
LED_DISPLAY_ACTUATOR_TYPE = 2001

CAMERA_SENSOR_NAME        = 'CameraSensor'
MEDIA_TYPE_NAME           = 'MediaType'
MEDIA_TYPE_CATEGORY       = 3000
DEFAULT_MEDIA_TYPE        = 3000
MEDIA_DEVICE_TYPE         = 3000
CAMERA_SENSOR_TYPE        = 3101
CAMERA_MOTION_SENSOR_TYPE = 3102
CAMERA_STREAM_SENSOR_TYPE = 3104
VIDEO_SYSTEM_TYPE         = 3201
AUDIO_SYSTEM_TYPE         = 3301
LIGHTING_SYSTEM_TYPE      = 3401

UTILITY_SYSTEM_TYPE_CATEGORY = 4000
UTILITY_SYSTEM_DEVICE_TYPE = UTILITY_SYSTEM_TYPE_CATEGORY

HEATING_SYSTEM_TYPE          = 4100
FLUID_VISCOSITY_SENSOR_TYPE  = 4101
FLUID_RATE_SENSOR_TYPE       = 4102
FLUID_PUMP_TYPE              = 4103
IMPELLER_RPM_SENSOR_TYPE     = 4105
IMPELLER_RPM_ACTUATOR_TYPE   = 4107

ELECTRICAL_SYSTEM_TYPE     = 4200
POWER_OUTPUT_SENSOR_TYPE   = 4201

WIND_TURBINE_POWER_OUTPUT_SENSOR_TYPE     = 4301
WIND_TURBINE_GENERATOR_TEMP_SENSOR_TYPE   = 4302
WIND_TURBINE_ROTATIONAL_SPEED_SENSOR_TYPE = 4303
WIND_TURBINE_AIR_SPEED_SENSOR_TYPE        = 4304

WIND_TURBINE_BRAKE_SYSTEM_ACTUATOR_TYPE   = 4320

ENERGY_TYPE_CATEGORY = 5000
STORAGE_LEVEL = 5001
STORAGE_DRAW = 5002

NATURAL_RESOURCE_ENERGY_SYSTEM_TYPE = 5100
WIND_SYSTEM_TYPE = 5101
WIND_TURBINE_SYSTEM_TYPE = WIND_SYSTEM_TYPE
SOLAR_SYSTEM_TYPE = 5102
HYDRO_SYSTEM_TYPE = 5103
GEOTHERMAL_SYSTEM_TYPE = 5104
OTHER_ENERGY_SYSTEM_TYPE = 5200
HYDROGEN_SYSTEM_TYPE = 5201
FOSSIL_FUEL_ENERGY_SYSTEM_TYPE = 5900
OIL_SYSTEM_TYPE = 5901
NATGAS_SYSTEM_TYPE = 5902
PROPANE_SYSTEM_TYPE = 5903
GASOLINE_SYSTEM_TYPE = 5904

ENABLE_PRODUCTION_NAME = 'enableProduction'
POWER_DRAW_NAME = 'powerDraw'
AMBIENT_TEMPERATURE_NAME = 'ambientTemperature'
ITEMS_PRODUCED_NAME = 'itemsProduced'
FACTORY_WORKCELL_TYPE_CATEGORY = 6300
FACTORY_WORKCELL_GENERIC_TYPE = FACTORY_WORKCELL_TYPE_CATEGORY
FACTORY_WORKCELL_POWER_DRAW_TYPE = 6301
FACTORY_WORKCELL_AMBIENT_TEMP_TYPE = 6302
FACTORY_WORKCELL_ITEMS_PRODUCED_TYPE = 6310

FACTORY_WORKCELL_ENABLE_PRODUCTION_ACTUATOR_TYPE = 6320

STRUCTURE_TYPE_CATEGORY = 7200
STRUCTURE_TYPE = 7201
STRUCTURE_LEVEL_TYPE = 7202
STRUCTURE_SPACE_TYPE = 7203

SYSTEM_MGMT_TYPE          = 8000
SYSTEM_MGMT_TYPE_CATEGORY = 8000
RESOURCE_MGMT_TYPE        = 8001
SYSTEM_CONN_STATE_TYPE    = 8002

RESOURCE_MGMT_NAME        = 'ResourceMgmt'

SYSTEM_PERF_TYPE          = 9000
SYSTEM_PERF_TYPE_CATEGORY = 9000
CPU_UTIL_TYPE             = 9001
DISK_UTIL_TYPE            = 9002
MEM_UTIL_TYPE             = 9003

MESSAGE_TYPE_CATEGORY = 10000
MESSAGE_TYPE          = 10001

CPU_UTIL_NAME  = 'DeviceCpuUtil'
DISK_UTIL_NAME = 'DeviceDiskUtil'
MEM_UTIL_NAME  = 'DeviceMemUtil'

#####
# typical topic naming conventions
#

# for CDA to GDA communications
# e.g., PIOT/ConstrainedDevice/ActuatorCmd
# e.g., PIOT/ConstrainedDevice/SensorMsg

SYSTEM_REQUEST_RESOURCE = PRODUCT_NAME + '/' + SYSTEM_MGMT_NAME

CDA_UPDATE_NOTIFICATIONS_MSG_RESOURCE = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + UPDATE_NOTIFICATIONS_MSG
CDA_ACTUATOR_CMD_MSG_RESOURCE         = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + ACTUATOR_CMD
CDA_ACTUATOR_RESPONSE_MSG_RESOURCE    = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + ACTUATOR_RESPONSE
CDA_MGMT_STATUS_MSG_RESOURCE          = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + MGMT_STATUS_MSG
CDA_MGMT_CMD_MSG_RESOURCE             = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + MGMT_STATUS_CMD
CDA_MEDIA_DATA_MSG_RESOURCE           = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + MEDIA_MSG
CDA_REGISTRATION_REQUEST_RESOURCE     = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + RESOURCE_REGISTRATION_REQUEST
CDA_SENSOR_DATA_MSG_RESOURCE          = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + SENSOR_MSG
CDA_SYSTEM_PERF_MSG_RESOURCE          = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + SYSTEM_PERF_MSG

#####
# Configuration Sections, Keys and Defaults
#

# NOTE: You may need to update these paths if you change
# the directory structure for python-components

CONFIG_FILE = 'PdtConfig.props'
CRED_FILE = 'PdtCred.props'
DEFAULT_CONFIG_FILE_NAME = './config/' + CONFIG_FILE
DEFAULT_CRED_FILE_NAME = './cred/' + CRED_FILE

TEST_GDA_DATA_PATH_KEY = 'testGdaDataPath'
TEST_CDA_DATA_PATH_KEY = 'testCdaDataPath'

LOCAL   = 'Local'
DATA    = 'Data'
MQTT    = 'Mqtt'
COAP    = 'Coap'
OPCUA   = 'Opcua'
SMTP    = 'Smtp'

CLOUD_GATEWAY_SERVICE = CLOUD   + '.' + GATEWAY_SERVICE
COAP_GATEWAY_SERVICE  = COAP    + '.' + GATEWAY_SERVICE
DATA_GATEWAY_SERVICE  = DATA    + '.' + GATEWAY_SERVICE
MQTT_GATEWAY_SERVICE  = MQTT    + '.' + GATEWAY_SERVICE
OPCUA_GATEWAY_SERVICE = OPCUA   + '.' + GATEWAY_SERVICE
SMTP_GATEWAY_SERVICE  = SMTP    + '.' + GATEWAY_SERVICE

SETTINGS_KEY = 'Settings'
TESTING_SETTINGS_KEY          = SETTINGS_KEY + '.' + 'Testing'
SYSTEM_PERF_SETTINGS_KEY      = SETTINGS_KEY + '.' + 'SystemPerformance'
ENVIRONMENTAL_SETTINGS_KEY    = SETTINGS_KEY + '.' + 'Environmental'
WIND_TURBINE_SETTINGS_KEY     = SETTINGS_KEY + '.' + 'WindTurbine'
FACTORY_WORKCELL_SETTINGS_KEY = SETTINGS_KEY + '.' + 'FactoryWorkcell'

DEVICE_ID_KEY          = 'deviceID'
DEVICE_LOCATION_ID_KEY = 'deviceLocationID'

CRED_SECTION = 'Credentials'

FROM_ADDRESS_KEY     = 'fromAddr'
TO_ADDRESS_KEY       = 'toAddr'
TO_MEDIA_ADDRESS_KEY = 'toMediaAddr'
TO_TXT_ADDRESS_KEY   = 'toTxtAddr'

HOST_KEY             = 'host'
PORT_KEY             = 'port'
SECURE_PORT_KEY      = 'securePort'

ROOT_CERT_ALIAS = 'root'

KEY_STORE_CLIENT_IDENTITY_KEY = 'keyStoreClientIdentity'
KEY_STORE_SERVER_IDENTITY_KEY = 'keyStoreServerIdentity'

KEY_STORE_FILE_KEY    = 'keyStoreFile'
KEY_STORE_AUTH_KEY    = 'keyStoreAuth'
TRUST_STORE_FILE_KEY  = 'trustStoreFile'
TRUST_STORE_ALIAS_KEY = 'trustStoreAlias'
TRUST_STORE_AUTH_KEY  = 'trustStoreAuth'
USER_NAME_TOKEN_KEY   = 'userToken'
USER_AUTH_TOKEN_KEY   = 'authToken'
API_TOKEN_KEY         = 'apiToken'
ORG_TOKEN_KEY         = 'orgToken'

CERT_FILE_KEY        = 'certFile'
CRED_FILE_KEY        = 'credFile'
ENABLE_AUTH_KEY      = 'enableAuth'
ENABLE_CRYPT_KEY     = 'enableCrypt'
ENABLE_SIMULATOR_KEY = 'enableSimulator'
ENABLE_EMULATOR_KEY  = 'enableEmulator'
ENABLE_SENSE_HAT_KEY = 'enableSenseHAT'
ENABLE_LOGGING_KEY   = 'enableLogging'
ENABLE_MSG_QUEUE_KEY = 'enableMsgQueue'
ENABLE_OPERATION_KEY = 'enableOperation'
ENABLE_DATA_GENERATION_KEY = 'enableDataGeneration'
ENABLE_SIM_ENGINE_UPDATES = 'enableSimEngineUpdates'
USE_WEB_ACCESS_KEY   = 'useWebAccess'
POLL_CYCLES_KEY      = 'pollCycleSecs'
KEEP_ALIVE_KEY       = 'keepAlive'
DEFAULT_QOS_KEY      = 'defaultQos'

ENABLE_TSDB_CLIENT_KEY = 'enableTsdbClient'
ENABLE_MQTT_CLIENT_KEY = 'enableMqttClient'
ENABLE_COAP_CLIENT_KEY = 'enableCoapClient'
ENABLE_COAP_SERVER_KEY = 'enableCoapServer'

ENABLE_ROBOTIC_MANIPULATOR_KEY = 'enableRoboticManipulator'
ENABLE_CONVEYOR_KEY = 'enableConveyor'
ENABLE_HOPPER_KEY = 'enableHopper'
ENABLE_PALLET_LOADING_KEY = 'enablePalletLoading'

ENABLE_POWER_GENERATION_KEY = 'enablePowerGeneration'
ENABLE_SYSTEM_PERF_KEY  = 'enableSystemPerformance'
ENABLE_ACTUATION_KEY    = 'enableActuation'
ENABLE_SENSING_KEY      = 'enableSensing'
ENABLE_COMMAND_NAME_KEY = 'enableCommandName'

SEND_EVENT_DISPLAY_UPDATES_KEY = 'sendEventDisplayUpdates'
UPDATE_DISPLAY_ON_ACTUATION_KEY = 'updateDisplayOnActuation'

MIN_WIND_SPEED_KEY       = 'minWindSpeed'
MAX_WIND_SPEED_KEY       = 'maxWindSpeed'

HUMIDITY_SIM_FLOOR_KEY   = 'humiditySimFloor'
HUMIDITY_SIM_CEILING_KEY = 'humiditySimCeiling'
PRESSURE_SIM_FLOOR_KEY   = 'pressureSimFloor'
PRESSURE_SIM_CEILING_KEY = 'pressureSimCeiling'
TEMP_SIM_FLOOR_KEY       = 'tempSimFloor'
TEMP_SIM_CEILING_KEY     = 'tempSimCeiling'

HANDLE_TEMP_CHANGE_ON_DEVICE_KEY = 'handleTempChangeOnDevice'
TRIGGER_HVAC_TEMP_FLOOR_KEY      = 'triggerHvacTempFloor'
TRIGGER_HVAC_TEMP_CEILING_KEY    = 'triggerHvacTempCeiling'

MIN_PRODUCTION_RATE_KEY = 'minProductionRate'
MAX_PRODUCTION_RATE_KEY = 'maxProductionRate'
DEFAULT_PRODUCTION_RATE_KEY = 'defaultProductionRate'

RUN_FOREVER_KEY    = 'runForever'
TEST_EMPTY_APP_KEY = 'testEmptyApp'

STREAM_HOST_ADDR_KEY       = 'streamHostAddr'
STREAM_HOST_LABEL_KEY      = 'streamHostLabel'
STREAM_PORT_KEY            = 'streamPort'
STREAM_PROTOCOL_KEY        = 'streamProtocol'
STREAM_PATH_KEY            = 'streamPath'
STREAM_ENCODING_KEY        = 'streamEncoding'
STREAM_FRAME_WIDTH_KEY     = 'streamFrameWidth'
STREAM_FRAME_HEIGHT_KEY    = 'streamFrameHeight'
STREAM_FPS_KEY             = 'streamFps'
IMAGE_FILE_EXT_KEY         = 'imageFileExt'
VIDEO_FILE_EXT_KEY         = 'videoFileExt'
MIN_MOTION_PIXELS_DIFF_KEY = 'minMotionPixelsDiff'

IMAGE_ENCODING_KEY         = 'imageEncoding'
IMAGE_DATA_STORE_PATH      = 'imageDataStorePath'
VIDEO_DATA_STORE_PATH      = 'videoDataStorePath'
MIN_MOTION_PIXELS_DIFF_KEY = 'minMotionPixelsDiff'
MAX_MOTION_FRAMES_BEFORE_ACTION_KEY = 'maxMotionFramesBeforeAction'
MAX_CACHED_FRAMES_KEY      = 'maxCachedFrames'
STORE_INTERIM_FRAMES_KEY   = 'storeInterimFrames'
INCLUDE_RAW_IMAGE_DATA_IN_MSG_KEY = 'includeRawImageDataInMsg'
