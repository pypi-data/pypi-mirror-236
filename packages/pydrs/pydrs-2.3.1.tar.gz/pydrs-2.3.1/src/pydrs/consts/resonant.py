# SWLS Resonant Converter
list_soft_interlocks = [
    "DCCT 1 Fault",
    "DCCT 2 Fault",
    "DCCT High Difference",
]

list_hard_interlocks = [
    "Load Overcurrent",
    "DCLink Overvoltage",
    "DCLink Undervoltage",
    "Welded Contactor Fault",
    "Opened Contactor Fault",
    "External Interlock",
    "IIB Interlock"
]

list_iib_interlocks = [
    "Input Overvoltage",
    "Output Overvoltage",
    "Input Overcurrent",
    "Output Overcurrent",
    "Input Inductor Overtemperature",
    "Output Inductor Overtemperature",
    "MOSFETs Heat-Sink Overtemperature",
    "Diodes Heat-Sink Overtemperature",
    "Drivers Overvoltage",
    "Drivers Overcurrent",
    "High Leakage Current",
    "Board IIB Overtemperature",
    "Module Overhumidity",
    "Contact Sticking of Contactor",
    "Emergency Button",
]

list_iib_alarms = [
    "Input Overvoltage",
    "Output Overvoltage",
    "Input Overcurrent",
    "Output Overcurrent",
    "Input Inductor Overtemperature",
    "Output Inductor Overtemperature",
    "MOSFETs Heat-Sink Overtemperature",
    "Diodes Heat-Sink Overtemperature",
    "Drivers Overvoltage",
    "Drivers Overcurrent",
    "High Leakage Current",
    "Board IIB Overtemperature",
    "Module Overhumidity",
]

bsmp = {
    "ps_alarms": {"addr": 33, "format": "I", "size": 4, "egu": ""},
    "i_load_mean": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "i_load_1": {"addr": 35, "format": "f", "size": 4, "egu": "A"},
    "i_load_2": {"addr": 36, "format": "f", "size": 4, "egu": "A"},
    "i_load_error": {"addr": 37, "format": "f", "size": 4, "egu": "A"},
    "freq_modulated": {"addr": 38, "format": "f", "size": 4, "egu": "Hz"},
    "v_input_iib": {"addr": 39, "format": "f", "size": 4, "egu": "V"},
    "v_output_iib": {"addr": 40, "format": "f", "size": 4, "egu": "V"},
    "i_input_iib": {"addr": 41, "format": "f", "size": 4, "egu": "A"},
    "i_output_iib": {"addr": 42, "format": "f", "size": 4, "egu": "A"},
    "temp_input_inductor_iib": {"addr": 43, "format": "f", "size": 4, "egu": "°C"},
    "temp_output_inductor_iib": {"addr": 44, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_mosfet_iib": {"addr": 45, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_diodes_iib": {"addr": 46, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_iib": {"addr": 47, "format": "f", "size": 4, "egu": "V"},
    "i_driver_iib": {"addr": 48, "format": "f", "size": 4, "egu": "A"},
    "i_leakage_iib": {"addr": 49, "format": "f", "size": 4, "egu": "A"},
    "temp_board_iib": {"addr": 50, "format": "f", "size": 4, "egu": "°C"},
    "rh_iib": {"addr": 51, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks": {"addr": 52, "format": "I", "size": 4, "egu": ""},
    "iib_alarms": {"addr": 53, "format": "I", "size": 4, "egu": ""},
}