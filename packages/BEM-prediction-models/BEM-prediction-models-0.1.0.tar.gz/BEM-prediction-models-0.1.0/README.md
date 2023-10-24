# BEM Prediction Models

## Setup Instructions

Run `pip install -r requirements.txt` to install python packages.

Developed using Python version 3.9.7.

## Using this code as a library
After running the setup instructions, import the package into your code and call the
`calculate_savings(property_info)` function to calculate the savings for that property.

#### Parameters
`property_info` - a dictionary with the following required entries:
```
	building_type
	climate_zone
	hvac_system
	gross_floor_area
	number_of_floors
	aspect_ratio
	window_wall_ratio
	roof_thermal_perf_type
	wall_thermal_perf_type
	window_u_factor
	window_shgc
	proposed_lpd
	water_heating_energy_factor
	air_system_fan_total_efficiency
	boiler_average_efficiency
	dx_cooling_cop
	zone_hvac_fan_total_efficiency
	dx_heating_cop
	gas_coil_average_efficiency
	chiller_average_cop
```

#### Driver program
The following is a test program you can use to check if you have correctly installed the library

```
from calculator_179d.main_calculator import calculate_savings

inputs = {
	"building_type": "small office",
	"climate_zone": "4A",
	"hvac_system":"PSZ-AC with gas coil",
	"gross_floor_area": 11250,
	"number_of_floors": 1,
	"aspect_ratio": 2.959,
	"window_wall_ratio": 0.13,
	"roof_thermal_perf_type": 0.209,
	"wall_thermal_perf_type": 0.265,
	"window_u_factor": 2.956,
	"window_shgc": 0.351,
	"proposed_lpd": 5.705,
	"water_heating_energy_factor": 0.705,
	"air_system_fan_total_efficiency": 0.95,
	"boiler_average_efficiency": 0,
	"dx_cooling_cop": 3.799,
	"zone_hvac_fan_total_efficiency": 0,
	"dx_heating_cop": 0,
	"gas_coil_average_efficiency": 0,
	"chiller_average_cop": 0
}

print("These are the savings:")
print(calculate_savings(inputs))
```


## Running the package as a standalone application
You may run this package as a standalone application instead of importing it as a library. To do so,
simply update the parameters in `calculator_179d/calculator_user_inputs.json` and execute the code using the
following command:

```
    cd calculator_179d/
    python3 main_calculator.py calculator_user_inputs.json
```

This will create an file at `calculator_179d/output_files/calculator_outputs.json` with the results from the models.
