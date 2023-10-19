from __future__ import annotations
import gdsfactory as gf
from cnmpdk.config import PATH
from cnmpdk.tech import LAYER

@gf.cell
def cnmMMI2x2DE_BB() -> gf.Component:
    """Return cnmMMI2x2DE_BB fixed cell."""
    c = gf.Component()
    c = gf.import_gds(PATH.library_path, "cnmMMI2x2DE_BB")
    c.add_port(name="in0",center=[0,-4.5],width=1.2,orientation=180,layer=LAYER.PORT)
    c.add_port(name="in1",center=[0,4.5],width=1.2,orientation=180,layer=LAYER.PORT)
    c.add_port(name="out0",center=[205.42000,-4.5],width=1.2,orientation=0,layer=LAYER.PORT)
    c.add_port(name="out1",center=[205.42000,4.5],width=1.2,orientation=0,layer=LAYER.PORT)
    return c