from __future__ import annotations

import gdsfactory as gf
from gdsfactory.get_factories import get_cells
from gdsfactory.pdk import Pdk, constants


from cnmpdk import components
from cnmpdk import ip_blocks

from cnmpdk.config import PATH
from cnmpdk.tech import LAYER, cnm_cross_sections
# from cnmpdk.xsections import cross_sections
from cnmpdk.tech import deep, trench, heater, shallow
from functools import partial
from gdsfactory.technology import LayerView, LayerViews

cells = get_cells([components])

PDK = Pdk(
    name="cnmpdk",
    cells=cells,
    cross_sections= cnm_cross_sections,
    layers=LAYER.dict(),
    layer_stack=None,
    layer_views= LayerViews(filepath=PATH.lyp_2_yaml),
    # layer_transitions=LAYER_TRANSITIONS,
    # sparameters_path=PATH.sparameters,
    constants=constants,
)

# TODO: Remove if not needed
gf.routing.all_angle.LOW_LOSS_CROSS_SECTIONS = [
    {"cross_section": "rib", "settings": {"width": 2.5}},
    {"cross_section": "strip", "settings": {"width": 6.0}},
    {"cross_section": "strip", "settings": {"width": 3.0}},
]

PDK.activate()

if __name__ == "__main__":
    # layer_views = LayerViews(filepath=PATH.lyp_yaml)
    # layer_views.to_lyp(PATH.lyp)
    print(PDK.name)