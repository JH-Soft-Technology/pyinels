"""Const of iNels BUS tests."""
TEST_HOST = "http://localhost"

TEST_INELS_NAMESPACE = "inels.cu3"
TEST_INELS_BUS3_NAMESPACE = "inels.cu3.InelsBus3"

TEST_PORT = "1000"
TEST_RAW_DEVICES = """garage:
name="Doors" column="0" inels="Doors_Garage" read_only="no" row="1"
lights:
name="Main light" column="0" inels="SV_12_Garage" read_only="no" row="0"
name="Wall light" column="1" inels="SV_Wall_Garage" read_only="no" row="0"
"""
TEST_ROOMS = ['Basement', 'First floor', 'Front yard',
              'Back yard', 'Attic', 'Garrage']

TEST_DATA_THERM = {
    'name': 'Valve in bedroom',
    'therm': 'Bedroom_temerature',
    'rele': 'DIGITALGROUP_0001',
    'read_only': 'no',
    'stateth': 'Bedroom_stateth'
}

TEST_DATA_LIGHT = {
    'name': 'Kitchen main light',
    'id': 'KITCHEN_MAIN_LIGHT',
    'read_only': 'no'
}

TEST_DATA_SWITCH = {
    'name': 'Kitchen kettel switch',
    'id': 'KITCHEN_KETTLE_SWITCH',
    'read_only': 'no'
}

TEST_DATA_SHUTTER = {
    'name': 'Kitchen shuuter',
    'up': 'KITCHEN_SHUUTER_1_UP',
    'down': 'KITCHEN_SHUUTER_1_DOWN',
    'read_only': 'no'
}

TEST_DATA_GARAGE = {
    'name': 'Garage door',
    'id': 'GARAGE_DOOR',
    'read_only': 'no'
}

TEST_DATA_HEATING = {
    'name': 'Holiday',
    'id': 'HOLIDAY_HEATING',
    'read_only': 'no'
}
