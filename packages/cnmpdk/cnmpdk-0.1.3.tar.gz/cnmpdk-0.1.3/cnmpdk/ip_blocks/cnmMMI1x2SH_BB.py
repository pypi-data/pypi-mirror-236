from __future__ import annotations
import gdsfactory as gf
from cnmpdk.config import PATH

@gf.cell
def cnmMMI1x2SH_BB() -> gf.Component:
    """Return cnmMMI1x2SH_BB fixed cell."""
    c = gf.Component()
    c = gf.import_gds(PATH.library_path, "cnmMMI1x2SH_BB")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[91.48900,-4.65],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[91.48900,4.65],width=1.2,orientation=0,layer=1)
    return c