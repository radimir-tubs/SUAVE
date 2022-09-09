## @ingroup Methods-Weights-Buildups-Common

# wiring.py
#
# Created: Jun, 2017, J. Smart
# Modified: Feb, 2018, J. Smart
#           Mar 2020, M. Clarke
#           May 2021, M. Clarke

# -------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------

from SUAVE.Core import Units
import numpy as np


# -------------------------------------------------------------------------------
# Wiring
# -------------------------------------------------------------------------------

## @ingroup Methods-Weights-Buildups-Common
def wiring_radi(wing, config, cablePower):
    """ weight = SUAVE.Methods.Weights.Buildups.Common.wiring(
            wing,
            config, 
            cablePower)

        Assumptions:
        Calculates mass of wiring required for a wing, including DC power
        cables and communication cables, assuming power cables run an average of
        half the fuselage length and height in addition to reaching the motor
        location on the wingspan, and that communication and sesor  wires run an
        additional length based on the fuselage and wing dimensions.

        Intended for use with the following SUAVE vehicle types, but may be used
        elsewhere:

            Electric Multicopter
            Electric Vectored_Thrust
            Electric Stopped Rotor

        Originally written as part of an AA 290 project intended for trade study
        of the above vehicle types.

        Sources:
        Project Vahana Conceptual Trade Study

        Inputs:

            config                      SUAVE Config Data Structure
            motor_spanwise_locations    Motor Semi-Span Fractions       [Unitless]
            max_power_draw              Maximum DC Power Draw           [W]

        Outputs:

            weight:                     Wiring Mass                     [kg]

    """

    # ---------------------------------------------------------------------------
    # Unpack Inputs
    # ---------------------------------------------------------------------------
    if 'motor_spanwise_locations' in config.wings[wing.tag]:
        fLength = config.fuselages.fuselage.lengths.total
        fHeight = config.fuselages.fuselage.heights.maximum
        MSL = config.wings[wing.tag].motor_spanwise_locations
        wingspan = wing.spans.projected
        nMotors = max(len(MSL), 1)  # No. of motors on each half-wing, defaults to 1

        # ---------------------------------------------------------------------------
        # Determine mass of Power Cables
        # ---------------------------------------------------------------------------
        cableLength = (nMotors * fHeight) + np.sum(abs(MSL)) * 1.1
        cablePower = cablePower * 1.2

        cableDensity = 5.7e-6
        massCables = cableDensity * cablePower * cableLength

        # # Method Number 2
        # Voltage = 600           # f
        # current = cablePower/600            # Assumed the case with 600V I took it from the
        # cable_cross_section = 1.2e-5
        # cable_density_aluminum = 2700
        # cable_density_per_meter = cable_cross_section * cable_density_aluminum
        # massCables_Radi = cable_density_per_meter * cableLength
        #
        # print('cable_density_per_meter ', cable_density_per_meter)
        # print('massCables_Radi ', massCables_Radi)
        # print('massCables ', massCables)

        # ---------------------------------------------------------------------------
        # Determine mass of sensor/communication wires
        # ---------------------------------------------------------------------------

        wiresPerBundle = 6
        wireDensity = 460e-5
        wireLength = cableLength + (10 * fLength) + 4 * wingspan
        massWires = 2 * wireDensity * wiresPerBundle * wireLength
        # ---------------------------------------------------------------------------
        # Sum Total
        # ---------------------------------------------------------------------------

        weight = massCables + massWires
    else:
        weight = 0.0
    return weight