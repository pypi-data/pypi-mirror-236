"""This module contains a model of a wind turbine and an inverter"""
from ..turbinesim import WindPowerPlant
from .config import WindTurbineSystemConfig
from .inputs import WindTurbineSystemInputs
from .state import WindTurbineSystemState

from ...model.qgenerator import QGenerator
from ...other.invertersim.inverter import Inverter


class WindTurbineSystem(QGenerator):
    def __init__(self, params, inits):
        self.config = WindTurbineSystemConfig(params)
        self.inputs = WindTurbineSystemInputs()
        self.state = WindTurbineSystemState(inits)

        self.turbine = WindPowerPlant(
            params["wind_turbine"], inits["wind_turbine"]
        )
        self.inverter = Inverter(params["inverter"], inits["inverter"])

    def step(self):
        """Perform simulation step."""

        # Step the wind turbine
        self.turbine.inputs.step_size = self.inputs.step_size
        self.turbine.inputs.now_dt = self.inputs.now_dt
        self.turbine.inputs.wind_v_m_per_s = self.inputs.wind_v_m_per_s
        self.turbine.inputs.t_air_deg_celsius = self.inputs.t_air_deg_celsius
        self.turbine.step()

        # Step the inverter
        self.inverter.inputs.p_in_kw = self.turbine.state.p_kw
        self.inverter.inputs.p_set_kw = self.inputs.p_set_kw
        self.inverter.inputs.q_set_kvar = self.inputs.q_set_kvar
        self.inverter.inputs.cos_phi_set = self.inputs.cos_phi_set
        self.inverter.inputs.inductive = self.inputs.inverter_inductive
        self.inverter.step()

        # Update state
        self.state.p_kw = self.inverter.state.p_kw
        self.state.p_possible_max_kw = self.turbine.state.p_kw
        self.state.q_kvar = self.inverter.state.q_kvar
        self.state.cos_phi = self.inverter.state.cos_phi
        self.state.inverter_inductive = self.inverter.state.inductive

        self.inputs.reset()

    def get_state(self):
        state_dict = {
            "wind_turbine": self.turbine.get_state(),
            "inverter": self.inverter.get_state(),
        }
        return state_dict

    def set_state(self, state_dict):
        self.turbine.set_state(state_dict["wind_turbine"])
        self.inverter.set_state(state_dict["inverter"])

        self.state.p_possible_max_kw = self.turbine.state.p_kw
        self.state.p_kw = self.inverter.state.p_kw
        self.state.q_kvar = self.inverter.state.q_kvar
        self.state.cos_phi = self.inverter.state.cos_phi
        self.state.inverter_inductive = self.inverter.state.inductive

    def set_q_kvar(self, q_kvar: float):
        self.inputs.q_set_kvar = q_kvar
