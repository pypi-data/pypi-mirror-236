def calculate_ext_wall_surface_area(gross_floor_area):
    ext_wall_surface_area = 1.4*gross_floor_area

    return ext_wall_surface_area


def calculate_roof_area(calculator_user_inputs):
    gross_floor_area = calculator_user_inputs['gross_floor_area']
    n_stories = calculator_user_inputs['number_of_floors']
    roof_area = gross_floor_area/n_stories

    return roof_area


def calculate_ACH_infiltration(calculator_user_inputs):
    bldg_type = calculator_user_inputs['building_type']
    if bldg_type == 'small office':
        ACH_infiltration = 1.072

    return ACH_infiltration


def calculate_ua_bldg(calculator_user_inputs):
    # calculate external wall surface area
    gross_floor_area = calculator_user_inputs['gross_floor_area']
    ext_wall_surface_area = calculate_ext_wall_surface_area(gross_floor_area)

    #calculate roof area
    n_stories = calculator_user_inputs['number_of_floors']
    roof_area = calculate_roof_area(calculator_user_inputs)

    # calculate window area
    window_area = ext_wall_surface_area*calculator_user_inputs['window_wall_ratio']
    #calculate ua_bldg
    ua_bldg = (
        roof_area*calculator_user_inputs['roof_thermal_perf_type'] +
        ext_wall_surface_area*calculator_user_inputs['wall_thermal_perf_type'] +
        window_area*calculator_user_inputs['window_u_factor']
    )
    return ua_bldg


def calculate_sa_to_vol_ratio(calculator_user_inputs):
    # calculate roof area
    roof_area = calculate_roof_area(calculator_user_inputs)
    #calculate surface to volume ratio
    sa_to_vol_ratio = (
        2. * ((
            calculator_user_inputs['aspect_ratio']/roof_area
            ) ** 0.5 +
            (1./(calculator_user_inputs['aspect_ratio']*roof_area)
            ) **0.5) +
        (1./(10.*calculator_user_inputs["number_of_floors"]))
    )
    return sa_to_vol_ratio