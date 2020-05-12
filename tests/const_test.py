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

TEST_RAW_DUPLICIT_DEVICES = """on_off:
name="Zas OB" column="0" inels="ZAS_1A_Obyvak" read_only="no" row="2"
name="Zas POK" column="1" inels="ZAS_1B_Pokoj_dole" read_only="no" row="2"
name="Zas POK" column="1" inels="ZAS_1B_Pokoj_dole" read_only="no" row="2"
thermals:
name="Obyvak" inels="Koupelna_dole_StateTH" placement="indoor"
heating:
name="DOVOLENA" column="0" inels="DIGITALGROUP_0001" read_only="no" row="5"
lights:
name="Obyvak" column="0" inels="SV_1_Obyvak_strop" read_only="no" row="0"
name="Stul" column="1" inels="SV_2_Jidelni_stul" read_only="no" row="0"
name="Kuchyn" column="2" inels="SV_3_Kuchyn" read_only="no" row="0"
name="Linka" column="3" inels="SV_4_Kuchyn_linka" read_only="no" row="0"
name="Schody" column="0" inels="SV_15_Schodiste" read_only="no" row="1"
name="Vstup" column="1" inels="SV_10_Chodba_dole" read_only="no" row="1"
name="Pokoj" column="2" inels="SV_7_Pokoj_dole" read_only="no" row="1"
name="Koupelna" column="3" inels="SV_9_Koupelna_dole" read_only="no" row="1"
name="Technicka" column="4" inels="SV_11_Technicka_1." read_only="no" row="1"
name="Pod schody" column="5" inels="SV_14_Kumbal_rozvc" read_only="no" row="1"
shutters:
name="Zal OB" column="0" down="Z_Obk_do" read_only="no" up="ZAL__ahor" row="3"
name="Rol KRB" column="1" down="ROL_Jillu" read_only="no" up="ROJidru" row="3"
name="Rol KUCH" column="2" down="RL_Kc_do" read_only="no" up="ROuchyu" row="3"
name="Rol POK" column="3" down="R_Po_dou" read_only="no" up="ROnahoru" row="3"
heat-control:
name="Obyvak" read_only="no" therm="O" column="0" stateth="O" rele="D" row="4"
name="Pokoj" read_only="no" therm="P" column="1" stateth="P" rele="D" row="4"
name="Koupel" read_only="no" therm="K" column="2" stateth="K" rele="D" row="4"
name="Zadveri" read_only="no" therm="V" column="3" stateth="V" rele="D" row="4"
name="Obyvak" read_only="no" therm="O" column="0" stateth="O" rele="D" row="4"
name="Pokoj" read_only="no" therm="P" column="1" stateth="P" rele="D" row="4"
name="Koupel" read_only="no" therm="K" column="2" stateth="K" rele="D" row="4"
name="Zadveri" read_only="no" therm="V" column="3" stateth="V" rele="D" row="4"
"""

TEST_ROOMS = ['Basement', 'First floor', 'Front yard',
              'Back yard', 'Attic', 'Garrage']

TEST_VERSION = "CU3"
