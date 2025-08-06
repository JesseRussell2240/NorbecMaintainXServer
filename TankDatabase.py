# database.py

# Simulating a database with tanks, each having pressure, temperature, and level meters
tanks_database = {
    "Iso_1": {
        "name": "Iso Tank 1",  # Tanak name
        "pressure": {
            "meter_id": 287297,
            "tag_name": "PT_ISO_1C_125",
            "max_value": 150,  # Max pressure in PSI
            "min_value": 50    # Min pressure in PSI
        },
        "temperature": {
            "meter_id": 287308,
            "tag_name": "TT_ISO_1C_110",
            "max_value": 200,  # Max temperature in Celsius
            "min_value": 10    # Min temperature in Celsius
        },
        "level": {
            "meter_id": 287322,
            "tag_name": "LS_ISO_1C_130",
            "max_value": 10,  # Max level in meters
            "min_value": 1    # Min level in meters
        }
    },
    "Iso_2": {
        "name": "Iso Tank 2",
        "pressure": {
            "meter_id": 287298,
            "tag_name": "PT_ISO_1C_225",
            "max_value": 180,  # Max pressure
            "min_value": 40    # Min pressure
        },
        "temperature": {
            "meter_id": 287309,
            "tag_name": "TT_ISO_1C_210",
            "max_value": 180,  # Max temperature
            "min_value": 5     # Min temperature
        },
        "level": {
            "meter_id": 287323,
            "tag_name": "LS_ISO_1C_230",
            "max_value": 8,  # Max level
            "min_value": 2   # Min level
        }
    },
        "Iso_3": {
        "name": "Iso Tank 3",
        "pressure": {
            "meter_id": 287299,
            "tag_name": "PT_ISO_1C_325",
            "max_value": 180,  # Max pressure
            "min_value": 40    # Min pressure
        },
        "temperature": {
            "meter_id": 287310,
            "tag_name": "TT_ISO_1C_310",
            "max_value": 180,  # Max temperature
            "min_value": 5     # Min temperature
        },
        "level": {
            "meter_id": 287324,
            "tag_name": "LS_ISO_1C_330",
            "max_value": 8,  # Max level
            "min_value": 2   # Min level
        }
    },
        "Iso_4": {
        "name": "Iso Tank 4",
        "pressure": {
            "meter_id": 287300,
            "tag_name": "PT_ISO_1C_425",
            "max_value": 180,  # Max pressure
            "min_value": 40    # Min pressure
        },
        "temperature": {
            "meter_id": 287311,
            "tag_name": "TT_ISO_1C_410",
            "max_value": 180,  # Max temperature
            "min_value": 5     # Min temperature
        },
        "level": {
            "meter_id": 287325,
            "tag_name": "LS_ISO_1C_430",
            "max_value": 8,  # Max level
            "min_value": 2   # Min level
        }
    },    "Poly_1": {
        "name": "Poly Tank 1",  # Tank name
        "pressure": {
            "meter_id": 287302,
            "tag_name": "PT_POL_4D_125",
            "max_value": 150,  # Max pressure in PSI
            "min_value": 50    # Min pressure in PSI
        },
        "temperature": {
            "meter_id": 287314,
            "tag_name": "TT_POL_4D_110",
            "max_value": 200,  # Max temperature in Celsius
            "min_value": 10    # Min temperature in Celsius
        },
        "level": {
            "meter_id": 287326,
            "tag_name": "LS_POL_4D_130",
            "max_value": 10,  # Max level in meters
            "min_value": 1    # Min level in meters
        }
    },
    "Poly_2": {
        "name": "Poly Tank 2",  # Tank name
        "pressure": {
            "meter_id": 287303,
            "tag_name": "PT_POL_4D_225",
            "max_value": 150,  # Max pressure in PSI
            "min_value": 50    # Min pressure in PSI
        },
        "temperature": {
            "meter_id": 287315,
            "tag_name": "TT_POL_4D_210",
            "max_value": 200,  # Max temperature in Celsius
            "min_value": 10    # Min temperature in Celsius
        },
        "level": {
            "meter_id": 287327,
            "tag_name": "LS_POL_4D_230",
            "max_value": 10,  # Max level in meters
            "min_value": 1    # Min level in meters
        }
    },
        "Poly_3": {
        "name": "Poly Tank 3",  # Tank name
        "pressure": {
            "meter_id": 287304,
            "tag_name": "PT_POL_6D_325",
            "max_value": 150,  # Max pressure in PSI
            "min_value": 50    # Min pressure in PSI
        },
        "temperature": {
            "meter_id": 287317,
            "tag_name": "TT_POL_6D_310",
            "max_value": 200,  # Max temperature in Celsius
            "min_value": 10    # Min temperature in Celsius
        },
        "level": {
            "meter_id": 287328,
            "tag_name": "LS_POL_6D_325",
            "max_value": 10,  # Max level in meters
            "min_value": 1    # Min level in meters
        }
    },
        "Poly_4": {
        "name": "Poly Tank 4",  # Tank name
        "pressure": {
            "meter_id": 287305,
            "tag_name": "PT_POL_6D_425",
            "max_value": 150,  # Max pressure in PSI
            "min_value": 50    # Min pressure in PSI
        },
        "temperature": {
            "meter_id": 287320,
            "tag_name": "TT_POL_6D_410",
            "max_value": 200,  # Max temperature in Celsius
            "min_value": 10    # Min temperature in Celsius
        },
        "level": {
            "meter_id": 287329,
            "tag_name": "LS_POL_6D_430",
            "max_value": 10,  # Max level in meters
            "min_value": 1    # Min level in meters
        }
    },
        "Pentane": {
        "name": "Pentane",  # Tank name
        "pressure": {
            "meter_id": 287307,
            "tag_name": "PT_PNT_9F_105",
            "max_value": 150,  # Max pressure in PSI
            "min_value": 50    # Min pressure in PSI
        },
        "temperature": {
            "meter_id": 287321,
            "tag_name": "TT_PNT_9F_100",
            "max_value": 200,  # Max temperature in Celsius
            "min_value": 10    # Min temperature in Celsius
        },
        "level": {
            "meter_id": 287330,
            "tag_name": "LS_PNT_9F_110",
            "max_value": 10,  # Max level in meters
            "min_value": 1    # Min level in meters
        }
    }
}

# Function to get all tanks from the database
def get_tanks():
    return tanks_database
