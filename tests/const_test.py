"""Const of iNels BUS tests."""
TEST_API_NAMESPACE = "pyinels.api"
TEST_API_CLASS_NAMESPACE = "pyinels.api.Api"

TEST_DATA_THERM = {
    'title': 'Valve in bedroom',
    'temp': 'Bedroom_temerature',
    'rele': 'DIGITALGROUP_0001',
    'read_only': 'no',
    'temp_set': 'Bedroom_stateth'
}

TEST_DATA_LIGHT = {
    'title': 'Kitchen main light',
    'id': 'KITCHEN_MAIN_LIGHT',
    'read_only': 'no'
}

TEST_DATA_SWITCH = {
    'title': 'Kitchen kettel switch',
    'id': 'KITCHEN_KETTLE_SWITCH',
    'read_only': 'no'
}

TEST_DATA_SHUTTER = {
    'title': 'Kitchen shuuter',
    'up': 'KITCHEN_SHUUTER_1_UP',
    'down': 'KITCHEN_SHUUTER_1_DOWN',
    'read_only': 'no'
}

TEST_DATA_GARAGE = {
    'title': 'Garage door',
    'id': 'GARAGE_DOOR',
    'read_only': 'no'
}

TEST_DATA_HEATING = {
    'title': 'Holiday',
    'id': 'HOLIDAY_HEATING',
    'read_only': 'no'
}

TEST_HOST = "http://localhost"

TEST_INELS_DEVICE_NAMESPACE = "pyinels.device.Device"

TEST_PORT = "1000"

TEST_RESOURCE_SWITCH = {
    'column': '0',
    'group': 'basement',
    'inels': 'ZA_14_basement',
    'name': 'Office switch',
    'read_only': 'no',
    'row': '1',
    'type': 'switch'
}

TEST_RAW_DEVICES = """garage:
name="Doors" column="0" inels="Doors_Garage" read_only="no" row="1"
lights:
name="Main light" column="0" inels="SV_12_Garage" read_only="no" row="0"
name="Wall light" column="1" inels="SV_Wall_Garage" read_only="no" row="0"
on_off:
name="Main switch" column="2" inels="ZA_01_GARAGE" read_only="no" row="0"
"""
TEST_ROOMS = ['Basement', 'First floor', 'Front yard',
              'Back yard', 'Attic', 'Garrage']

TEST_VERSION = "CU3"
