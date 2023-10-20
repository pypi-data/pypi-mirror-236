"""This module contains multiple configuration examples for the
biogas plant.

"""
import logging
import sys
import pandas as pd
import numpy as np

LOG = logging.getLogger(__name__)

ALL_PRESETS = [
    # (XX,1)  for power curve interpolation
    # (XX,2)  for other method  (power_coefficient_curve(function of density))
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
    (8, 1),
    (15, 1),
]
# List of tuples


def turbine_preset(pn_max_kw, **kwargs):
    """Return the parameter configuration for a turbine model
    from the
    .

    """
    thismodule = sys.modules[
        __name__
    ]  # Accessing a function defined in the current module
    # num_gens = kwargs.get("num_gens", None)

    actual_pn_max_kw = max(2, min(15, pn_max_kw))
    if actual_pn_max_kw != pn_max_kw:
        LOG.warning(
            f"Invalid nominal power for Wind Turbine: {pn_max_kw}. "
            f"Will use {actual_pn_max_kw} instead"
        )
        pn_max_kw = actual_pn_max_kw
    possible_p = [val for val in ALL_PRESETS if val[0] == pn_max_kw]

    # if num_gens is not None:
    #      possible_p = [val for val in possible_p if val[1] == num_gens]

    # method_params = f"params_{possible_p[0][1]}g_{possible_p[0][0]}kw"     #params_1g_80kw
    method_params = f"params_turbine_{possible_p[0][0]}kw"

    # method_inits = f"inits_{possible_p[0][1]}g_{possible_p[0][0]}kw"       #inits_1g_40kw
    method_inits = f"inits_turbine_{possible_p[0][0]}kw"  # inits_1g_40kw

    params = getattr(thismodule, method_params)()
    params["sign_convention"] = "active"

    return params, getattr(thismodule, method_inits)()


def params_turbine_3kw():
    """Params for a Turbuine type with 3 kw nominal power
    Nominal power  in W .
    """
    return {
        "rotor_diameter": 82,
        "turbine_type": "E-82/3000",
        #   "power_coefficient_curve_wind_speeds": pd.Series([4.0, 5.0, 6.0]),
        #   "power_coefficient_curve_values": pd.Series([0.3, 0.4, 0.5]),
        #  "density": pd.Series(data=[1.3, 1.3, 1.3]),
        #  "density_correction": False,
        "power_curve_wind_speeds": pd.Series(
            [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
                15.0,
                16.0,
                17.0,
                18.0,
                19.0,
                20.0,
                21.0,
                22.0,
                23.0,
                24.0,
                25.0,
            ]
        ),
        "power_curve_values": pd.Series(
            [
                0.0,
                0.0,
                25.0,
                82.0,
                174.0,
                321.0,
                525.0,
                800.0,
                1135.0,
                1510.0,
                1880.0,
                2200.0,
                2500.0,
                2770.0,
                2910.0,
                3000.0,
                3020.0,
                3020.0,
                3020.0,
                3020.0,
                3020.0,
                3020.0,
                3020.0,
                3020.0,
                3020.0,
            ]
        ),
        "wind_speed_height": 10,  # Height for which the parameter `wind_speed` applies.
        "obstacle_height": 0,
        "air_density": np.array([1.3, 1.3, 1.3]),
    }


def inits_turbine_3kw():
    return {}


def params_turbine_8kw():
    """Params for a Turbuine type with 8 kw nominal power
    Nominal power  in W .
    """
    return {
        "rotor_diameter": 164,
        "turbine_type": "V164/8000",
        #  "power_coefficient_curve_wind_speeds": pd.Series([4.0, 5.0, 6.0]),
        #  "power_coefficient_curve_values": pd.Series([0.3, 0.4, 0.5]),
        #  "density": pd.Series(data=[1.3, 1.3, 1.3]),
        #  "density_correction": False,
        "power_curve_wind_speeds": pd.Series(
            [
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
                15.0,
                16.0,
                17.0,
                18.0,
                19.0,
                20.0,
                21.0,
                22.0,
                23.0,
                24.0,
                25.0,
            ]
        ),
        "power_curve_values": pd.Series(
            [
                0.0,
                0.0,
                0.0,
                91.8,
                526.7,
                1123.1,
                2043.9,
                3134.6,
                4486.4,
                6393.2,
                7363.8,
                7834.4,
                8026.4,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
                8077.2,
            ]
        ),
        "wind_speed_height": 10,  # Height for which the parameter `wind_speed` applies.
        "obstacle_height": 0,
        "air_density": np.array([1.3, 1.3, 1.3]),
    }


def inits_turbine_8kw():
    return {}


