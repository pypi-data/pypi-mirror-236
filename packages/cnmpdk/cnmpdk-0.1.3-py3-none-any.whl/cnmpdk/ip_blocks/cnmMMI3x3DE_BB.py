from __future__ import annotations
import gdsfactory as gf
from cnmpdk.config import PATH

@gf.cell
def cnmMMI3x3DE_BB() -> gf.Component:
    """Return cnmMMI3x3DE_BB fixed cell."""
    c = gf.Component()
    c = gf.import_gds(PATH.library_path, "cnmMMI3x3DE_BB")
    c.add_port(name="in0",center=[0,-5.65],width=1.2,orientation=180,layer=1)
    c.add_port(name="in1",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="in2",center=[0,5.65],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[210.47700,-5.65],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[210.47700,0],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[210.47700,5.65],width=1.2,orientation=0,layer=1)
    return c