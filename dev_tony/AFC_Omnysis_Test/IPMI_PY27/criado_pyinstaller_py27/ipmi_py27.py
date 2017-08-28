from __future__ import print_function
import pyipmi.interfaces


interface = pyipmi.interfaces.create_interface('ipmitool', interface_type='lan')
connection = pyipmi.create_connection(interface)
connection.target = pyipmi.Target(0x82)
connection.session.set_session_type_rmcp('10.0.18.14', port=623)
connection.session.set_auth_type_user('', '')
connection.session.establish()



def sdr_show_amc_current(ipmi, s):
    if s.type is pyipmi.sdr.SDR_TYPE_FULL_SENSOR_RECORD:
        (raw, states) = ipmi.get_sensor_reading(s.number, s.owner_lun)
        value = s.convert_sensor_raw_to_value(raw)
        if value is None:
            value = "na"
        print("Reading Type: ",s.device_id_string)
	print("Reading Value: ",value)
	print("Reading Units: ","A")

def sdr_show_fmcvadj_voltage(ipmi, s):
    if s.type is pyipmi.sdr.SDR_TYPE_FULL_SENSOR_RECORD:
        (raw, states) = ipmi.get_sensor_reading(s.number, s.owner_lun)
        value = s.convert_sensor_raw_to_value(raw)
        if value is None:
            value = "na"
        print("Reading Type: ",s.device_id_string)
	print("Reading Value: ",value)
	print("Reading Units: ","V")

def sdr_show_sensors_tempfpga(ipmi, s):
    if s.type is pyipmi.sdr.SDR_TYPE_FULL_SENSOR_RECORD:
        (raw, states) = ipmi.get_sensor_reading(s.number, s.owner_lun)
        value = s.convert_sensor_raw_to_value(raw)
        if value is None:
            value = "na"
        print("Reading Type: ",s.device_id_string)
	print("Reading Value: ",value)
	print("Reading Units: ","C")

def sdr_show_sensors_dont_know(ipmi, s):
    if s.type is pyipmi.sdr.SDR_TYPE_FULL_SENSOR_RECORD:
        (raw, states) = ipmi.get_sensor_reading(s.number, s.owner_lun)
        value = s.convert_sensor_raw_to_value(raw)
        if value is None:
            value = "na"
        print("Reading Type: ",s.device_id_string)
	print("Reading Value: ",value)
	print("Reading Units: ","NoUnits")


def tests(ipmi):
    for y in range(4, 8):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_sensors_tempfpga(connection, s)
        print("\n")
    for y in range(8, 10):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_fmcvadj_voltage(connection, s)
        print("\n")
    for y in range(11, 17):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_sensors_tempfpga(connection, s)
        print("\n")
    for y in range(17, 22):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_fmcvadj_voltage(connection, s)
        print("\n")
    y=67
    s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
    sdr_show_sensors_dont_know(connection, s)
    print("\n")
    for y in range(69, 74):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_sensors_tempfpga(connection, s)
        print("\n")
    y=74
    s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
    sdr_show_fmcvadj_voltage(connection, s)
    print("\n")
    for y in range(75, 91):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_amc_current(connection, s)
        print("\n")        
    for y in range(95, 102):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_sensors_tempfpga(connection, s)
        print("\n") 
    for y in range(102, 108):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_fmcvadj_voltage(connection, s)
        print("\n") 
    for y in range(110, 112):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_sensors_tempfpga(connection, s)
        print("\n") 
    for y in range(114, 120):
        s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
        sdr_show_fmcvadj_voltage(connection, s)
        print("\n") 
    y=120
    s = pyipmi.sensor.Sensor.get_device_sdr(connection,y)
    sdr_show_amc_current(connection, s)
    print("\n")


out = tests(connection)


