"""This module contains the config model for the Wind plant."""
import pandas as pd

from pysimmods.model.config import ModelConfig
import pandas as pd


class TurbineConfig(ModelConfig):
    """Config parameters of Wind plant model.

    Parameters
    ----------
    params : dict
        Contains the configuration of the turbine. See attribute
        section for more information about the parameters, attributes
        marked with *(Input)* can or must be provided.

    Attributes
    ----------


    """

    def __init__(self, params):
        super().__init__(params)

        self.wind_speed_height = params.get("wind_speed_height", 11)
        self.roughness_length = params.get("roughness_length", 15)
        self.obstacle_height = params.get("obstacle_height", 5)
        self.air_density = params.get("air_density", 1.225)
        self.nominal_power = params.get("nominal_power", 3e6)
        self.hub_height = params.get("hub_height", 105)
        self.rotor_diameter = params.get("rotor_diameter", 60)
        self.turbine_type = params.get("turbine_type", "E-126/4200")
        self.pressure = params.get("pressure", 98405.7)
        self.temperature = params.get("temperature", 268)
        self.temperature_height = params.get("temperature_height", 10)
        power_curve_values = params.get(
            "power_curve_values",
            [
                p * 1000
                for p in [  # from kw to w
                    0.0,
                    26.0,
                    180.0,
                    1500.0,
                    3000.0,
                    3000.0,
                ]
            ],
        )
        power_curve_wind_speed = params.get(
            "power_curve_wind_speeds", [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
        )

        self.power_curve = pd.DataFrame(
            data={
                "value": power_curve_values,
                "wind_speed": power_curve_wind_speed,
            }
        )
        # print(self.power_curve)
        # self.power_curve = params.get(
        #    "power_curve",
        #    pd.DataFrame(
        #        data={
        #            "value": [
        #                p * 1000
        #                for p in [  # from kw to w
        #                    0.0,
        #                    26.0,
        #                    180.0,
        #                    1500.0,
        #                    3000.0,
        #                    3000.0,
        #                ]
        #            ],  # in W
        #            "wind_speed": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        #        }
        #    ),
        # )
        #     self.wind_speed = params.get(
        #        "wind_speed",
        #   pd.Series(data=[5.0, 6.5]),
        #    )

        # self.p_max_kw = self.eta_percent / 100 * self.a_m2
        self.p_min_kw = 0
        # self.max_step_size = 300
        self.default_p_schedule = None
        self.default_q_schedule = None
