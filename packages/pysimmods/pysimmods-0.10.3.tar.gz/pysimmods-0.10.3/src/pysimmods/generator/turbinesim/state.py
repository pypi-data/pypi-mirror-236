"""This module contains the state model for pv."""
from pysimmods.model.state import ModelState


class TurbineState(ModelState):
    """State parameters of Wind model.

    See :class:`pysimmods.model.state.ModelState` for additional
    information.

    Parameters
    ----------
    inits : dict
        Contains the initial configuration of this wind plant. See
        attributes section for specific to the wind plant.

    Attributes
    ----------
    t_module_deg_celsius : float
        Temperature of the module in [°C].

    """

    def __init__(self, inits):
        super().__init__(inits)
