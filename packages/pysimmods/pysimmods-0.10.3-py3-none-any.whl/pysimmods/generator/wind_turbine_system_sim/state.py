"""This module contains the state model of the Wind Turbine System."""
from ...model.state import ModelState


class WindTurbineSystemState(ModelState):
    def __init__(self, inits):
        super().__init__(inits)

        self.p_possible_max_kw: float = 0
