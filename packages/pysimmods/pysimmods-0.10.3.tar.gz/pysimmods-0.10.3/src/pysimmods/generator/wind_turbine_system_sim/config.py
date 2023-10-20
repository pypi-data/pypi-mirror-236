"""This module contains the config of the Wind Turbine System."""
from ...generator.turbinesim.config import TurbineConfig
from ...model.config import ModelConfig
from ...other.invertersim.config import InverterConfig


class WindTurbineSystemConfig(ModelConfig):
    def __init__(self, params):
        super().__init__(params)
        params["wind_turbine"]["sign_convention"] = self.sign_convention
        params["inverter"]["sign_convention"] = self.sign_convention

        # Those are duplicate to the original configs
        self._turbine = TurbineConfig(params["wind_turbine"])
        self._inverter = InverterConfig(params["inverter"])

        self.default_p_schedule = None
        self.default_q_schedule = None

    @property
    def s_max_kva(self):
        return self._inverter.s_max_kva

    @property
    def q_control(self):
        return self._inverter.q_control

    @property
    def cos_phi(self):
        return self._inverter.cos_phi

    @property
    def p_max_kw(self):
        return self._turbine.p_max_kw

    @property
    def p_min_kw(self):
        return self._turbine.p_min_kw
