import numpy as np
import pandas as pd


def logarithmic_profile(
    wind_speed,
    wind_speed_height,
    hub_height,
    roughness_length,
    obstacle_height=0.0,
):

    if (
        0.7 * obstacle_height > wind_speed_height
    ):  # not strong enough to overcome
        raise ValueError(
            "To take an obstacle height of {0} m ".format(obstacle_height)
            + "into consideration, wind "
            + "speed data of a greater height is needed."
        )
    # Return np.array if wind_speed is np.array       #  check if wind_speed is  a  np.array object
    if isinstance(wind_speed, np.ndarray) and isinstance(
        roughness_length, pd.Series
    ):
        roughness_length = np.array(roughness_length)

    return (
        wind_speed
        * np.log((hub_height - 0.7 * obstacle_height) / roughness_length)
        / np.log(
            (wind_speed_height - 0.7 * obstacle_height) / roughness_length
        )
    )


# the other method Hellme
