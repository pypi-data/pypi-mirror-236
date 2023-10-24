import calculator_179d.calculate_common_features as ccf
import numpy as np
import pickle
import pkg_resources

class baseline_electricity_179d():
    def __init__(self, calculator_user_inputs):
        self.bldg_type = calculator_user_inputs['building_type']
        self.climate_zone = calculator_user_inputs['climate_zone']
        self.hvac_system = calculator_user_inputs['hvac_system']
        self.baseline_electricity_model = self.read_proposed_model()


    # pick the sklearn model based on bldg type, climate zone and hvac_system
    def read_proposed_model(self):
        model_file = (
            'baseline_electricity_' +
            self.bldg_type + '_' +
            self.climate_zone + '_' +
            self.hvac_system +
            '.pk'
        )
        model_path = pkg_resources.resource_filename(__name__, f"model_files/{model_file}")

        with open(model_path,'rb') as f:
            model = pickle.load(f)

        return model


    # create input array used for model prediction
    def create_input_array(self, calculator_user_inputs):
        # calculated features - ua building, ACH infiltration, surface to volume ratio
        ua_bldg = ccf.calculate_ua_bldg(calculator_user_inputs)
        ach_infiltration = ccf.calculate_ACH_infiltration(calculator_user_inputs)
        sa_to_vol_ratio = ccf.calculate_sa_to_vol_ratio(calculator_user_inputs)

        # create input array - same order as used during model development
        input_array = np.array(
            [[
                calculator_user_inputs['number_of_floors'],
                calculator_user_inputs['gross_floor_area'],
                calculator_user_inputs['window_wall_ratio'],
                calculator_user_inputs['window_shgc'],
                ach_infiltration,
                calculator_user_inputs['proposed_lpd'],
                calculator_user_inputs['dx_cooling_cop'],
                ua_bldg,
                sa_to_vol_ratio,
            ]]
        )

        return input_array


    # Predict annual electricity 179d
    def estimate_annual_electricity(self, calculator_user_inputs):
        #create input array for prediction
        input_array = self.create_input_array(calculator_user_inputs)
        # predict floor area normalized annualy electricity 179d
        baseline_electricity_179d_normalized = self.baseline_electricity_model.predict(
            input_array
        )
        baseline_electricity_179d_value = (
            baseline_electricity_179d_normalized*
            calculator_user_inputs['gross_floor_area']
        )[0]

        return baseline_electricity_179d_value