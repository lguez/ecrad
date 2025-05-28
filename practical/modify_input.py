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
            "aerosol_optics_override_file_name": "aer_opt_LMDZ_RRTMG.nc",
            "i_aerosol_type_map": [-7, -6, -5, 1, 1, 1, -2, 3, 2, 2, -4],
        }
    },
    "aer_LMDZ_nml.txt",
)
print('Created file "aer_LMDZ_nml.txt".')

# Atmosphere of LMDZ. Do not use f90nml.patch because we change the
# length of i_aerosol_type_map. Also, we have to specify albedo bands
# because, in the input file coming from LMDZ, the albedo has 6
# bands. We did not need to specify albedo bands with the input file
# from ERA5 because there was a single albedo value for the shortwave
# in this file.
nml = f90nml.read("aer_LMDZ_nml.txt")
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
)
nml.write("atm_LMDZ_nml.txt", force=True)
print('Created file "atm_LMDZ_nml.txt".')

# Atmosphere of ERA5, ECCKD:
# Do not use patch because we delete a key:
nml = f90nml.read("control_nml.txt")
nml["radiation"].update(
    {
        "use_general_cloud_optics": True,
        "gas_model_name": "ECCKD",
        "use_general_aerosol_optics": True,
    }
)
del nml["radiation"]["aerosol_optics_override_file_name"]
nml.write("ECCKD_nml.txt", force=True)
print('Created file "ECCKD_nml.txt".')

# Atmosphere of LMDZ, ECCKD:
nml = f90nml.read("ECCKD_nml.txt")
nml["radiation"].update(
    {
        "aerosol_optics_override_file_name": "aer_opt_LMDZ_ECCKD.nc",
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
)
nml.write("atm_LMDZ_ECCKD_nml.txt", force=True)
print('Created file "atm_LMDZ_ECCKD_nml.txt".')
