from __future__ import annotations
import gdsfactory as gf
from cnmpdk.config import PATH

@gf.cell
def cnmMMI2x2SH_BB() -> gf.Component:
    """Return cnmMMI2x2SH_BB fixed cell."""
    c = gf.Component()
    c = gf.import_gds(PATH.library_path, "cnmMMI2x2SH_BB")
    c.add_port(name="in0",center=[0,-4.6],width=1.2,orientation=180,layer=1)
    c.add_port(name="in1",center=[0,4.6],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[214.50600,-4.6],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[214.50600,4.6],width=1.2,orientation=0,layer=1)
    return c