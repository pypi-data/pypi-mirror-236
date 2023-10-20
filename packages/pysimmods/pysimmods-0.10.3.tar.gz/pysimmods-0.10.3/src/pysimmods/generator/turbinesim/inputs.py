"""This module contains the input model for PV plant."""
from pysimmods.model.inputs import ModelInputs


class TurbineInputs(ModelInputs):
    """Input variables of Wind plant model.

    See :class:`pysimmods.model.inputs.ModelInputs` for additional
    information. This class has no inputs itself. Instead, each
    of the values is to be provided before each step.

    Attributes
    ----------
    t_air_deg_celsius:
        Air temperature in [°C].
    wind_v_m_per_s:
        Wind speed in meter per second
    """

    def __init__(self):
        super().__init__()
        self.t_air_deg_celsius = None
        self.wind_v_m_per_s = None
