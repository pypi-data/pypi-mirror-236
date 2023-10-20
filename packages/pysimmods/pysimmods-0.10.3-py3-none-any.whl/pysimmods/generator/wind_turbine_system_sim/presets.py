from pysimmods.generator.turbinesim.presets import turbine_preset


def wind_presets(
    pn_max_kw,
    cos_phi=0.9,
    q_control="prioritize_p",
    inverter_mode="inductive",
    **kwargs
):
    print(pn_max_kw, cos_phi, q_control, inverter_mode, kwargs)
    wparams, winit = turbine_preset(pn_max_kw, **kwargs)

    params = {
        "wind_turbine": wparams,
        "inverter": {
            "sn_kva": pn_max_kw / cos_phi,
            "q_control": q_control,
            "cos_phi": cos_phi,
            "inverter_mode": inverter_mode,
        },
        "sign_convention": "active",
    }

    inits = {"wind_turbine": winit, "inverter": None}

    return params, inits
