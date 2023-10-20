from __future__ import annotations
import gdsfactory as gf
from cnmpdk.config import PATH
from cnmpdk.tech import LAYER
@gf.cell
def cnmMMI1x2DE_BB() -> gf.Component:
    """Return cnmMMI1x2DE_BB fixed cell."""
    c = gf.Component()
    c = gf.import_gds(PATH.library_path, "cnmMMI1x2DE_BB")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=LAYER.PORT)
    c.add_port(name="out0",center=[66.08700,-3.85],width=1.2,orientation=0,layer=LAYER.PORT)
    c.add_port(name="out1",center=[66.08700,3.85],width=1.2,orientation=0,layer=LAYER.PORT)
    return c