def params_turbine_2kw():
    """Params for a Turbuine type with 3 kw nominal power
    Nominal power  in W .
    """
    return {
        "rotor_diameter": 82,
        "hub_height": 69,
        "turbine_type": "E-82/2000 E2",
        #   "power_coefficient_curve_wind_speeds": pd.Series([4.0, 5.0, 6.0]),
        #   "power_coefficient_curve_values": pd.Series([0.3, 0.4, 0.5]),
        #  "density": pd.Series(data=[1.3, 1.3, 1.3]),
        #  "density_correction": False,
        "power_curve_wind_speeds": pd.Series(
            [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
                15.0,
                16.0,
                17.0,
                18.0,
                19.0,
                20.0,
                21.0,
                22.0,
                23.0,
                24.0,
                25.0,
            ]
        ),
        "power_curve_values": pd.Series(
            [
                0.0,
                3.0,
                25.0,
                82.0,
                174.0,
                321.0,
                532.0,
                815.0,
                1180.0,
                1580.0,
                1810.0,
                1980.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
                2050.0,
            ]
        ),
        "wind_speed_height": 10,  # Height for which the parameter `wind_speed` applies.
        "obstacle_height": 0,
        "air_density": np.array([1.3, 1.3, 1.3]),
    }


def inits_turbine_2kw():
    return {}


def params_turbine_15kw():
    """Params for a Turbuine type with 3 kw nominal power
    Nominal power  in W .
    """
    return {
        "rotor_diameter": 240,
        "hub_height": 150,
        "turbine_type": "IEA 15 MW offshore reference turbine",
        "temperature_height": 2,
        #   "power_coefficient_curve_wind_speeds": pd.Series([4.0, 5.0, 6.0]),
        #   "power_coefficient_curve_values": pd.Series([0.3, 0.4, 0.5]),
        #  "density": pd.Series(data=[1.3, 1.3, 1.3]),
        #  "density_correction": False,
        "power_curve_wind_speeds": pd.Series(
            [
                3.0,
                3.5,
                4.0,
                4.5,
                4.8,
                5.0,
                5.2,
                6.0,
                6.2,
                6.4,
                6.5,
                6.6,
                6.6,
                6.7,
                6.8,
                6.9,
                6.9,
                6.9,
                6.9,
                7.0,
                7.0,
                7.0,
                7.0,
                7.0,
                7.0,
                7.5,
                8.0,
                8.5,
                9.0,
                9.5,
                10.0,
                10.2,
                10.5,
                10.6,
                10.7,
                10.7,
                10.7,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.9,
                11.0,
                11.2,
                11.5,
                11.8,
                12.0,
                13.0,
                14.0,
                15.0,
                17.5,
                20.0,
                22.5,
                25.0,
            ]
        ),
        "power_curve_values": pd.Series(
            [
                70.0,
                302.0,
                595.1,
                964.9,
                1185.1,
                1429.2,
                1695.2,
                2656.3,
                2957.2,
                3275.7,
                3442.7,
                3528.6,
                3615.0,
                3791.2,
                3972.0,
                4155.6,
                4192.4,
                4210.8,
                4228.8,
                4247.2,
                4265.5,
                4283.9,
                4302.0,
                4320.3,
                4339.3,
                5338.8,
                6481.1,
                7774.6,
                9229.2,
                10855.0,
                12661.2,
                13638.2,
                14660.7,
                14994.8,
                14994.7,
                14994.6,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.6,
                14994.5,
                14994.4,
                14994.3,
                14994.0,
                14994.1,
                14994.2,
                14994.2,
                14994.8,
                14994.8,
                14994.8,
                14994.8,
                14994.8,
                14996.3,
                14997.6,
            ]
        ),
        "wind_speed_height": 10,  # Height for which the parameter `wind_speed` applies.
        "obstacle_height": 0,
        "air_density": np.array([1.3, 1.3, 1.3]),
    }


def inits_turbine_15kw():
    return {}


def params_turbine_xkw():
    """Params for a Turbuine type with 3 kw nominal power
    Nominal power  in W .
    """
    return {
        "rotor_diameter": 82,
        "turbine_type": "E-82/2000",
        #   "power_coefficient_curve_wind_speeds": pd.Series([4.0, 5.0, 6.0]),
        #   "power_coefficient_curve_values": pd.Series([0.3, 0.4, 0.5]),
        #  "density": pd.Series(data=[1.3, 1.3, 1.3]),
        #  "density_correction": False,
        "power_curve_wind_speeds": pd.Series(),
        "power_curve_values": pd.Series(),
        "wind_speed_height": 10,  # Height for which the parameter `wind_speed` applies.
        "obstacle_height": 0,
        "air_density": np.array([1.3, 1.3, 1.3]),
    }


def inits_turbine_xkw():
    return {}
