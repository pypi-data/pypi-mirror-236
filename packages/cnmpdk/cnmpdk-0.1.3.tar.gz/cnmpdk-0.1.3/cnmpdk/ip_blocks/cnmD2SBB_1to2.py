from __future__ import annotations
import gdsfactory as gf
from cnmpdk.config import PATH

@gf.cell
def cnmD2SBB_1to2() -> gf.Component:
    """Return cnmD2SBB_1to2 fixed cell."""
    c = gf.Component()
    c =  gf.import_gds(PATH.library_path, "cnmD2SBB_1to2")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[73,0],width=2.2,orientation=0,layer=1)
    return c