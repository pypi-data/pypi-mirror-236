# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
from typing import cast

from pdkmaster.technology import property_ as _prp, primitive as _prm
from pdkmaster.design import circuit as _ckt, layout as _lay, library as _lbry
from pdkmaster.io.klayout import merge

from c4m.flexio import IOSpecification, TrackSpecification, IOFrameSpecification, IOFactory

from .pdkmaster import tech, cktfab, layoutfab
from .stdcell import stdcell1v2lambdalib

__all__ = [
    "ihpsg13g2_iospec", "ihpsg13g2_ioframespec", "IHPSG13g2IOFactory",
    "ihpsg13g2_iofab", "iolib",
]


_prims = tech.primitives

_cell_width = 80.0
_cell_height = 180.0
ihpsg13g2_iospec = IOSpecification(
    stdcelllib=stdcell1v2lambdalib,
    nmos=cast(_prm.MOSFET, _prims.sg13g2_lv_nmos), pmos=cast(_prm.MOSFET, _prims.sg13g2_lv_pmos),
    ionmos=cast(_prm.MOSFET, _prims.sg13g2_hv_nmos),
    iopmos=cast(_prm.MOSFET, _prims.sg13g2_hv_pmos),
    monocell_width=_cell_width, 
    metal_bigspace=0.6, topmetal_bigspace=4.0,
    clampnmos=None, clampnmos_w=14, clampnmos_l=0.6,
    clamppmos=None, clamppmos_w=36, clamppmos_l=0.6,
    clampfingers=32, clampfingers_analog=20, clampdrive=3,
    clampgate_gatecont_space=0.24, clampgate_sourcecont_space=0.24,
    clampgate_draincont_space=0.51,
    add_clampsourcetap=False,
    clampsource_cont_tap_enclosure=_prp.Enclosure((0.265, 0.06)), clampsource_cont_tap_space=0.075,
    clampdrain_layer=None, clampgate_clampdrain_overlap=None, clampdrain_active_ext=None,
    clampdrain_gatecont_space=None, clampdrain_contcolumns=1, clampdrain_via1columns=2,
    nres=cast(_prm.Resistor, _prims.Rppd),
    pres=cast(_prm.Resistor, _prims.Rppd),
    ndiode=cast(_prm.Diode, _prims.ndiode),
    pdiode=cast(_prm.Diode, _prims.pdiode),
    secondres_width=1.0, secondres_length=2.0,
    secondres_active_space=0.6,
    corerow_height=10, corerow_nwell_height=6,
    iorow_height=8.5, iorow_nwell_height=5.25,
    nwell_minspace=2.0, levelup_core_space=1.0,
    resvdd_prim=cast(_prm.Resistor, _prims.Rppd), resvdd_meander=False,
    resvdd_w=1.0, resvdd_lfinger=20.0, resvdd_fingers=8, resvdd_space=0.65,
    invvdd_n_mosfet=cast(_prm.MOSFET, _prims.sg13g2_hv_nmos),
    invvdd_n_l=0.5, invvdd_n_w=18.0, invvdd_n_fingers=6,
    invvdd_p_mosfet=cast(_prm.MOSFET, _prims.sg13g2_hv_pmos),
    invvdd_p_l=0.5, invvdd_p_w=7.0, invvdd_p_fingers=50,
    capvdd_l=10.0, capvdd_w=18.0, capvdd_fingers=6,
    add_corem3pins=True,
    add_dcdiodes=True,
    dcdiode_actwidth=1.26, dcdiode_actspace=0.99, dcdiode_actspace_end=1.38,
    dcdiode_inneractheight=27.78, dcdiode_diodeguard_space=1.32, dcdiode_fingers=2,
    dcdiode_indicator=_prims["Recog.esd"],
)
ihpsg13g2_ioframespec = IOFrameSpecification(
    cell_height=_cell_height,
    tracksegment_viapitch=2.0,
    pad_height=None,
    padpin_height=3.0,
    pad_width=70.0,
    pad_viapitch=None,
    pad_viacorner_distance=23.0, pad_viametal_enclosure=3.0,
    pad_y=55.32,
    tracksegment_maxpitch=30.0, tracksegment_space={
        None: 2.0,
        cast(_prm.MetalWire, _prims.TopMetal2): 5.0,
    },
    acttracksegment_maxpitch=30, acttracksegment_space=1.0,
    track_specs=(
        TrackSpecification(name="iovss", bottom=5.0, width=50.0),
        TrackSpecification(name="iovdd", bottom=70.0, width=50.8),
        TrackSpecification(name="vddvss", bottom=(_cell_height - 41.0), width=40.0),
    ),
)
class IHPSG13g2IOFactory(IOFactory):
    iospec = ihpsg13g2_iospec
    ioframespec = ihpsg13g2_ioframespec

    def __init__(self, *,
        lib: _lbry.Library, cktfab: _ckt.CircuitFactory, layoutfab: _lay.LayoutFactory,
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            spec=self.iospec, framespec=self.ioframespec,
        )


iolib = _lbry.Library(name="IOLib", tech=tech)
ihpsg13g2_iofab = IHPSG13g2IOFactory(lib=iolib, cktfab=cktfab, layoutfab=layoutfab)
ihpsg13g2_iofab.get_cell("Gallery").layout
merge(iolib)
