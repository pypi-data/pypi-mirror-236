from __future__ import annotations
import gdsfactory as gf
from cnmpdk.config import PATH
from cnmpdk.tech import LAYER


@gf.cell
def cnmINVTAP_10_0() -> gf.Component:
    """Return cnmINVTAP_10 fixed cell."""
    c = gf.Component()
    c = gf.import_gds(PATH.library_path, "cnmINVTAP_10.0")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=LAYER.PORT)
    c.add_port(name="out0",center=[425.12500,0],width=0.95,orientation=0,layer=LAYER.PORT)
    return c