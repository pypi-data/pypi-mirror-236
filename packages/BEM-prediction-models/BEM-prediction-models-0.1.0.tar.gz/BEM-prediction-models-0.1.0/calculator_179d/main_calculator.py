import calculator_179d.proposed_electricity_179d as pe179d
import calculator_179d.baseline_electricity_179d as be179d
import calculator_179d.proposed_naturalgas_179d as pn179d
import calculator_179d.baseline_naturalgas_179d as bn179d
import numpy as np
import sys
import json
import pkg_resources
import os

def calculate_model_outputs(property_info):
    ## proposed and baseline electricity 179d

    # create proposed model object based on bulding type, climate zone, and system type
    proposed_electricity_179d_obj = pe179d.proposed_electricity_179d(property_info)
    # estimate annual electricity using proposed model, and user calculator inputs
    proposed_electricity_179d_value = proposed_electricity_179d_obj.estimate_annual_electricity(
        property_info
    )
    # create baseline model object based on bulding type, climate zone, and system type
    baseline_electricity_179d_obj = be179d.baseline_electricity_179d(property_info)
    # estimate baseline annual electricity withe baseline model and user calculator inputs
    baseline_electricity_179d_value = baseline_electricity_179d_obj.estimate_annual_electricity(
        property_info
    )

    # create proposed model object based on bulding type, climate zone, and system type
    proposed_naturalgas_179d_obj = pn179d.proposed_naturalgas_179d(property_info)
    # estimate annual electricity using proposed model, and user calculator inputs
    proposed_naturalgas_179d_value = proposed_naturalgas_179d_obj.estimate_annual_naturalgas(
        property_info
    )
    # create baseline model object based on bulding type, climate zone, and system type
    baseline_naturalgas_179d_obj = bn179d.baseline_naturalgas_179d(property_info)
    # estimate baseline annual electricity withe baseline model and user calculator inputs
    baseline_naturalgas_179d_value = baseline_naturalgas_179d_obj.estimate_annual_naturalgas(
        property_info
    )

    model_outputs = [
        proposed_electricity_179d_value,
        baseline_electricity_179d_value,
        proposed_naturalgas_179d_value,
        baseline_naturalgas_179d_value
    ]

    return model_outputs

def calculate_total_cost_and_savings(model_output,cost_file,climate_zone):
    #open json file with cost data
    with open(cost_file,'rb') as f:

        Cost = json.load(f)
        AvgElectricityPrice=Cost[climate_zone]['Electricity']
        AvgNaturalGasPrice=Cost[climate_zone]['NaturalGas']

        #calculate total costs
        baseline_179d_totalcost=(
            AvgElectricityPrice*model_output[1]+
            AvgNaturalGasPrice*model_output[3]
        )
        proposed_179d_totalcost=(
            AvgElectricityPrice*model_output[0]+
            AvgNaturalGasPrice*model_output[2]
        )

        #calculate savings
        Percent_Savings=round(
            (
                (baseline_179d_totalcost-proposed_179d_totalcost)/
                baseline_179d_totalcost
            )*100
        )
        Percent_Savings_Electricity=(
            round(
                ((model_output[1]-model_output[0])/
                model_output[1])*100
            )
        )
        Percent_Savings_Naturalgas=(
            round(
                ((model_output[3]-model_output[2])/
                model_output[3])*100
            )
        )

        #output arrays
        list_total_costs = [
            baseline_179d_totalcost,
            proposed_179d_totalcost
        ]
        list_savings = [
            Percent_Savings,
            Percent_Savings_Electricity,
            Percent_Savings_Naturalgas
        ]

        return[list_total_costs,list_savings]


def calculate_savings(property_info):
    #calculate model outputs
    model_outputs = calculate_model_outputs(property_info)

    #calculate total cost and savings
    climate_zone = property_info['climate_zone']
    cost_file = 'Elec_Gas_AverageCost.json'
    cost_file_path = pkg_resources.resource_filename(__name__, cost_file)

    [list_total_costs,list_savings] = calculate_total_cost_and_savings(
        model_outputs,
        cost_file_path,
        climate_zone
    )

    ## Save outputs in json file
    dict_outputs = {
        'proposed_179d_electricity':model_outputs[0],
        'baseline_179d_electricity':model_outputs[1],
        'proposed_179d_naturalgas':model_outputs[2],
        'baseline179d_natualgas':model_outputs[3],
        'baseline_179d_totalcost':list_total_costs[0],
        'poposed_179d_totalcost':list_total_costs[1],
        'percent_savings':list_savings[0],
        'percent_savings_electricity':list_savings[1],
        'percent_savings_naturalgas':list_savings[2]
    }

    BinSavings=np.arange(25,51, 1).tolist()
    RateList=np.arange(0.5,1.02,0.02).tolist()
    if list_savings[0]>=25:
        Tax_deduction_Rate=RateList[np.digitize(list_savings[0],BinSavings)-1]  # $/sqft
        dict_outputs['tax_deduction_rate'] = Tax_deduction_Rate
    else:
        Tax_deduction_Rate=0
        print("Minimum savings requirement not met and not qualified for 179D tax deduction")
        dict_outputs['tax_deduction_rate'] = Tax_deduction_Rate

    return dict_outputs





if __name__ == "__main__":
    json_file = sys.argv[1:][0]
    #load json file given as argument in command line
    with open(json_file) as f:
        property_info = json.load(f)
        #compute outputs and save in calculator_outputs.json
        output = calculate_savings(property_info)
        with open(r'./output_files/calculator_outputs.json', 'w') as fp:
            json.dump(output, fp)
