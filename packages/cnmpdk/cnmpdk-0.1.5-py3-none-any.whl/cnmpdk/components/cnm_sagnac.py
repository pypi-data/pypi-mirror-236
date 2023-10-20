"""cnmpdk straight waveguide."""
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.cross_section import CrossSectionSpec
import cnmpdk
import warnings
from gdsfactory.components.bend_euler import bend_euler
from gdsfactory.typings import (
    ComponentSpec,
    CrossSectionSpec,
)
import math

@gf.cell
def cnm_sagnac(
    radius: float = 100.0,
    bend_spec: ComponentSpec = bend_euler,
    cross_section: CrossSectionSpec = "cnm_deep",
    layer: gf.typings.LayerSpec | None = None,
) -> Component:
    """Returns a Straight waveguide.

    Args:
        length: straight length (um).
        npoints: number of points.
        layer: layer to use. Defaults to cross_section.layer.
        width: width to use. Defaults to cross_section.width.
        add_pins: add pins to the component.
        cross_section: specification (CrossSection, string or dict).

    .. code::

        o1 -------------- o2
                length
    """
    c = gf.Component()
    mmi = c << cnmpdk.ip_blocks.cnmMMI2x2DE_BB()

    # phi_rad = math.acos(1+(9-2*radius)/(4*radius))
    # phi = phi_rad*180/math.pi
    # bend_circ = gf.components.bend_circular(angle=phi, cross_section=cross_section, add_pins=True)
    # bend_bot = c.add_ref(bend_circ).connect("o1", destination=mmi.ports["in0"])
    # bend_top = c.add_ref(bend_circ).connect("o1", destination=mmi.ports["in1"]).mirror_y(y0=4.5)
    # route = gf.routing.get_route(mmi.ports["in0"], mmi.ports["in1"], radius=radius, cross_section=cross_section)
    # TODO: bend_spec

    route = gf.routing.get_route(mmi.ports["in0"], mmi.ports["in1"], radius=radius, cross_section=cross_section)
    c.add(route.references)
    c.add_port("o1", port=mmi.ports["out0"])
    c.add_port("o2", port=mmi.ports["out1"])

    return c

if __name__ == "__main__":
    import gdsfactory as gf

    c = cnm_sagnac(cross_section="cnm_deep")
    # c = straight()
    print(c.info)
    c.show(show_ports=True)
