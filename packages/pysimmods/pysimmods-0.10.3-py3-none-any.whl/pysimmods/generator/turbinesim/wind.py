"""This module contains a Wind turbine."""

from copy import deepcopy

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pysimmods.generator.turbinesim.config import TurbineConfig
from pysimmods.generator.turbinesim.inputs import TurbineInputs
from pysimmods.generator.turbinesim.state import TurbineState
from pysimmods.model.generator import Generator


class WindPowerPlant(Generator):
    """Simulation model of a windturbine plant."""

    def __init__(self, params, inits):
        self.config = TurbineConfig(params)
        self.state = TurbineState(inits)
        self.inputs = TurbineInputs()

        # self.df = pd.DataFrame()

    def step(self):
        """Perform a simulation step."""
        next_state = deepcopy(self.state)
        self._check_inputs(next_state)

        # What is the formular? Where does it come from?
        wind_speed_hub = (
            self.inputs.wind_v_m_per_s
            * (self.config.hub_height / self.config.wind_speed_height) ** 1
            / 7
        )
        next_state.p_kw = np.interp(
            wind_speed_hub,
            self.config.power_curve["wind_speed"],
            self.config.power_curve["value"],
            left=0,
            right=0,
        )

        # Scale to step size
        next_state.p_kw *= self.inputs.step_size / 3600

        self.state = next_state
        self.inputs.reset()

    def _check_inputs(self, nstate):
        pass

    #
    #
    def temperature_correction(self):
        """Using air tempreture at hub height to correct the power out

        Linear temperature gradient model is used.

        (
            temperature_height (Air temperature in K.),
            temperature (Height in m for which the parameter
                `temperature` applies.
            )
        )
        Hub height of wind turbine in m.
        Temperature gradient of -6.5 K/km (-0.0065 K/m)

        """

        return (
            self.config.temperature,
            self.config.hub_height,
            self.config.temperature_height,
            self.config.temperature
            - 0.0065
            * (self.config.hub_height - self.config.temperature_height),
        )

    #  return self.config.temperature,self.config.hub_height,self.config.temperature_height

    # FIXME: Seems quite redundant right now
    def air_density_correction(self):
        """Formular for air density correction.

        Using air density at hub height to correct the power out.
        Describe the effect of air density-temperature on the generated
        power.
        """
        temperature_hub_height = self.temperature_correction()

        #        return (
        #     (self.config.pressure / 100 - (self.config.hub_height - self.config.pressure_height) * 1 / 8)
        #     * 100
        #     / (287.058 * temperature_hub_height)
        # )

        return temperature_hub_height

    def corr_poweroutput(self):
        out = np.array(self.config.power_curve["wind_speed"])

        #   return np.array(self.config.power_curve["wind_speed"]) , np.array(self.config.power_curve["value"] )

        #         self.config.power_curve["wind_speed"],
        #         self.config.power_curve["value"],

        power_curves_per_ts = (1.225 / self.config.air_density).reshape(
            -1, 1
        ) ** np.interp(
            self.config.power_curve["wind_speed"], [7.5, 12.5], [1 / 3, 2 / 3]
        )

        #                   * self.config.power_curve["wind_speed"]
        # ( (1.225 / self.config.air_density).reshape(-1, 1)
        #   ** np.interp(self.config.power_curve["wind_speed"], [7.5, 12.5], [1 / 3, 2 / 3])
        #   ) * self.config.power_curve["wind_speed"]
        return power_curves_per_ts

    #     # Create the interpolation function
    #     def interp_func(w_speed, p_curves):
    #         return np.interp(
    #         w_speed, p_curves, power_curve_values, left=0, right=0
    #         )

    #     # Calculate the power output by mapping the arrays to the interp function
    #     power_output = np.array(
    #     list(map(interp_func, wind_speed, power_curves_per_ts))
    #     )
    def barometric(
        pressure, pressure_height, hub_height, temperature_hub_height
    ):
        return (
            (pressure / 100 - (hub_height - pressure_height) * 1 / 8)
            * 1.225
            * 288.15
            * 100
            / (101330 * temperature_hub_height)
        )
