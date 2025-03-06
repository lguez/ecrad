#!/usr/bin/env python3

import sys
from os import path

import f90nml

script_dir = path.dirname(sys.argv[0])
nml_file_in = path.join(script_dir, "config.nam")
f90nml.patch(
    nml_file_in,
    {
        "radiation_driver": {"do_parallel": False},
        "radiation": {"directory_name": "."},
    },
    "control_nml.txt",
)
print('Created file "control_nml.txt".')

# Aerosols of ERA5 with optical properties of LMDZ aerosols,
# approximative correspondance:
f90nml.patch(
    "control_nml.txt",
    {
        "radiation": {
            "aerosol_optics_override_file_name": "aer_opt_LMDZ_RRTMG_filled.nc",
            "i_aerosol_type_map": [-7, -6, -5, 1, 1, 1, -2, 3, 2, 2, -4],
        }
    },
    "LMDZ_optics_nml.txt",
)
print('Created file "LMDZ_optics_nml.txt".')

# Aerosols of LMDZ with optical properties of LMDZ aerosols:
nml = f90nml.read("LMDZ_optics_nml.txt")
nml["radiation"].update(
    {
        "n_aerosol_types": 13,
        "i_aerosol_type_map": [-1, -2, -3, -4, -5, -6, -7, 1, 2, 3, -8, -9, 4],
        "sw_albedo_wavelength_bound": [
            0.25e-6,
            0.44e-6,
            0.69e-6,
            1.19e-6,
            2.38e-6,
        ],
        "i_sw_albedo_index": [1, 2, 3, 4, 5, 6],
    }
)  # do not use patch because we change the length of i_aerosol_type_map
nml.write("LMDZ_aer_nml.txt", force=True)
print('Created file "LMDZ_aer_nml.txt".')
