import gdsfactory as gf

from cnmpdk.config import PATH

import gdsfactory as gf
from pydantic import BaseModel
from gdsfactory.typings import Layer
from functools import partial
from gdsfactory.technology import LayerLevel, LayerStack
from gdsfactory.cross_section import cross_section

# Define PDK Materials
class LayerMap(BaseModel):
    SHALLOW_WAVEGUIDES: Layer = (1, 0)
    DEEP_WAVEGUIDES: Layer = (2, 0)
    TRENCH: Layer = (3, 0)
    HEATER: Layer = (4, 0)
    DEEP_WAVEGUIDES_PROTECTION: Layer = (11, 0)
    SHALLOW_WAVEGUIDES_PROTECTION: Layer = (21, 0)
    DICING_LINES: Layer = (100, 0)
    PORT: Layer = (1,10)
    BB_OUTLINE: Layer = (51,0)
    BB_GUIDES: Layer = (52,0)
    BB_PARAMETERS: Layer = (53,0)
    
LAYER = LayerMap()

# Define XSections
deep = gf.partial(
    gf.cross_section.strip,
    width=1.2,
    radius=100,
    layer=LAYER.DEEP_WAVEGUIDES,
    # cladding_layers=(LAYER.DEEP_WAVEGUIDES,LAYER.DEEP_WAVEGUIDES_PROTECTION),      TODO: Delete or fix
    # cladding_offsets=(0.1,15,-15,-0.1),                                            TODO: Delete or fix
)
shallow = gf.partial(
    gf.cross_section.strip,
    width=1.2,
    radius=150,
    layer=LAYER.SHALLOW_WAVEGUIDES,
    # cladding_layers=(LAYER.SHALLOW_WAVEGUIDES,LAYER.SHALLOW_WAVEGUIDES_PROTECTION), TODO: Delete or fix
    # cladding_offsets=(0.1,15,-15,-0.1),                                             TODO: Delete or fix
)
heater = gf.partial(
    cross_section,
    width=10,
    layer=LAYER.HEATER,
    # name="cnm_heater",TODO: Delete or fix
    # add_bbox=None,    TODO: Delete or fix
)
trench = gf.partial(
    cross_section,
    width=10,
    layer=LAYER.TRENCH,
    # name="cnm_trench", TODO: Delete or fix
    # add_bbox=None,     TODO: Delete or fix
)

cnm_cross_sections = dict( cnm_deep=deep, cnm_trench=trench, cnm_heater=heater, cnm_shallow=shallow)

nm = 1e-3
um = 1

def get_layer_stack_cnmpdk(
    Thermal_SiO2_thickness: float = -2.5*um,
    zmin_Thermal_SiO2: float = -2.5*um,

    LPCVD_Si3N4_thickness: float = 300 * nm,
    zmin_LPCVD_Si3N4: float = 0.0,

    PECVD_SiO2_thickness: float = -2*um,
    zmin_PECVD_SiO2: float = 300*nm,

    thickness_Cr: float = 10 * nm,
    zmin_Cr: float = 300*nm + 2*um,

    thickness_Au: float = 90*nm,
    zmin_Au: float = 300*nm + 2*um + 90*nm,
) -> LayerStack:
    """Returns cnmpdk LayerStack"""

    return LayerStack(
        layers=dict(
            # substrate=LayerLevel(
            #     layer=LAYER.DICING_LINES,
            #     thickness=substrate_thickness,
            #     zmin=-substrate_thickness - box_thickness,
            #     material="Si",
            #     mesh_order=101,
            #     background_doping={"concentration": "1E14", "ion": "Boron"},
            #     orientation="100",
            # ),
            box=LayerLevel(
                layer=LAYER.DICING_LINES,
                thickness=Thermal_SiO2_thickness,
                zmin=zmin_Thermal_SiO2,
                material="Thermal_SiO2",
                mesh_order=9,
            ),

            wg=LayerLevel(
                layer=LAYER.DEEP_WAVEGUIDES,
                thickness=LPCVD_Si3N4_thickness,
                zmin=0,
                material="LPCVD_Si3N4",
            ),

            metal1=LayerLevel(
                layer=LAYER.HEATER,
                thickness=thickness_Cr,
                zmin=zmin_Cr,
                material="Cr",
                mesh_order=2,
            ),
            metal2=LayerLevel(
                layer=LAYER.HEATER,
                thickness=thickness_Au,
                zmin=zmin_Au,
                material="Au",
                mesh_order=2,
            ),
        )
    )
               

LAYER_STACK = get_layer_stack_cnmpdk()