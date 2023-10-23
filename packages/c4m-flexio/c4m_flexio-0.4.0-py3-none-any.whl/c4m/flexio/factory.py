from math import floor, ceil
from typing import (
    List, Tuple, Dict, Set, Generator, Iterable, Container, Union, Optional, cast,
)
from dataclasses import dataclass

from pdkmaster.typing import MultiT
from pdkmaster.technology import (
    property_ as _prp, primitive as _prm, geometry as _geo, technology_ as _tch,
)
from pdkmaster.design import (
    circuit as _ckt, layout as _lay, cell as _cell, library as _lbry, factory as _fab,
)

from . import _helpers as hlp


__all__ = [
    "IOSpecification", "TrackSpecification", "IOFrameSpecification",
    "FactoryCellT", "IOFactory",
]


_sqrt2 = 2**0.5


class _MetalSpec:
    def __init__(self, *,
        tech: _tch.Technology, spec: "IOSpecification", framespec: "IOFrameSpecification",
        computed: "_ComputedSpecs",
        metal: _prm.MetalWire,
    ):
        self._prim = metal
        self._minwidth_down = tech.computed.min_width(
            metal, up=False, down=True, min_enclosure=True,
        )
        self._minwidth4ext_down = tech.computed.min_width(
            metal, up=False, down=True, min_enclosure=False,
        )
        self._minwidth_up = tech.computed.min_width(
            metal, up=True, down=False, min_enclosure=True,
        )
        self._minwidth4ext_up = tech.computed.min_width(
            metal, up=True, down=False, min_enclosure=False,
        )
        self._minwidth_updown = tech.computed.min_width(
            metal, up=True, down=True, min_enclosure=True,
        )
        self._minwidth4ext_updown = tech.computed.min_width(
            metal, up=True, down=True, min_enclosure=False,
        )
        # Compute min track space
        # first take specific value, otherwise value for None considered default,
        # otherwise metal minimum space
        s = framespec.tracksegment_space
        self.tracksegment_space = s.get(metal, s.get(None, metal.min_space))

        for via in computed.vias:
            if via.bottom[0] == metal:
                self._top_via = via
                break
        else:
            self._top_via = None

    @property
    def prim(self) -> _prm.MetalWire:
        return self._prim
    @property
    def minwidth_down(self) -> float:
        return self._minwidth_down
    @property
    def minwidth4ext_down(self) -> float:
        return self._minwidth4ext_down
    @property
    def minwidth_up(self) -> float:
        return self._minwidth_up
    @property
    def minwidth4ext_up(self) -> float:
        return self._minwidth4ext_up
    @property
    def minwidth_updown(self) -> float:
        return self._minwidth_updown
    @property
    def minwidth4ext_updown(self) -> float:
        return self._minwidth4ext_updown

    @property
    def top_via(self) -> _prm.Via:
        if self._top_via is None:
            raise AttributeError(f"Top via not found for metal '{self.prim.name}'")
        return self._top_via


def _iterate_polygonbounds(*, polygon: _geo.MaskShape) -> Generator[
    _geo._Rectangular, None, None,
]:
    for shape in polygon.shape.pointsshapes:
        yield shape.bounds


class IOSpecification:
    def __init__(self, *,
        stdcelllib: _lbry.Library,
        nmos: _prm.MOSFET, pmos: _prm.MOSFET, ionmos: _prm.MOSFET, iopmos: _prm.MOSFET,
        monocell_width: float,
        metal_bigspace: float, topmetal_bigspace: float,
        clampnmos: Optional[_prm.MOSFET]=None,
        clampnmos_w: float, clampnmos_l: Optional[float]=None,
        clamppmos: Optional[_prm.MOSFET]=None,
        clamppmos_w: float, clamppmos_l: Optional[float]=None,
        clampfingers: int, clampfingers_analog: Optional[int], clampdrive: int,
        clampgate_gatecont_space: float, clampgate_sourcecont_space: float,
        clampgate_draincont_space: float,
        add_clampsourcetap: bool=False,
        clampsource_cont_tap_enclosure: Optional[Union[float, _prp.Enclosure]]=None,
        clampsource_cont_tap_space: Optional[float]=None,
        clampdrain_layer: Optional[_prm.DesignMaskPrimitiveT],
        clampgate_clampdrain_overlap: Optional[float], clampdrain_active_ext: Optional[float],
        clampdrain_gatecont_space: Optional[float],
        clampdrain_contcolumns: int, clampdrain_via1columns: int,
        nres: _prm.Resistor, pres: _prm.Resistor, ndiode: _prm.Diode, pdiode: _prm.Diode,
        secondres_width: float, secondres_length: float,
        secondres_active_space: float,
        corerow_height: float, corerow_nwell_height: float,
        iorow_height: float, iorow_nwell_height: float,
        nwell_minspace: Optional[float]=None, levelup_core_space: float,
        resvdd_prim: Optional[_prm.Resistor]=None, resvdd_meander: bool=True,
        resvdd_w: Optional[float]=None, resvdd_space: Optional[float]=None,
        resvdd_lfinger: Optional[float]=None, resvdd_fingers: Optional[int]=None,
        capvdd_l: Optional[float]=None, capvdd_w: Optional[float]=None,
        capvdd_mosfet: Optional[_prm.MOSFET]=None, capvdd_fingers: Optional[int]=None,
        invvdd_n_l: Optional[float]=None, invvdd_n_w: Optional[float]=None,
        invvdd_n_mosfet: Optional[_prm.MOSFET]=None, invvdd_n_fingers: Optional[int]=None,
        invvdd_p_l: Optional[float]=None, invvdd_p_w: Optional[float]=None,
        invvdd_p_mosfet: Optional[_prm.MOSFET]=None, invvdd_p_fingers: Optional[int]=None,
        add_corem3pins: bool=False,
        add_dcdiodes: bool=False,
        dcdiode_actwidth: Optional[float]=None, dcdiode_actspace: Optional[float]=None,
        dcdiode_actspace_end: Optional[float]=None, dcdiode_inneractheight: Optional[float]=None,
        dcdiode_diodeguard_space: Optional[float]=None, dcdiode_fingers: int=1,
        dcdiode_indicator: Optional[_prm.DesignMaskPrimitiveT]=None,
    ):
        self.stdcelllib = stdcelllib

        self.monocell_width = monocell_width

        self.metal_bigspace = metal_bigspace
        self.topmetal_bigspace = topmetal_bigspace

        self.nmos = nmos
        self.pmos = pmos
        self.ionmos = ionmos
        self.iopmos = iopmos
        self.clampnmos = clampnmos if clampnmos is not None else ionmos
        self.clamppmos = clamppmos if clamppmos is not None else iopmos
        # TODO: Implement proper source implant for transistor
        self.clampnmos_w = clampnmos_w
        if clampnmos_l is not None:
            self.clampnmos_l = clampnmos_l
        else:
            self.clampnmos_l = self.clampnmos.computed.min_l
        self.clamppmos_w = clamppmos_w
        if clamppmos_l is not None:
            self.clamppmos_l = clamppmos_l
        else:
            self.clamppmos_l = self.clamppmos.computed.min_l
        self.clampcount = clampfingers
        self.clampdrive = clampdrive
        self.clampcount_analog = (
            clampfingers_analog if clampfingers_analog is not None
            else clampfingers
        )

        self.clampgate_gatecont_space = clampgate_gatecont_space
        self.clampgate_sourcecont_space = clampgate_sourcecont_space
        self.clampgate_draincont_space = clampgate_draincont_space

        if add_clampsourcetap:
            assert clampsource_cont_tap_enclosure is not None
            assert clampsource_cont_tap_space is not None
            if not isinstance(clampsource_cont_tap_enclosure, _prp.Enclosure):
                clampsource_cont_tap_enclosure = _prp.Enclosure(clampsource_cont_tap_enclosure)
            clampsource_cont_tap_space = clampsource_cont_tap_space
        self.add_clampsourcetap = add_clampsourcetap
        self.clampsource_cont_tap_enclosure = clampsource_cont_tap_enclosure
        self.clampsource_cont_tap_space = clampsource_cont_tap_space
        self.clamp_clampdrain = clampdrain_layer
        self.clampgate_clampdrain_overlap = clampgate_clampdrain_overlap
        self.clampdrain_active_ext = clampdrain_active_ext
        self.clampdrain_gatecont_space = clampdrain_gatecont_space
        self.clampdrain_contcolumns = clampdrain_contcolumns
        self.clampdrain_via1columns = clampdrain_via1columns

        self.nres = nres
        self.pres = pres
        self.ndiode = ndiode
        self.pdiode = pdiode
        self.secondres_width = secondres_width
        self.secondres_length = secondres_length
        self.secondres_active_space = secondres_active_space

        self.corerow_height = corerow_height
        self.corerow_nwell_height = corerow_nwell_height
        self.iorow_height = iorow_height
        self.iorow_nwell_height = iorow_nwell_height
        self.cells_height = self.corerow_height + self.iorow_height
        self.corerow_pwell_height = self.corerow_height - self.corerow_nwell_height
        self.iorow_pwell_height = self.iorow_height - self.iorow_nwell_height

        self.nwell_minspace = nwell_minspace

        self.levelup_core_space = levelup_core_space

        if resvdd_prim is None:
            assert (
                (resvdd_w is None) and (resvdd_lfinger is None)
                and (resvdd_fingers is None) and (resvdd_space is None)
                and (capvdd_l is None) and (capvdd_w is None)
                and (capvdd_mosfet is None) and (capvdd_fingers is None)
                and (invvdd_n_w is None) and (invvdd_n_l is None)
                and (invvdd_n_mosfet is None) and (invvdd_n_fingers is None)
                and (invvdd_p_w is None) and (invvdd_p_l is None)
                and (invvdd_p_mosfet is None) and (invvdd_p_fingers is None)
            )
        else:
            assert (
                (resvdd_w is not None) and (resvdd_lfinger is not None)
                and (resvdd_fingers is not None) and (resvdd_space is not None)
                and (capvdd_l is not None) and (capvdd_w is not None)
                and (capvdd_fingers is not None)
                and (invvdd_n_w is not None) and (invvdd_n_l is not None)
                and (invvdd_n_mosfet is not None) and (invvdd_n_fingers is not None)
                and (invvdd_p_w is not None) and (invvdd_p_l is not None)
                and (invvdd_p_mosfet is not None) and (invvdd_p_fingers is not None)
            )
            resvdd_w = resvdd_w
            resvdd_lfinger = resvdd_lfinger
            resvdd_space = resvdd_space
            capvdd_w = capvdd_w
            capvdd_l = capvdd_l
            if capvdd_mosfet is None:
                capvdd_mosfet = invvdd_n_mosfet
            invvdd_n_w = invvdd_n_w
            invvdd_n_l = invvdd_n_l
            invvdd_p_w = invvdd_p_w
            invvdd_p_l = invvdd_p_l
        self.resvdd_prim = resvdd_prim
        self.resvdd_meander = resvdd_meander
        self.resvdd_w = resvdd_w
        self.resvdd_space = resvdd_space
        self.resvdd_lfinger = resvdd_lfinger
        self.resvdd_fingers = resvdd_fingers
        self.capvdd_l = capvdd_l
        self.capvdd_w = capvdd_w
        self.capvdd_mosfet = capvdd_mosfet
        self.capvdd_fingers = capvdd_fingers
        self.invvdd_n_l = invvdd_n_l
        self.invvdd_n_w = invvdd_n_w
        self.invvdd_n_mosfet = invvdd_n_mosfet
        self.invvdd_n_fingers = invvdd_n_fingers
        self.invvdd_p_l = invvdd_p_l
        self.invvdd_p_w = invvdd_p_w
        self.invvdd_p_mosfet = invvdd_p_mosfet
        self.invvdd_p_fingers = invvdd_p_fingers

        self.add_corem3pins = add_corem3pins

        self.add_dcdiodes = add_dcdiodes
        if not add_dcdiodes:
            assert (
                (dcdiode_actwidth is None) and (dcdiode_actspace is None)
                and (dcdiode_actspace_end is None) and (dcdiode_inneractheight is None)
                and (dcdiode_diodeguard_space is None) and (dcdiode_fingers == 1)
                and (dcdiode_indicator is None)
            )
        else:
            assert (
                (dcdiode_actwidth is not None) and (dcdiode_actspace is not None)
                and (dcdiode_inneractheight is not None) and (dcdiode_diodeguard_space is not None)
                and (dcdiode_fingers > 0)
            )
            if dcdiode_actspace_end is None:
                dcdiode_actspace_end = dcdiode_actspace
            self.dcdiode_actwidth = dcdiode_actwidth
            self.dcdiode_actspace = dcdiode_actspace
            self.dcdiode_actspace_end = dcdiode_actspace_end
            self.dcdiode_inneractheight = dcdiode_inneractheight
            self.dcdiode_diodeguardspace = dcdiode_diodeguard_space
            self.dcdiode_fingers = dcdiode_fingers
            self.dcdiode_indicator = dcdiode_indicator

@dataclass
class _SegmentSpecification:
    bottom: float
    top: float

    @property
    def center(self) -> float:
        return 0.5*(self.bottom + self.top)
    @property
    def height(self) -> float:
        return self.top - self.bottom


@dataclass
class TrackSpecification:
    name: str
    bottom: float
    width: float

    @property
    def center(self) -> float:
        return self.bottom + 0.5*self.width
    @property
    def top(self) -> float:
        return self.bottom + self.width

    def track_segments(self, *,
        tech: _tch.Technology, maxpitch: float,
    ) -> Tuple[_SegmentSpecification, ...]:
        n_segments = int((self.width - _geo.epsilon)/maxpitch) + 1
        width = tech.on_grid(self.width/n_segments, mult=2)

        segments: List[_SegmentSpecification] = []
        for i in range(n_segments):
            bottom = self.bottom + i*width
            # For last segment take top as top of the track
            if i < (n_segments - 1):
                top = bottom + width
            else:
                top = self.bottom + self.width
            segments.append(_SegmentSpecification(bottom=bottom, top=top))

        return tuple(segments)


class IOFrameSpecification:
    track_names: Set[str] = {"iovss", "iovdd", "secondiovss", "vddvss"}

    def __init__(self, *,
        cell_height: float, top_metal: Optional[_prm.MetalWire]=None,
        tracksegment_maxpitch: float, tracksegment_space: Dict[Optional[_prm.MetalWire], float]={},
        tracksegment_viapitch: float,
        acttracksegment_maxpitch: Optional[float]=None, acttracksegment_space: Optional[float]=None,
        pad_width: float, pad_height: Optional[float]=None, pad_y: float,
        pad_viapitch: Optional[float], pad_viacorner_distance: float, pad_viametal_enclosure: float,
        padpin_height: Optional[float]=None,
        track_specs: Iterable[TrackSpecification],
    ):
        self.cell_height = cell_height
        self.top_metal = top_metal

        self.tracksegment_maxpitch = tracksegment_maxpitch
        self.tracksegment_space = tracksegment_space
        self.tracksegement_viapitch = tracksegment_viapitch

        assert (acttracksegment_maxpitch is None) == (acttracksegment_space is None)
        self.acttracksegment_maxpitch = acttracksegment_maxpitch
        self.acttracksegment_space = acttracksegment_space

        if (pad_height is None) == (padpin_height is None):
            raise TypeError("Either pad_height or padpin_height needs to be provided")

        self.pad_width = pad_width
        if pad_height is not None:
            self.pad_height = pad_height
        self.pad_y = pad_y
        self.pad_viapitch = pad_viapitch
        self.pad_viacorner_distance = pad_viacorner_distance
        self.pad_viametal_enclosure = pad_viametal_enclosure
        if padpin_height is not None:
            self.padpin_height = padpin_height
        self.track_specs = track_specs = tuple(track_specs)
        self._track_specs_dict: Dict[str, TrackSpecification] = {
            spec.name: spec for spec in track_specs
        }

        spec_names = {spec.name for spec in track_specs}
        if self.track_names != spec_names:
            missing = self.track_names - spec_names
            if (len(missing) == 1) and ("secondiovss" in missing):
                self._has_secondiovss = False
            elif missing:
                raise ValueError(
                    f"Missing spec for track(s) '{tuple(missing)}'"
                )
            wrong = spec_names - self.track_names
            if wrong:
                raise ValueError(
                    f"Wrong spec for track name(s) '{tuple(wrong)}'"
                )
        else:
            self._has_secondiovss = True

    @property
    def has_secondiovss(self) -> bool:
        return self._has_secondiovss


class _ComputedSpecs:
    def __init__(self, *,
        fab: "IOFactory", framespec: "IOFrameSpecification",
        nmos: _prm.MOSFET, pmos: _prm.MOSFET, ionmos: _prm.MOSFET, iopmos: _prm.MOSFET,
    ):
        self.fab = fab
        spec = fab.spec
        tech = fab.tech

        # assert statements are used for unsupported technology configuration
        # TODO: Implement unsupported technology configurations

        assert nmos.well is None
        assert pmos.well is not None
        assert ionmos.well is None
        assert iopmos.well is not None
        assert pmos.well == iopmos.well

        prims = tech.primitives
        self.nmos = nmos
        self.pmos = pmos
        self.ionmos = ionmos
        self.iopmos = iopmos

        assert nmos.gate == pmos.gate
        assert ionmos.gate == iopmos.gate

        mosgate = nmos.gate
        iomosgate = ionmos.gate

        assert mosgate.oxide is None
        assert iomosgate.oxide is not None
        assert mosgate.active == iomosgate.active
        assert mosgate.poly == iomosgate.poly

        self.active = active = mosgate.active
        self.oxide = iomosgate.oxide
        self.poly = poly = mosgate.poly

        assert active.oxide is not None
        assert active.min_oxide_enclosure is not None
        assert active.min_substrate_enclosure is not None

        # Following code assumes that either (io)nmos or (io)pmos transistor have implants
        # We also use the first implant of a MOSFET as the main implant layer

        # nmos/pmos & nimplant/pimplan
        if nmos.implant:
            nimplant = nmos.implant[0]
            idx = active.implant.index(nimplant)
            nimplant_enc = active.min_implant_enclosure[idx]
        else:
            nimplant = None
            nimplant_enc = None
        self.nimplant = nimplant
        if pmos.implant:
            pimplant = pmos.implant[0]
            idx = active.implant.index(pimplant)
            pimplant_enc = active.min_implant_enclosure[idx]
        else:
            pimplant = None
            pimplant_enc = None
        self.pimplant = pimplant
        if nimplant is not None:
            try:
                space = tech.computed.min_space(nimplant, active)
            except AttributeError:
                space = None
        else:
            space = None
        # Don't overlap implants
        if space is None:
            assert pimplant_enc is not None
            space = pimplant_enc.max()
        elif pimplant_enc is not None:
            space = max(space, pimplant_enc.max())
        self.min_space_nimplant_active = space
        if pimplant is not None:
            try:
                space = tech.computed.min_space(pimplant, active)
            except AttributeError:
                space = None
        else:
            space = None
        # Don't overlap implants
        if space is None:
            assert nimplant_enc is not None
            space = nimplant_enc.max()
        elif nimplant_enc is not None:
            space = max(space, nimplant_enc.max())
        self.min_space_pimplant_active = space

        # ionmos/iopmos & nimplant/pimplant
        if ionmos.implant:
            ionimplant = ionmos.implant[0]
            idx = active.implant.index(ionimplant)
            ionimplant_enc = active.min_implant_enclosure[idx]
        else:
            ionimplant = None
            ionimplant_enc = None
        self.ionimplant = ionimplant
        if iopmos.implant:
            iopimplant = iopmos.implant[0]
            idx = active.implant.index(iopimplant)
            iopimplant_enc = active.min_implant_enclosure[idx]
        else:
            iopimplant = None
            iopimplant_enc = None
        self.iopimplant = iopimplant
        if ionimplant is not None:
            try:
                space = tech.computed.min_space(ionimplant, active)
            except AttributeError:
                space = None
        else:
            space = None
        # Don't overlap implants
        if space is None:
            assert iopimplant_enc is not None
            space = iopimplant_enc.max()
        elif iopimplant_enc is not None:
            space = max(space, iopimplant_enc.max())
        self.min_space_ionimplant_active = space
        if iopimplant is not None:
            try:
                space = tech.computed.min_space(iopimplant, active)
            except AttributeError:
                space = None
        else:
            space = None
        # Don't overlap implants
        if space is None:
            assert ionimplant_enc is not None
            space = ionimplant_enc.max()
        elif ionimplant_enc is not None:
            space = max(space, ionimplant_enc.max())
        self.min_space_iopimplant_active = space

        # oxide
        oxidx = active.oxide.index(iomosgate.oxide)
        try:
            self.min_oxactive_space = tech.computed.min_space(active.in_(iomosgate.oxide))
        except AttributeError:
            self.min_oxactive_space = active.min_space
        oxenc = iomosgate.min_gateoxide_enclosure
        if oxenc is None:
            oxenc = _prp.Enclosure(tech.grid)
        self.iogateoxide_enclosure = oxenc
        # TODO: add active oxide enclosure
        oxext = oxenc.second
        oxenc = active.min_oxide_enclosure[oxidx]
        if oxenc is None:
            oxenc = _prp.Enclosure(tech.grid)
        self.activeoxide_enclosure = oxenc
        oxext = max((oxext, oxenc.max()))

        # min spacings for active
        min_space_active_poly = tech.computed.min_space(poly, active)
        space = max((
            active.min_space,
            nmos.computed.min_polyactive_extension + min_space_active_poly,
        ))
        if nmos.min_gateimplant_enclosure:
            space = max(
                space,
                nmos.min_gateimplant_enclosure[0].max() + self.min_space_nimplant_active,
            )
        if pimplant is not None:
            try:
                s = tech.computed.min_space(nmos.gate4mosfet, pimplant)
            except:
                pass
            else:
                space = max(space, s + self.min_space_nimplant_active)
        self.min_space_nmos_active = space
        space = max((
            active.min_space,
            pmos.computed.min_polyactive_extension + min_space_active_poly,
        ))
        if pmos.min_gateimplant_enclosure:
            space = max(
                space,
                pmos.min_gateimplant_enclosure[0].max() + self.min_space_pimplant_active,
            )
        if nimplant is not None:
            try:
                s = tech.computed.min_space(pmos.gate4mosfet, nimplant)
            except:
                pass
            else:
                space = max(space, s + self.min_space_pimplant_active)
        self.min_space_pmos_active = space
        min_space_iomosgate_active = (
            oxext + tech.computed.min_space(iomosgate.oxide, active)
        )
        space = max((
            active.min_space,
            ionmos.computed.min_polyactive_extension + min_space_active_poly,
            min_space_iomosgate_active,
        ))
        if ionmos.min_gateimplant_enclosure:
            space = max(
                space,
                ionmos.min_gateimplant_enclosure[0].max() + self.min_space_ionimplant_active,
            )
        if iopimplant is not None:
            try:
                s = tech.computed.min_space(ionmos.gate4mosfet, iopimplant)
            except:
                pass
            else:
                space = max(space, s + self.min_space_ionimplant_active)
        self.min_space_ionmos_active = space
        space = max((
            active.min_space,
            iopmos.computed.min_polyactive_extension + min_space_active_poly,
            min_space_iomosgate_active,
        ))
        if iopmos.min_gateimplant_enclosure:
            space = max(
                space,
                iopmos.min_gateimplant_enclosure[0].max() + self.min_space_iopimplant_active,
            )
        if ionimplant is not None:
            try:
                s = tech.computed.min_space(iopmos.gate4mosfet, ionimplant)
            except:
                pass
            else:
                space = max(space, s + self.min_space_iopimplant_active)
        self.min_space_iopmos_active = space
        vias = tuple(prims.__iter_type__(_prm.Via))
        metals = tuple(filter(
            lambda m: not isinstance(m, _prm.MIMTop),
            prims.__iter_type__(_prm.MetalWire),
        ))
        # One via below each metal => #vias == #metals
        assert len(vias) == len(metals)
        if framespec.top_metal is not None:
            idx = metals.index(framespec.top_metal)
            metals = metals[:(idx + 1)]
            vias = vias[:(idx + 1)]
        assert all(hasattr(metal, "pin") for metal in metals), "Unsupported configuration"
        self.vias = vias

        # Vias are sorted in the technology from bottom to top
        # so first via is the contact layer
        self.contact = contact = vias[0]
        assert (
            (active in contact.bottom) and (poly in contact.bottom)
            and (len(contact.top) == 1)
        ), "Unsupported configuration"

        actidx = contact.bottom.index(active)
        self.chact_enclosure = actenc = contact.min_bottom_enclosure[actidx]
        polyidx = contact.bottom.index(poly)
        self.chpoly_enclosure = polyenc = contact.min_bottom_enclosure[polyidx]
        self.chm1_enclosure = contact.min_top_enclosure[0]

        self.minwidth_activewithcontact = (
            contact.width + 2*actenc.min()
        )
        self.minwidth4ext_activewithcontact = (
            contact.width + 2*actenc.max()
        )

        self.minwidth_polywithcontact = (
            contact.width + 2*polyenc.min()
        )
        self.minwidth4ext_polywithcontact = (
            contact.width + 2*polyenc.max()
        )

        self.minnmos_contactgatepitch = (
            0.5*contact.width + nmos.computed.min_contactgate_space
            + 0.5*nmos.computed.min_l
        )
        self.minpmos_contactgatepitch = (
            0.5*contact.width + pmos.computed.min_contactgate_space
            + 0.5*pmos.computed.min_l
        )

        self.minionmos_contactgatepitch = (
            0.5*contact.width + ionmos.computed.min_contactgate_space
            + 0.5*ionmos.computed.min_l
        )
        self.miniopmos_contactgatepitch = (
            0.5*contact.width + iopmos.computed.min_contactgate_space
            + 0.5*iopmos.computed.min_l
        )

        self.nwell = nwell = pmos.well
        nwellidx = active.well.index(nwell)

        nactenc = active.min_substrate_enclosure.max()
        pactenc = active.min_well_enclosure[nwellidx].max()
        try:
            s = tech.computed.min_space(active, contact)
        except AttributeError:
            pass
        else:
            # Be sure that a poly contact can be put in between nmos and pmos
            if (nactenc + pactenc) < (contact.width + 2*s):
                # First make the two enclosures equal
                if pactenc < nactenc:
                    pactenc = nactenc
                else:
                    nactenc = pactenc
                # Then increase both if not enough yet
                if (nactenc + pactenc) < (contact.width + 2*s):
                    d = tech.on_grid(
                        0.5*((contact.width + 2*s) - (nactenc + pactenc)),
                        rounding="ceiling",
                    )
                    nactenc += d
                    pactenc += d
        self.activenwell_minspace = nactenc
        self.activenwell_minenclosure = pactenc

        ionactenc = nactenc
        if ionmos.min_gateimplant_enclosure:
            ionactenc = max(ionactenc, ionmos.min_gateimplant_enclosure[0].second)
        if pimplant is not None:
            try:
                s = tech.computed.min_space(ionmos.gate4mosfet, pimplant)
            except:
                pass
            else:
                ionactenc = max(ionactenc, s)
        iopactenc = pactenc
        if iopmos.min_gateimplant_enclosure:
            iopactenc = max(iopactenc, iopmos.min_gateimplant_enclosure[0].second)
        if nimplant is not None:
            try:
                s = tech.computed.min_space(iopmos.gate4mosfet, nimplant)
            except:
                pass
            else:
                iopactenc = max(iopactenc, s)

        nwellenc = active.min_well_enclosure[nwellidx].max()
        self.guardring_width = w = max(
            contact.width + contact.min_space,
            nwell.min_width - 2*nwellenc,
        )
        nwell_minspace = nwell.min_space
        if spec.nwell_minspace is not None:
            nwell_minspace = max(nwell_minspace, spec.nwell_minspace)
        s = max(
            pactenc + nactenc,
            0.5*(nwell_minspace + 2*pactenc - w), # Minimum NWELL spacing
        )
        self.guardring_space = 2*ceil(s/(2*tech.grid))*tech.grid
        self.guardring_pitch = self.guardring_width + self.guardring_space

        bottom = spec.iorow_height + 0.5*self.minwidth_activewithcontact + self.min_space_nmos_active
        top = spec.iorow_height + spec.corerow_pwell_height - nactenc
        self.maxnmos_w = w = tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxnmos_y = tech.on_grid(top - 0.5*w)
        self.maxnmos_activebottom = top - w
        self.maxnmos_activetop = top

        bottom = spec.iorow_height + spec.corerow_pwell_height + pactenc
        top = (
            spec.iorow_height + spec.corerow_height
            - (0.5*self.minwidth_activewithcontact + self.min_space_pmos_active)
        )
        self.maxpmos_w = w = tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxpmos_y = bottom + 0.5*w
        self.maxpmos_activebottom = bottom
        self.maxpmos_activetop = bottom + w

        bottom = spec.iorow_nwell_height + ionactenc
        top = (
            spec.iorow_height
            - (0.5*self.minwidth_activewithcontact + self.min_space_ionmos_active)
        )
        self.maxionmos_w = w = tech.on_grid(top - bottom,mult=2, rounding="floor")
        self.maxionmos_y = bottom + 0.5*w
        self.maxionmos_activebottom = bottom
        self.maxionmos_activetop = bottom + w

        bottom = 0.5*self.minwidth_activewithcontact + self.min_space_iopmos_active
        top = spec.iorow_nwell_height - iopactenc
        self.maxiopmos_w = tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxiopmos_y = tech.on_grid(
            0.5*self.minwidth_activewithcontact + self.min_space_iopmos_active
            + 0.5*self.maxiopmos_w,
        )
        self.maxiopmos_activebottom = tech.on_grid(self.maxiopmos_y - 0.5*self.maxiopmos_w)
        self.maxiopmos_activetop = tech.on_grid(self.maxiopmos_y + 0.5*self.maxiopmos_w)

        self.io_oxidebottom = (
            0.5*self.minwidth_activewithcontact
            + tech.computed.min_space(iomosgate.oxide, active)
        )
        self.io_oxidetop = (
            spec.iorow_height
            - 0.5*self.minwidth_activewithcontact
            - tech.computed.min_space(iomosgate.oxide, active)
        )

        # Also get dimensions of io transistor in the core row
        bottom = spec.iorow_height + 0.5*self.minwidth_activewithcontact + self.min_space_ionmos_active
        top = spec.iorow_height + spec.corerow_pwell_height - ionactenc
        self.maxionmoscore_w = w =  tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxionmoscore_y = top - 0.5*w
        self.maxionmoscore_activebottom = top - w
        self.maxionmoscore_activetop = top

        bottom = spec.iorow_height + spec.corerow_pwell_height + iopactenc
        top = (
            spec.iorow_height + spec.corerow_height
            - (0.5*self.minwidth_activewithcontact + self.min_space_iopmos_active)
        )
        self.maxiopmoscore_w = w = tech.on_grid(top - bottom, mult=2, rounding="floor")
        self.maxiopmoscore_y = bottom + 0.5*w
        self.maxiopmoscore_activebottom = bottom
        self.maxiopmoscore_activetop = bottom + w

        for via in vias[1:]:
            assert all((
                (len(via.bottom) == 1) or isinstance(via.bottom[0], _prm.MetalWire),
                (len(via.top) == 1) or isinstance(via.top[0], _prm.MetalWire),
            )), "Unsupported configuration"

        pads = tuple(tech.primitives.__iter_type__(_prm.PadOpening))
        assert len(pads) == 1
        self.pad = pads[0]

        # self.track_nsegments =
        # Don't start from 0; self.metal[1] corresponds with metal 1
        self.metal = {
            (i + 1): _MetalSpec(
                tech=tech, spec=spec, framespec=framespec, computed=self,
                metal=metal,
            )
            for i, metal in enumerate(metals)
        }

        self.track_metalspecs = tuple(self.metal[i] for i in range(3, (len(metals) + 1)))


class _IOCellFrame:
    """Default cells for in IO cell framework"""
    def __init__(self, *,
        fab: "IOFactory", framespec: IOFrameSpecification,
    ):
        self.fab = fab
        self.framespec = framespec
        tech = fab.tech
        comp = fab.computed

        active = comp.active
        actmaxpitch = framespec.acttracksegment_maxpitch
        actspace = framespec.acttracksegment_space

        self._pad = None # Only create pad first time it is accessed
        self._pad_bb: Dict[_prm.DesignMaskPrimitiveT, _geo.RectangularT] = {}
        self.__padpin_shape: Optional[_geo.Rect] = None

        track_segments: Dict[str, Tuple[_SegmentSpecification, ...]] = {
            track_name: track_spec.track_segments(
                tech=fab.tech, maxpitch=self.tracksegment_maxpitch,
            )
            for track_name, track_spec in framespec._track_specs_dict.items()
        }

        l_gd = fab.get_cell("GateDecode").layout
        assert l_gd.boundary is not None
        gd_height = l_gd.boundary.top - l_gd.boundary.bottom
        self.cells_y = cells_y = self.cell_height - gd_height

        l_ld = fab.get_cell("LevelDown").layout
        act_bb = l_ld.bounds(mask=active.mask)

        def act_segs(track_spec: TrackSpecification) -> Tuple[_SegmentSpecification, ...]:
            if actmaxpitch is None:
                return (
                    _SegmentSpecification(
                        bottom=track_spec.bottom,
                        top=track_spec.top,
                    ),
                )
            else:
                assert actspace is not None
                segs1 = track_spec.track_segments(tech=tech, maxpitch=actmaxpitch)
                segs2 = []
                for i, seg in enumerate(segs1):
                    # TODO: always ad/subtract space
                    bottom = seg.bottom + (0.0 if i == 0 else 0.5*actspace)
                    top = seg.top - (0.0 if i == (len(segs1) - 1) else 0.5*actspace)
                    segs2.append(_SegmentSpecification(bottom=bottom, top=top))
                return tuple(segs2)

        bottom = framespec._track_specs_dict["iovdd"].bottom
        top = cells_y + act_bb.bottom
        track_spec = TrackSpecification(name="temp", bottom=bottom, width=(top - bottom))
        track_segments["actiovss"] = act_segs(track_spec)

        track_spec = framespec._track_specs_dict["iovss"]
        track_segments["actiovdd"] = act_segs(track_spec)

        self._track_segments = track_segments

    @property
    def cell_height(self) -> float:
        return self.framespec.cell_height
    @property
    def monocell_width(self) -> float:
        return self.fab.spec.monocell_width
    @property
    def top_metal(self) -> Optional[_prm.MetalWire]:
        return self.framespec.top_metal
    @property
    def tracksegment_maxpitch(self) -> float:
        return self.framespec.tracksegment_maxpitch
    @property
    def tracksegment_space(self) -> Dict[Optional[_prm.MetalWire], float]:
        return self.framespec.tracksegment_space
    @property
    def tracksegment_viapitch(self) -> float:
        return self.framespec.tracksegement_viapitch
    @property
    def pad_width(self) -> float:
        return self.framespec.pad_width
    @property
    def pad_height(self) -> float:
        return self.framespec.pad_height
    @property
    def pad_y(self) -> float:
        return self.framespec.pad_y
    @property
    def pad_viapitch(self) -> Optional[float]:
        return self.framespec.pad_viapitch
    @property
    def pad_viacorner_distance(self) -> float:
        return self.framespec.pad_viacorner_distance
    @property
    def pad_viametal_enclosure(self) -> float:
        return self.framespec.pad_viametal_enclosure
    @property
    def padpin_height(self) -> float:
        return self.framespec.padpin_height
    @property
    def track_specs(self) -> Dict[str, TrackSpecification]:
        return self.framespec._track_specs_dict
    @property
    def has_secondiovss(self) -> bool:
        return self.framespec.has_secondiovss

    #
    # Pin support
    #

    def add_corepin(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt.CircuitNetT, m2_shape: _geo.RectangularT,
    ):
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed

        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        shape = _geo.Rect.from_rect(rect=m2_shape, top=self.cell_height)
        layouter.add_wire(net=net, wire=metal2, pin=metal2pin, shape=shape)

        if spec.add_corem3pins:
            metal2_spec = comp.metal[2]
            metal3_spec = comp.metal[3]
            metal3 = metal3_spec.prim
            via2 = comp.vias[2]

            w = m2_shape.width
            h = max(metal2_spec.minwidth4ext_updown, metal3_spec.minwidth4ext_updown)
            if (metal3.min_area is not None) and ((w*h + _geo.epsilon) < metal3.min_area):
                w = tech.on_grid(metal3.min_area/h, mult=2, rounding="ceiling")

            l_via2 = layouter.add_wire(
                net=net, wire=via2,
                x=m2_shape.center.x, bottom_width=w, top_width=w,
                y=(self.cell_height - 0.5*h), bottom_height=h, top_height=h,
            )
            m3_bb = l_via2.bounds(mask=metal3.mask)
            layouter.add_wire(net=net, wire=metal3, pin=metal3.pin, shape=m3_bb)

    def promote_m1instpin_to_corepin(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt.CircuitNetT, inst_layout: _lay.LayoutT,
        align: str,
    ):
        assert align in ("left", "center", "right"), "Internal error"

        fab = self.fab
        comp = fab.computed

        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        metal2 = comp.metal[2].prim
        via1 = comp.vias[1]

        m1pin_bounds = inst_layout.bounds(net=net, mask=metal1pin.mask, depth=1)
        _l_via1 = layouter.wire_layout(
            net=net, wire=via1, bottom_height=m1pin_bounds.height,
            bottom_enclosure="tall", top_enclosure="wide",
        )
        _m1_bounds = _l_via1.bounds(mask=metal1.mask)
        if align == "left":
            x = m1pin_bounds.right - _m1_bounds.right
        elif align == "center":
            x = m1pin_bounds.center.x
        elif align == "right":
            x = m1pin_bounds.left - _m1_bounds.left
        else:
            assert False, "Internal error"
        y = m1pin_bounds.top - _m1_bounds.top
        l_via = layouter.place(object_=_l_via1, x=x, y=y)
        self.add_corepin(
            layouter=layouter, net=net, m2_shape=l_via.bounds(mask=metal2.mask),
        )

    def promote_m2instpin_to_corepin(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt.CircuitNetT, inst_layout: _lay.LayoutT,
    ):
        fab = self.fab
        comp = fab.computed

        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        m2pin_bb = inst_layout.bounds(net=net, mask=metal2pin.mask, depth=1)
        self.add_corepin(layouter=layouter, net=net, m2_shape=m2pin_bb)

    #
    # IO track support
    #

    def add_track_nets(self, *, ckt: _ckt.CircuitT) -> Dict[
        str, _ckt._CircuitNet,
    ]:
        nets = {
            net_name: ckt.new_net(name=net_name, external=True)
            for net_name in ("vss", "vdd", "iovss", "iovdd")
        }
        return nets

    def add_trackconn_inst(self, *,
        ckt: _ckt._Circuit, width: float, connect_up: bool,
    ):
        fab = self.fab

        nets = ckt.nets

        trackconn_cell = fab.trackconn(width=width)
        inst = ckt.instantiate(trackconn_cell, name="trackconn")

        for net_name in ("vss", "vdd", "iovss", "iovdd"):
            nets[net_name].childports += inst.ports[net_name]

    def place_trackconn(self, *, layouter: _lay.CircuitLayouterT) -> _lay.LayoutT:
        ckt = layouter.circuit
        inst = ckt.instances.trackconn

        return layouter.place(inst, x=0.0, y=self.cells_y)

    def draw_tracks(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT,
        cell_width: Optional[float]=None,
        skip_top: Container[str]=(),
    ):
        spec = self.fab.spec
        nets = ckt.nets

        if cell_width is None:
            cell_width = spec.monocell_width

        # Draw tracks on higher metals
        self.draw_track(
            layouter=layouter, net=nets.iovss, cell_width=cell_width,
            track_segments=self._track_segments["iovss"],
            draw_top=("iovss" not in skip_top),
        )
        self.draw_track(
            layouter=layouter, net=nets.iovdd, cell_width=cell_width,
            track_segments=self._track_segments["iovdd"],
            draw_top=("iovdd" not in skip_top),
        )
        if self.has_secondiovss:
            self.draw_track(
                layouter=layouter, net=nets.iovss, cell_width=cell_width,
                track_segments=self._track_segments["secondiovss"],
                draw_top=("secondiovss" not in skip_top),
            )
        self.draw_duotrack(
            layouter=layouter, net1=nets.vss, net2=nets.vdd, cell_width=cell_width,
            track_segments=self._track_segments["vddvss"],
        )

    def draw_lowertracks(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT, cell_width: float,
        cells_only: bool,
    ) -> None:
        fab = self.fab
        comp = fab.computed

        nets = ckt.nets

        nwell = comp.nwell
        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        metal1 = comp.metal[1].prim

        self._draw_tracks_lowerlayers(ckt=ckt, layouter=layouter, cell_width=cell_width)

        if not cells_only:
            # iovss
            net = nets.iovss
            for segment in self._track_segments["actiovss"]:
                shape = _geo.Rect(left=0.0, bottom=segment.bottom, right=cell_width, top=segment.top)
                layouter.add_wire(net=net, wire=active, implant=pimplant, shape=shape)
                layouter.add_wire(net=net, wire=metal1, shape=shape)

            # iovdd
            net = nets.iovdd
            for segment in self._track_segments["actiovdd"]:
                shape = _geo.Rect(left=0.0, bottom=segment.bottom, right=cell_width, top=segment.top)
                layouter.add_wire(
                    net=net, wire=active, implant=nimplant, well=nwell, well_net=net,
                    shape=shape,
                )
                layouter.add_wire(net=net, wire=metal1, shape=shape)

    def draw_corner_tracks(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT,
    ):
        nets = ckt.nets

        self.draw_corner_track(
            layouter=layouter, net=nets.iovss,
            track_segments=self._track_segments["iovss"]
        )
        self.draw_corner_track(
            layouter=layouter, net=nets.iovdd,
            track_segments=self._track_segments["iovdd"]
        )
        if self.has_secondiovss:
            self.draw_corner_track(
                layouter=layouter, net=nets.iovss,
                track_segments=self._track_segments["secondiovss"]
            )
        self.draw_corner_duotrack(
            layouter=layouter, net1=nets.vss, net2=nets.vdd,
            track_segments=self._track_segments["vddvss"],
        )

        self._draw_cornertracks_lowerlayers(ckt=ckt, layouter=layouter)

    def draw_track(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt._CircuitNet, cell_width: float,
        track_segments: Tuple[_SegmentSpecification, ...],
        draw_top: bool=True,
    ):
        """drawn shapes on the track always stay half minimum space from the
        track edge. This means tracks can be defined without space in between
        them.
        """
        fab = self.fab
        comp = fab.computed

        specs = comp.track_metalspecs
        for n_metal, mspec in enumerate(specs if draw_top else specs[:-1]):
            space = mspec.tracksegment_space

            for segment_spec in track_segments:
                bottom = segment_spec.bottom + 0.5*space
                top = segment_spec.top - 0.5*space

                shape = _geo.Rect(left=0.0, bottom=bottom, right=cell_width, top=top)
                layouter.add_wire(net=net, wire=mspec.prim, pin=mspec.prim.pin, shape=shape)

                if n_metal < (len(comp.track_metalspecs) - (1 if draw_top else 2)): # Not top metal
                    via = mspec.top_via
                    mspec2 = comp.track_metalspecs[n_metal + 1]
                    space2 = mspec2.tracksegment_space

                    top_bottom = segment_spec.bottom + 0.5*space2
                    top_top = segment_spec.top - 0.5*space2

                    via_space = self.tracksegment_viapitch - via.width
                    if cell_width > 10*space: # Don't draw vias for small width
                        layouter.add_wire(
                            wire=via, net=net, space=via_space,
                            bottom_left=via_space, bottom_bottom=(bottom + via_space),
                            bottom_right=(cell_width - via_space), bottom_top=(top - via_space),
                            top_left=via_space, top_bottom=(top_bottom + via_space),
                            top_right=(cell_width - via_space), top_top=(top_top - via_space),
                        )

    def draw_duotrack(self, *,
        layouter: _lay.CircuitLayouterT, net1: _ckt._CircuitNet, net2: _ckt._CircuitNet,
        cell_width: float, track_segments: Tuple[_SegmentSpecification, ...],
    ):
        fab = self.fab
        tech = fab.tech

        prev_metal: Optional[_prm.MetalWire] = None
        prev_via: Optional[_prm.Via] = None
        prev_bottom_bottom: Optional[float] = None
        prev_bottom_top: Optional[float] = None
        prev_top_bottom: Optional[float] = None
        prev_top_top: Optional[float] = None
        for n, (
            bottom_net, top_net, metal, via, space,
            bottom_bottom, bottom_top, top_bottom, top_top,
        ) in enumerate(self._duotrack_iter(
            net1=net1, net2=net2, track_segments=track_segments,
        )):
            shape = _geo.Rect(left=0.0, bottom=bottom_bottom, right=cell_width, top=bottom_top)
            layouter.add_wire(net=bottom_net, wire=metal, pin=metal.pin, shape=shape)

            shape = _geo.Rect(left=0.0, bottom=top_bottom, right=cell_width, top=top_top)
            layouter.add_wire(net=top_net, wire=metal, pin=metal.pin, shape=shape)

            # Draw vias
            if n == 0:
                assert (prev_metal is None), "Internal error"
                assert (prev_via is None), "Internal error"
            elif cell_width > 10*space: # Only vias for wide cells
                # Draw via connection with prev_via
                assert prev_metal is not None
                assert prev_via is not None
                assert prev_bottom_bottom is not None
                assert prev_bottom_top is not None
                assert prev_top_bottom is not None
                assert prev_top_top is not None

                via_space = self.tracksegment_viapitch - prev_via.width

                if n == 1:
                    conn_width = tech.on_grid((cell_width - 2*space)/2, mult=2, rounding="floor")

                    via_bottommetal_width = tech.computed.min_width(
                        prev_metal, up=True, down=False, min_enclosure=True,
                    )
                    via_topmetal_width = tech.computed.min_width(
                        metal, up=False, down=True, min_enclosure=True,
                    )
                    ext = 0.5*via_bottommetal_width + 0.5*via_topmetal_width

                    layouter.add_wire(
                        wire=prev_via, net=bottom_net,
                        bottom_left=0.5*space,
                        bottom_bottom=prev_top_bottom,
                        bottom_right=(0.5*space + conn_width),
                        bottom_top=(prev_top_bottom + via_bottommetal_width),
                        bottom_enclosure="wide",
                        top_left=0.5*space,
                        top_bottom=bottom_top,
                        top_right=(0.5*space + conn_width),
                        top_top=(prev_top_bottom + ext),
                        top_enclosure="wide",
                    )
                    layouter.add_wire(
                        wire=prev_via, net=top_net,
                        bottom_left=(cell_width - 0.5*space - conn_width),
                        bottom_bottom=(prev_bottom_top - via_bottommetal_width),
                        bottom_right=(cell_width - 0.5*space),
                        bottom_top=prev_bottom_top,
                        bottom_enclosure="wide",
                        top_left=(cell_width - 0.5*space - conn_width),
                        top_bottom=(prev_bottom_top - ext),
                        top_right=(cell_width - 0.5*space),
                        top_top=top_bottom,
                        top_enclosure="wide",
                    )
                else:
                    layouter.add_wire(
                        wire=prev_via, net=bottom_net, space=via_space,
                        bottom_left=via_space,
                        bottom_bottom=(prev_bottom_bottom + via_space),
                        bottom_right=(cell_width - via_space),
                        bottom_top=(prev_bottom_top - via_space),
                        top_left=via_space, top_bottom=(bottom_bottom + via_space),
                        top_right=(cell_width - via_space), top_top=(bottom_top - via_space),
                    )

                    layouter.add_wire(
                        wire=prev_via, net=top_net, space=via_space,
                        bottom_left=via_space,
                        bottom_bottom=(prev_top_bottom + via_space),
                        bottom_right=(cell_width - via_space),
                        bottom_top=(prev_top_top - via_space),
                        top_left=via_space, top_bottom=(top_bottom + via_space),
                        top_right=(cell_width - via_space), top_top=(top_top - via_space),
                    )

            prev_metal = metal
            prev_via = via
            prev_bottom_bottom = bottom_bottom
            prev_bottom_top = bottom_top
            prev_top_bottom = top_bottom
            prev_top_top = top_top

    def draw_corner_track(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt._CircuitNet,
        track_segments: Tuple[_SegmentSpecification, ...],
    ):
        fab = self.fab
        comp = fab.computed

        pin_width = comp.track_metalspecs[0].tracksegment_space

        for mspec in comp.track_metalspecs:
            metal = mspec.prim
            space = mspec.tracksegment_space

            for segment_spec in track_segments:
                bottom = segment_spec.bottom + 0.5*space
                top = segment_spec.top - 0.5*space

                shape, pin1, pin2 = self._corner_segment(
                    bottom=bottom, top=top, pin_width=pin_width,
                )
                layouter.add_wire(net=net, wire=mspec.prim, shape=shape)
                layouter.add_wire(net=net, wire=metal, pin=metal.pin, shape=pin1)
                layouter.add_wire(net=net, wire=metal, pin=metal.pin, shape=pin2)

    def draw_corner_duotrack(self, *,
        layouter: _lay.CircuitLayouterT, net1: _ckt._CircuitNet, net2: _ckt._CircuitNet,
        track_segments: Tuple[_SegmentSpecification, ...],
    ):
        fab = self.fab
        comp = fab.computed

        pin_width = comp.track_metalspecs[0].tracksegment_space

        for (
            bottom_net, top_net, metal, _, _,
            bottom_bottom, bottom_top, top_bottom, top_top,
        ) in self._duotrack_iter(
            net1=net1, net2=net2, track_segments=track_segments,
        ):
            poly, pin1, pin2 = self._corner_segment(
                bottom=bottom_bottom, top=bottom_top, pin_width=pin_width,
            )
            layouter.add_wire(net=bottom_net, wire=metal, shape=poly)
            layouter.add_wire(net=bottom_net, wire=metal, pin=metal.pin, shape=pin1)
            layouter.add_wire(net=bottom_net, wire=metal, pin=metal.pin, shape=pin2)

            poly, pin1, pin2 = self._corner_segment(
                bottom=top_bottom, top=top_top, pin_width=pin_width,
            )
            layouter.add_wire(net=top_net, wire=metal, shape=poly)
            layouter.add_wire(net=top_net, wire=metal, pin=metal.pin, shape=pin1)
            layouter.add_wire(net=top_net, wire=metal, pin=metal.pin, shape=pin2)

    def _draw_tracks_lowerlayers(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT,
        cell_width: float,
    ) -> None:
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed

        nets = ckt.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        nwell = comp.nwell
        metal1 = comp.metal[1].prim

        acttap_width = tech.computed.min_width(
            active, up=True, down=False, min_enclosure=True,
        )
        m1tap_width = tech.computed.min_width(
            metal1, up=False, down=True, min_enclosure=True,
        )

        # iovdd
        net = nets.iovdd
        x = 0.5*cell_width
        y = self.cells_y
        l = layouter.add_wire(
            net=net, wire=active, implant=nimplant, well=nwell, well_net=net,
            x=x, y=y, width=cell_width, height=acttap_width,
        )
        nwell_bb = l.bounds(mask=nwell.mask)
        if nwell_bb.height < (nwell.min_width - _geo.epsilon):
            shape = _geo.Rect.from_rect(
                rect=nwell_bb,
                bottom=(nwell_bb.center.y - 0.5*nwell.min_width),
                top=(nwell_bb.center.y + 0.5*nwell.min_width),
            )
            layouter.add_wire(wire=nwell, net=net, shape=shape)

        layouter.add_wire(
            net=net, wire=metal1, x=x, y=y, width=cell_width, height=m1tap_width,
        )

        # vss
        net = nets.vss
        x = 0.5*cell_width
        y = self.cells_y + spec.iorow_height
        layouter.add_wire(
            net=net, wire=active, implant=pimplant,
            x=x, y=y, width=cell_width, height=acttap_width,
        )

        layouter.add_wire(
            net=net, wire=metal1, x=x, y=y, width=cell_width, height=m1tap_width,
        )

        # vdd
        net= nets.vdd
        x = 0.5*cell_width
        y = self.cells_y + spec.cells_height
        l = layouter.add_wire(
            net=net, wire=active, implant=nimplant, well=nwell, well_net=net,
            x=x, y=y, width=cell_width, height=acttap_width,
        )
        nwell_bb = l.bounds(mask=nwell.mask)
        if nwell_bb.height < (nwell.min_width - _geo.epsilon):
            shape = _geo.Rect.from_rect(
                rect=nwell_bb,
                bottom=(nwell_bb.center.y - 0.5*nwell.min_width),
                top=(nwell_bb.center.y + 0.5*nwell.min_width),
            )
            layouter.add_wire(wire=nwell, net=net, shape=shape)

        layouter.add_wire(
            net=net, wire=metal1, x=x, y=y, width=cell_width, height=m1tap_width,
        )

    def _draw_cornertracks_lowerlayers(self, *,
        ckt: _ckt._Circuit, layouter: _lay.CircuitLayouterT,
    ) -> None:
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed

        nets = ckt.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        nwell = comp.nwell
        metal1 = comp.metal[1].prim

        pin_width = tech.grid

        acttap_width = tech.computed.min_width(
            active, up=True, down=False, min_enclosure=True,
        )
        m1tap_width = tech.computed.min_width(
            # we don't use minimal width to work around possible 45deg minimal width
            # violations in the corner cell.
            metal1, up=True, down=True, min_enclosure=False,
        )

        layout = layouter.layout

        # iovss
        net = nets.iovss
        for segment in self._track_segments["actiovss"]:
            for net2, prim, shape in self._corner_active_segment(
                net=net, bottom=segment.bottom, top=segment.top,
                active=active, implant=pimplant, well=None,
            ):
                layout.add_shape(net=net2, layer=prim, shape=shape)
            shape, _, _ = self._corner_segment(
                bottom=segment.bottom, top=segment.top, pin_width=pin_width,
            )
            layouter.add_wire(net=net, wire=metal1, shape=shape)

        # iovdd
        net = nets.iovdd
        y = self.cells_y
        for net2, prim, shape in self._corner_active_segment(
            net=net, bottom=(y - 0.5*acttap_width), top=(y + 0.5*acttap_width),
            active=active, implant=nimplant, well=nwell,
        ):
            layout.add_shape(net=net2, layer=prim, shape=shape)
        shape, _, _ = self._corner_segment(
            bottom=(y - 0.5*m1tap_width), top=(y + 0.5*m1tap_width), pin_width=pin_width,
        )
        layouter.add_wire(net=net, wire=metal1, shape=shape)

        for segment in self._track_segments["actiovdd"]:
            for net2, prim, shape in self._corner_active_segment(
                net=net, bottom=segment.bottom, top=segment.top,
                active=active, implant=nimplant, well=nwell,
            ):
                layout.add_shape(net=net2, layer=prim, shape=shape)
            shape, _, _ = self._corner_segment(
                bottom=segment.bottom, top=segment.top, pin_width=pin_width,
            )
            layouter.add_wire(net=net, wire=metal1, shape=shape)

        # vss
        net = nets.vss
        y = self.cells_y + spec.iorow_height
        for net2, prim, shape in self._corner_active_segment(
            net=net, bottom=(y - 0.5*acttap_width), top=(y + 0.5*acttap_width),
            active=active, implant=pimplant, well=None,
        ):
            l = layout.add_shape(net=net2, layer=prim, shape=shape)
        shape, _, _ = self._corner_segment(
            bottom=(y - 0.5*m1tap_width), top=(y + 0.5*m1tap_width), pin_width=pin_width,
        )
        layouter.add_wire(net=net, wire=metal1, shape=shape)

        # vdd
        net= nets.vdd
        y = self.cells_y + spec.cells_height
        for net2, prim, shape in self._corner_active_segment(
            net=net, bottom=(y - 0.5*acttap_width), top=(y + 0.5*acttap_width),
            active=active, implant=nimplant, well=nwell,
        ):
            l = layout.add_shape(net=net2, layer=prim, shape=shape)
        shape, _, _ = self._corner_segment(
            bottom=(y - 0.5*m1tap_width), top=(y + 0.5*m1tap_width), pin_width=pin_width,
        )
        layouter.add_wire(net=net, wire=metal1, shape=shape)

    def _corner_segment(self, *,
        bottom: float, top: float, pin_width: float,
        ext: float=0.0,
    ) -> Tuple[_geo.Polygon, _geo.Polygon, _geo.Polygon]:
        fab = self.fab
        tech = fab.tech

        cell_height = self.cell_height

        d_top = tech.on_grid((cell_height - top)/_sqrt2)
        d_bottom = tech.on_grid(d_top + (top - bottom)/_sqrt2)

        if (d_top - _geo.epsilon) < pin_width:
            pin_width = d_top - tech.grid

        if d_top < _geo.epsilon:
            shape = _geo.Polygon.from_floats(points=(
                (ext, bottom),
                (-d_bottom, bottom),
                (-(cell_height - bottom), cell_height - d_bottom),
                (-(cell_height - bottom), cell_height + ext),
                (ext, cell_height + ext),
                (ext, bottom),
            ))
        else:
            shape = _geo.Polygon.from_floats(points=(
                (ext, bottom),
                (-d_bottom, bottom),
                (-(cell_height - bottom), cell_height - d_bottom),
                (-(cell_height - bottom), cell_height + ext),
                (-(cell_height - top), cell_height + ext),
                (-(cell_height - top), cell_height - d_top),
                (-d_top, top),
                (ext, top),
                (ext, bottom),
            ))

        pin1 = _geo.Rect(left=(ext - pin_width), bottom=bottom, right=ext, top=top)
        pin2 = _geo.Rect(
            left=(-cell_height + bottom), bottom=(cell_height + ext - pin_width),
            right=(-cell_height + top), top=(cell_height + ext),
        )

        return shape, pin1, pin2

    def _corner_active_segment(self, *,
        net: _ckt.CircuitNetT, bottom: float, top: float,
        active: _prm.WaferWire, implant: Optional[_prm.Implant], well: Optional[_prm.Well],
    ) -> Iterable[Tuple[Optional[_ckt.CircuitNetT], _prm.DesignMaskPrimitiveT, _geo.Polygon]]:
        fab = self.fab
        tech = fab.tech

        pin_width = tech.grid

        polygon, _, _ = self._corner_segment(bottom=bottom, top=top, pin_width=pin_width)
        yield net, active, polygon

        if implant is not None:
            idx = active.implant.index(implant)
            enc = active.min_implant_enclosure[idx]
            polygon, _, _ = self._corner_segment(
                bottom=(bottom - enc.second), top=(top + enc.second), ext=enc.first,
                pin_width=pin_width,
            )
            yield None, implant, polygon

        if well is not None:
            idx = active.well.index(well)
            enc = active.min_well_enclosure[idx]
            if (top - bottom + 2*enc.second + _geo.epsilon) > well.min_width:
                bottom2 = bottom - enc.second
                top2 = top + enc.second
            else:
                y = 0.5*(bottom + top)
                bottom2 = y - 0.5*well.min_width
                top2 = y + 0.5*well.min_width
            polygon, _, _ = self._corner_segment(
                bottom=bottom2, top=top2, ext=enc.first, pin_width=pin_width,
            )
            yield net, well, polygon

    def _duotrack_iter(self, *,
        net1: _ckt._CircuitNet, net2: _ckt._CircuitNet,
        track_segments: Tuple[_SegmentSpecification, ...],
    ) -> Iterable[Tuple[
        _ckt._CircuitNet, _ckt._CircuitNet, _prm.MetalWire, _prm.Via, float,
        float, float, float, float,
    ]]:
        fab = self.fab
        tech = fab.tech
        comp = fab.computed

        assert len(track_segments) == 2, "Internal error"
        bottom_segment = track_segments[0]
        top_segment = track_segments[1]

        prev_metal: Optional[_prm.MetalWire] = None
        for n_metal, mspec in enumerate(comp.track_metalspecs[:-1]):
            metal = mspec.prim
            top_via = mspec.top_via
            space = mspec.tracksegment_space

            # From second layer we exchange the nets
            bottom_net = net1 if (n_metal == 0) else net2
            top_net = net2 if (n_metal == 0) else net1

            bottom_bottom = bottom_segment.bottom + 0.5*space
            bottom_top = bottom_segment.top - 0.5*space

            top_bottom = top_segment.bottom + 0.5*space
            top_top = top_segment.top - 0.5*space

            # Smaller segments for second metal
            if n_metal == 1:
                assert prev_metal is not None

                prevmetal_width = tech.computed.min_width(
                    prev_metal, up=True, down=False, min_enclosure=True,
                )
                metal_width = tech.computed.min_width(
                    metal, up=False, down=True, min_enclosure=True,
                )
                dy = 0.5*prevmetal_width + 0.5*metal_width + space
                bottom_top -= dy
                top_bottom += dy

            yield (
                bottom_net, top_net, metal, top_via, space,
                bottom_bottom, bottom_top, top_bottom, top_top,
            )

            prev_metal = metal

    #
    # Pad support
    #

    @property
    def pad(self) -> "_FactoryCell":
        if not self.has_pad:
            raise AttributeError("No pad attribute as pad_height was not given")
        if self._pad is None:
            fab = self.fab
            self._pad = fab.pad(width=self.pad_width, height=self.pad_height)
        return self._pad
    @property
    def has_pad(self) -> bool:
        return hasattr(self, "pad_height")

    def pad_bb(self, *, prim: _prm.DesignMaskPrimitiveT) -> _geo.RectangularT:
        try:
            bb = self._pad_bb[prim]
        except KeyError:
            if self.has_pad:
                bb = self.pad.layout.bounds(mask=prim.mask).moved(
                    dxy=_geo.Point(x=0.5*self.monocell_width, y=self.pad_y),
                )
            else:
                bb = self._padpin_shape
            self._pad_bb[prim] = bb

        return bb

    def add_pad_inst(self, *, ckt: _ckt._Circuit, net: _ckt._CircuitNet):
        try:
            pad = self.pad
        except AttributeError:
            pass
        else:
            i_pad = ckt.instantiate(pad, name="pad")
            net.childports += i_pad.ports.pad

    def place_pad(self, *,
        layouter: _lay.CircuitLayouterT, net: _ckt._CircuitNet,
    ) -> _lay.LayoutT:
        fab = self.fab
        spec = fab.spec
        comp = fab.computed
        frame = fab.frame

        ckt = layouter.circuit
        insts = ckt.instances

        if self.has_pad:
            i_pad = insts.pad
            topmetal = comp.metal[len(comp.vias)].prim

            x = 0.5*spec.monocell_width
            l_pad = layouter.place(i_pad, x=x, y=frame.pad_y)
            pad_bounds = self.pad_bb(prim=topmetal)
            layouter.add_wire(net=net, wire=topmetal, pin=topmetal.pin, shape=pad_bounds)

            return l_pad
        else:
            # draw pin at the bottom
            l = layouter.fab.new_layout()

            pin_shape = self._padpin_shape

            for metalspec in (comp.metal[2], *comp.track_metalspecs):
                metal = metalspec.prim
                l += layouter.add_wire(
                    net=net, wire=metal, pin=metal.pin, shape=pin_shape,
                )
            for via in comp.vias[2:]:
                space = self.tracksegment_viapitch - via.width
                l += layouter.add_wire(
                    net=net, space=space, wire=via, bottom_shape=pin_shape, top_shape=pin_shape,
                )

            return l

    @property
    def _padpin_shape(self) -> _geo.Rect:
        if self.__padpin_shape is None:
            comp = self.fab.computed
            space = max(metalspec.tracksegment_space for metalspec in comp.track_metalspecs)
            self.__padpin_shape = _geo.Rect(
                left=space, bottom=0.0,
                right=(self.monocell_width - space), top=self.padpin_height,
            )
        return self.__padpin_shape

    #
    # clamp support
    #

    def add_clamp_nets(self, *,
        ckt: _ckt.CircuitT, add_n: bool=True, add_p: bool=True,
    ):
        if add_n:
            ckt.new_net(name="ngate", external=False)
        if add_p:
            ckt.new_net(name="pgate", external=False)

    def add_nclamp_inst(self, *,
        ckt: _ckt.CircuitT, n_trans: int, n_drive: int,
        pad: _ckt.CircuitNetT,
    ) -> None:
        fab = self.fab
        nets = ckt.nets

        c_clamp = fab.clamp(type_="n", n_trans=n_trans, n_drive=n_drive)
        i_clamp = ckt.instantiate(c_clamp, name="nclamp")
        nets.iovdd.childports += i_clamp.ports.iovdd
        nets.iovss.childports += i_clamp.ports.iovss
        pad.childports += i_clamp.ports.pad
        if n_drive > 0:
            nets.ngate.childports += i_clamp.ports.gate

    def add_pclamp_inst(self, *,
        ckt: _ckt.CircuitT, n_trans: int, n_drive: int,
        pad: _ckt.CircuitNetT,
    ) -> None:
        fab = self.fab
        nets = ckt.nets

        c_clamp = fab.clamp(type_="p", n_trans=n_trans, n_drive=n_drive)
        i_clamp = ckt.instantiate(c_clamp, name="pclamp")
        nets.iovdd.childports += i_clamp.ports.iovdd
        nets.iovss.childports += i_clamp.ports.iovss
        pad.childports += i_clamp.ports.pad
        if n_drive > 0:
            nets.pgate.childports += i_clamp.ports.gate

    def place_nclamp(self, *,
        layouter: _lay.CircuitLayouterT, pad: _ckt.CircuitNetT,
        connect_iovss: bool=False,
    ) -> _lay.LayoutT:
        fab = self.fab
        comp = fab.computed

        ckt = layouter.circuit
        nets = ckt.nets
        insts = ckt.instances

        layout = layouter.layout

        metal2 = comp.metal[2].prim

        iovss_trackspec = self.track_specs["iovss"]

        l_nclamp = layouter.place(insts.nclamp, x=0.0, y=iovss_trackspec.bottom)
        for polygon in self._pinpolygons(polygons=l_nclamp.polygons):
            layout.add_shape(net=nets.iovss, shape=polygon)

        pad_m2bb = self.pad_bb(prim=metal2)
        for polygon in l_nclamp.filter_polygons(net=pad, mask=metal2.pin.mask):
            # Iterate over bounds of individual shapes
            for bounds in _iterate_polygonbounds(polygon=polygon):
                shape = _geo.Rect.from_rect(
                    rect=bounds,
                    top=max(bounds.top, pad_m2bb.bottom),
                    bottom=min(bounds.bottom, pad_m2bb.top),
                )
                layouter.add_wire(wire=metal2, net=pad, shape=shape)

        if connect_iovss:
            tech = self.fab.tech

            max_pitch = self.tracksegment_maxpitch
            fingers = floor((self.pad_width + _geo.epsilon)/max_pitch) + 1
            pitch = tech.on_grid(self.pad_width/fingers, mult=2, rounding="floor")
            track_bottom = iovss_trackspec.bottom
            track_top = iovss_trackspec.top
            for metal_spec in comp.track_metalspecs[1:]:
                metal = metal_spec.prim
                space = metal_spec.tracksegment_space

                pad_bb = self.pad_bb(prim=metal)
                width = pitch - space
                bottom = min(track_bottom + 0.5*space, pad_bb.top)
                top = max(track_top - 0.5*space, pad_bb.bottom)
                for n in range(fingers):
                    if n < fingers - 1:
                        left = pad_bb.left + n*pitch + 0.5*space
                        right = left + width
                    else:
                        right = pad_bb.right - 0.5*space
                        left = right - width
                    shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
                    layouter.add_wire(net=pad, wire=metal, shape=shape)

        return l_nclamp

    def place_pclamp(self, *,
        layouter: _lay.CircuitLayouterT, pad: _ckt.CircuitNetT,
        connect_track: str="", connect_iovsstap: bool=False,
    ) -> _lay.LayoutT:
        assert (not connect_track) or (not connect_iovsstap), "Internal error"
        fab = self.fab
        frame = fab.frame
        comp = fab.computed

        ckt = layouter.circuit
        nets = ckt.nets
        insts = ckt.instances

        layout = layouter.layout

        metal1 = comp.metal[1].prim
        metal2 = comp.metal[2].prim
        metal3spec = comp.metal[3]
        via1 = comp.vias[1]
        via2 = comp.vias[2]

        iovdd_trackspec = self.track_specs["iovdd"]
        m3connect_bottom: Optional[float]
        m3connect_top: Optional[float]
        if not connect_track:
            m3connect_bottom = m3connect_top = None
        elif connect_track in ("secondiovss", "iovdd"):
            if connect_track == "secondiovss":
                trackspec = self.track_specs[connect_track]
                m3connect_bottom = trackspec.bottom + 0.5*metal3spec.tracksegment_space
                m3connect_top = trackspec.top - 0.5*metal3spec.tracksegment_space
            else:
                m3connect_bottom = m3connect_top = None
        elif connect_track in ("vss", "vdd"):
            # connect_trackspec = self.track_spec["vddvss"]
            connect_tracksegs = self._track_segments["vddvss"]
            assert len(connect_tracksegs) == 2
            trackseg = connect_tracksegs[0 if connect_track == "vss" else 1]
            m3connect_bottom = trackseg.bottom + 0.5*metal3spec.tracksegment_space
            m3connect_top = trackseg.top - 0.5*metal3spec.tracksegment_space
        else:
            raise RuntimeError(
                f"Internal error: unknown connect_track '{connect_track}'"
            )

        l_pclamp = layouter.place(insts.pclamp, x=0.0, y=iovdd_trackspec.bottom)
        for polygon in self._pinpolygons(polygons=l_pclamp.polygons):
            layout.add_shape(net=nets.iovdd, shape=polygon)

        pad_m2bb = self.pad_bb(prim=metal2)
        shape_args = {"bottom": pad_m2bb.top}
        if m3connect_top is not None:
            shape_args["top"] = m3connect_top
        elif connect_iovsstap:
            shape_args["top"] = frame._track_segments["actiovss"][-1].top
        for polygon in l_pclamp.filter_polygons(net=pad, mask=metal2.mask):
            # Iterate over bounds of individual shapes
            for bounds in _iterate_polygonbounds(polygon=polygon):
                shape = _geo.Rect.from_rect(rect=bounds, **shape_args)
                layouter.add_wire(wire=metal2, net=pad, shape=shape)

        if m3connect_bottom is not None:
            assert m3connect_top is not None, "Internal error"

            for polygon in l_pclamp.filter_polygons(
                net=pad, mask=metal2.mask, split=True,
            ):
                bounds = polygon.bounds
                layouter.add_wire(
                    wire=via2, net=pad,
                    bottom_left=bounds.left, bottom_right=bounds.right,
                    top_bottom=m3connect_bottom, top_top=m3connect_top,
                )

        if connect_track == "iovdd":
            fab = self.fab
            tech = fab.tech
            framespec = self.framespec

            net = nets.iovdd
            max_pitch = framespec.tracksegment_maxpitch
            fingers = floor((framespec.pad_width + _geo.epsilon)/max_pitch) + 1
            pitch = tech.on_grid(framespec.pad_width/fingers, mult=2, rounding="floor")
            track_top = iovdd_trackspec.top
            for metal_spec in comp.track_metalspecs[1:]:
                metal = metal_spec.prim
                space = metal_spec.tracksegment_space

                pad_bb = self.pad_bb(prim=metal)
                width = pitch - space
                top = track_top - 0.5*space
                bottom = pad_bb.top
                for n in range(fingers):
                    if n < fingers - 1:
                        left = pad_bb.left + n*pitch + 0.5*space
                        right = left + width
                    else:
                        right = pad_bb.right - 0.5*space
                        left = right - width
                    shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
                    layouter.add_wire(net=net, wire=metal, shape=shape)

        if connect_iovsstap:
            m1_top = frame._track_segments["actiovss"][-1].top
            clm1_bounds = l_pclamp.bounds(mask=metal1.mask)
            m1_bottom = clm1_bounds.top

            for polygon in l_pclamp.filter_polygons(
                net=pad, mask=metal2.mask, split=True,
            ):
                bounds = polygon.bounds
                layouter.add_wire(
                    wire=via1, net=pad,
                    top_left=bounds.left, top_right=bounds.right,
                    bottom_bottom=m1_bottom, bottom_top=m1_top,
                )

        return l_pclamp

    def _pinpolygons(self, *, polygons: Iterable[_geo.MaskShape]) -> Iterable[_geo.MaskShape]:
        trackmetalspecs = self.fab.computed.track_metalspecs
        trackpinmasks = tuple(spec.prim.pin.mask for spec in trackmetalspecs)

        return filter(lambda p: p.mask in trackpinmasks, polygons)

    def connect_clamp_wells(self, *,
        ckt: _ckt.CircuitT, layouter: _lay.CircuitLayouterT,
        nclamp_lay: _lay.LayoutT, pclamp_lay: _lay.LayoutT,
    ):
        nets = ckt.nets
        fab = self.fab
        comp = fab.computed

        width = self.monocell_width

        metal1 = comp.metal[1].prim
        metal2 = comp.metal[2].prim
        via1 = comp.vias[1]

        bottom = cast(_geo._Rectangular, nclamp_lay.boundary).top
        top = cast(_geo._Rectangular, pclamp_lay.boundary).bottom - comp.guardring_space
        _l_guardring = hlp.guardring(
            fab=fab, net=nets.iovss, type_="n",
            width=width, height=(top - bottom),
        )
        l_guardring = layouter.place(
            _l_guardring, x=0.5*width, y=0.5*(bottom + top),
        )
        guardringm1_bounds = l_guardring.bounds(mask=metal1.mask)
        viatop = guardringm1_bounds.top
        viay = viatop - 0.5*comp.metal[2].minwidth4ext_updown
        for polygon in pclamp_lay.filter_polygons(net=nets.iovdd, mask=metal2.mask):
            for bounds in _iterate_polygonbounds(polygon=polygon):
                l_via = layouter.add_wire(
                    net=nets.iovdd, wire=via1, y=viay,
                    top_left=bounds.left, top_right=bounds.right,
                )
                viam2_bounds = l_via.bounds(mask=metal2.mask)
                layouter.add_wire(net=nets.iovdd, wire=metal2, shape=_geo.Rect.from_rect(
                    rect=bounds, bottom=viam2_bounds.bottom,
                ))

    #
    # DCDiodes support
    #

    def add_dcdiodes_inst(self, *, ckt: _ckt.CircuitT, pad: _ckt.CircuitNetT) -> None:
        fab = self.fab
        spec = fab.spec

        if not spec.add_dcdiodes:
            return None
        else:
            if self.has_pad:
                raise NotImplementedError("DCDiodes with a pad")

        nets = ckt.nets

        iovdd = nets["iovdd"]
        iovss = nets["iovss"]

        ndio_cell = fab.dcdiode(type_="n")
        pdio_cell = fab.dcdiode(type_="p")

        ndio_inst = ckt.instantiate(ndio_cell, name="dcndiode")
        pdio_inst = ckt.instantiate(pdio_cell, name="dcpdiode")

        pad.childports += (ndio_inst.ports["cathode"], pdio_inst.ports["anode"])
        iovss.childports += (ndio_inst.ports["anode"], pdio_inst.ports["guard"])
        iovdd.childports += (ndio_inst.ports["guard"], pdio_inst.ports["cathode"])

    def place_dcdiodes(self, *,
        layouter: _lay.CircuitLayouterT, pad: _ckt.CircuitNetT,
        nclamp_lay: _lay.LayoutT, pclamp_lay: _lay.LayoutT,
    ) -> None:
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed

        if not spec.add_dcdiodes:
            return None

        ckt = layouter.circuit
        nets = ckt.nets
        insts = ckt.instances

        nwell = comp.nwell
        metal1 = comp.metal[1].prim
        metal2 = comp.metal[2].prim
        via1 = comp.vias[1]

        iovdd = nets["iovdd"]
        iovss = nets["iovss"]

        ndio_inst = insts["dcndiode"]
        pdio_inst = insts["dcpdiode"]

        bottom = cast(_geo._Rectangular, nclamp_lay.boundary).top
        top = cast(_geo._Rectangular, pclamp_lay.boundary).bottom - comp.guardring_space
        height = top - bottom

        # place the diodes
        _ndio_lay = layouter.inst_layout(inst=ndio_inst)
        _ndio_bb = _ndio_lay.boundary
        assert _ndio_bb is not None
        x = 0.5*self.monocell_width - _ndio_bb.center.x
        y = bottom + tech.on_grid(0.25*height) - _ndio_bb.center.y
        ndio_lay = layouter.place(_ndio_lay, x=x, y=y)

        _pdio_lay = layouter.inst_layout(inst=pdio_inst)
        _pdio_bb = _pdio_lay.boundary
        assert _pdio_bb is not None
        x = 0.5*self.monocell_width - _pdio_bb.center.x
        y = bottom + tech.on_grid(0.75*height) - _pdio_bb.center.y
        pdio_lay = layouter.place(_pdio_lay, x=x, y=y)

        # connect pad
        for pad_nclamp_m2poly in nclamp_lay.filter_polygons(
            net=pad, mask=metal2.pin.mask, depth=1, split=True,
        ):
            bb = pad_nclamp_m2poly.shape.bounds
            for pad_ndio_m1poly in ndio_lay.filter_polygons(
                net=pad, mask=metal1.pin.mask, depth=1, split=True,
            ):
                bb2 = pad_ndio_m1poly.shape.bounds
                if (bb2.left < bb.left) and (bb2.right > bb.right):
                    shape = _geo.Rect(
                        left=bb.left, bottom=bb2.bottom, right=bb.right, top=bb2.top,
                    )
                    layouter.add_wire(net=pad, wire=via1, bottom_shape=shape, top_shape=shape)

        for pad_pclamp_m2poly in pclamp_lay.filter_polygons(
            net=pad, mask=metal2.pin.mask, depth=1, split=True,
        ):
            bb = pad_pclamp_m2poly.shape.bounds
            for pad_pdio_m1poly in pdio_lay.filter_polygons(
                net=pad, mask=metal1.pin.mask, depth=1, split=True,
            ):
                bb2 = pad_pdio_m1poly.shape.bounds
                if (bb2.left < bb.left) and (bb2.right > bb.right):
                    shape = _geo.Rect(
                        left=bb.left, bottom=bb2.bottom, right=bb.right, top=bb2.top,
                    )
                    layouter.add_wire(net=pad, wire=via1, bottom_shape=shape, top_shape=shape)

        # connect iovss
        pclamp_botbb = None # get bottom bb pin of pclamp
        for iovss_pdio_m1poly in pdio_lay.filter_polygons(
            net=iovss, mask=metal1.pin.mask, depth=1, split=True,
        ):
            bb = iovss_pdio_m1poly.shape.bounds
            if (pclamp_botbb is None) or (bb.bottom < pclamp_botbb.bottom):
                pclamp_botbb = bb
        assert pclamp_botbb is not None

        for iovss_nclamp_m2poly in nclamp_lay.filter_polygons(
            net=iovss, mask=metal2.mask, depth=1, split=True,
        ):
            bb = iovss_nclamp_m2poly.shape.bounds
            for iovss_ndio_m1poly in ndio_lay.filter_polygons(
                net=iovss, mask=metal1.pin.mask, depth=1, split=True,
            ):
                bb2 = iovss_ndio_m1poly.shape.bounds
                if (bb2.left < bb.left) and (bb2.right > bb.right):
                    shape = _geo.Rect(
                        left=bb.left, bottom=bb2.bottom, right=bb.right, top=bb2.top,
                    )
                    layouter.add_wire(net=iovss, wire=via1, bottom_shape=shape, top_shape=shape)

                if (pclamp_botbb.left < bb.left) and (pclamp_botbb.right > bb.right):
                    shape = _geo.Rect(
                        left=bb.left, bottom=pclamp_botbb.bottom, right=bb.right, top=pclamp_botbb.top,
                    )
                    layouter.add_wire(net=iovss, wire=via1, bottom_shape=shape, top_shape=shape)

                    shape = _geo.Rect.from_rect(rect=shape, bottom=bb.top)
                    layouter.add_wire(net=iovss, wire=metal2, shape=shape)

        # connect iovdd
        for iovdd_pclamp_m2poly in pclamp_lay.filter_polygons(
            net=iovdd, mask=metal2.mask, depth=1, split=True,
        ):
            bb = iovdd_pclamp_m2poly.shape.bounds
            for iovdd_pdio_m1poly in pdio_lay.filter_polygons(
                net=iovdd, mask=metal1.pin.mask, depth=1, split=True,
            ):
                bb2 = iovdd_pdio_m1poly.shape.bounds
                if (bb2.left < bb.left) and (bb2.right > bb.right):
                    shape = _geo.Rect(
                        left=bb.left, bottom=bb2.bottom, right=bb.right, top=bb2.top,
                    )
                    layouter.add_wire(net=iovdd, wire=via1, bottom_shape=shape, top_shape=shape)

                    shape = _geo.Rect.from_rect(rect=shape, top=bb.bottom)
                    layouter.add_wire(net=iovdd, wire=metal2, shape=shape)

        m1bb = ndio_lay.bounds(mask=metal1.mask)
        for shape in (
            _geo.Rect(left=0.0, bottom=bottom, top=m1bb.top, right=m1bb.left),
            _geo.Rect(left=m1bb.left, bottom=bottom, top=m1bb.bottom, right=m1bb.right),
            _geo.Rect(left=m1bb.right, bottom=bottom, top=m1bb.top, right=self.monocell_width),
        ):
            layouter.add_wire(net=iovdd, wire=metal1, shape=shape)

        nwbb = ndio_lay.bounds(mask=nwell.mask)
        for shape in (
            _geo.Rect(left=0.0, bottom=bottom, top=nwbb.top, right=nwbb.left),
            _geo.Rect(left=nwbb.left, bottom=bottom, top=nwbb.bottom, right=nwbb.right),
            _geo.Rect(left=nwbb.right, bottom=bottom, top=nwbb.top, right=self.monocell_width),
        ):
            layouter.add_wire(net=iovdd, wire=nwell, shape=shape)


class _FactoryCell(_fab.FactoryCell["IOFactory"]):
    pass
FactoryCellT = _FactoryCell
class _FactoryOnDemandCell(_FactoryCell, _fab.FactoryOnDemandCell["IOFactory"]):
    pass


class _GuardRing(_FactoryCell):
    def __init__(self, *, name, fab, type_, width, height, fill_well, fill_implant):
        super().__init__(fab=fab, name=name)
        ckt = self.new_circuit()
        conn = ckt.new_net(name="conn", external=True)
        layouter = self.new_circuitlayouter()

        l = hlp.guardring(
            fab=fab, net=conn, type_=type_, width=width, height=height,
            fill_well=fill_well, fill_implant=fill_implant,
        )
        layouter.place(l, x=0.0, y=0.0)
        self.layout.boundary = l.boundary


class _Clamp(_FactoryCell):
    def __init__(self, *,
        name: str, fab: "IOFactory", type_: str, n_trans: int, n_drive: int,
    ):
        assert (
            (type_ in ("n", "p")) and (n_trans > 0) and (0 <= n_drive <= n_trans)
        ), "Internal error"
        spec = fab.spec
        tech = fab.tech
        comp = fab.computed

        nwell = comp.nwell
        cont = comp.contact
        metal1 = comp.metal[1].prim
        via1 = comp.vias[1]
        metal2 = comp.metal[2].prim
        via2 = comp.vias[2]

        super().__init__(fab=fab, name=name)

        ckt = self.new_circuit()
        layouter = self.new_circuitlayouter()
        layoutfab = layouter.fab

        iovss = ckt.new_net(name="iovss", external=True)
        iovdd = ckt.new_net(name="iovdd", external=True)
        source = iovss if type_ == "n" else iovdd
        notsource = iovdd if type_ == "n" else iovss
        pad = ckt.new_net(name="pad", external=True)

        gate_nets = tuple()
        gate: Optional[_ckt._CircuitNet] = None
        off: Optional[_ckt._CircuitNet] = None
        if n_drive > 0:
            gate = ckt.new_net(name="gate", external=True)
            gate_nets += n_drive*(gate,)
        if n_drive < n_trans:
            off = ckt.new_net(name="off", external=False)
            gate_nets += (n_trans - n_drive)*(off,)

        _l_clamp = hlp.clamp(
            fab=fab, ckt=ckt, type_=type_,
            source_net=source, drain_net=pad, gate_nets=gate_nets,
        )
        clampact_bounds = _l_clamp.bounds(mask=comp.active.mask)

        min_space_active_poly = tech.computed.min_space(comp.poly, comp.active)

        vspace = (
            spec.clampgate_gatecont_space + 0.5*cont.width + max(
                0.5*comp.minwidth_polywithcontact + min_space_active_poly,
                0.5*comp.metal[1].minwidth4ext_down + metal1.min_space,
            )
        )
        innerguardring_height = (
            (clampact_bounds.top - clampact_bounds.bottom) + 2*vspace
            + 2*comp.guardring_width
        )
        innerguardring_width = (spec.monocell_width - 2*comp.guardring_pitch)
        outerguardring_height = innerguardring_height + 2*comp.guardring_pitch

        c_outerring = fab.guardring(
            type_=type_, width=spec.monocell_width, height=outerguardring_height,
        )
        i_outerring = ckt.instantiate(c_outerring, name="OuterRing")
        notsource.childports += i_outerring.ports.conn
        c_innerring = fab.guardring(
            type_="p" if (type_ == "n") else "n",
            width=innerguardring_width, height=innerguardring_height,
            fill_well=(type_ == "p"), fill_implant=(not spec.add_clampsourcetap),
        )
        i_innerring = ckt.instantiate(c_innerring, name="InnerRing")
        source.childports += i_innerring.ports.conn

        # Place clamp, guard rings
        x = 0.5*spec.monocell_width
        y = 0.5*outerguardring_height
        layouter.place(i_outerring, x=x, y=y)
        layouter.place(i_innerring, x=x, y=y)
        l_clamp = layouter.place(_l_clamp, x=x, y=y)

        # Draw drain metal2 connections
        for ms in l_clamp.filter_polygons(net=pad, mask=metal1.mask, split=True):
            bounds = ms.shape.bounds
            l_via = layouter.add_wire(
                net=pad, wire=via1, x=bounds.center.x, columns=spec.clampdrain_via1columns,
                bottom_bottom=bounds.bottom, bottom_top=bounds.top,
            )
            viam2_bounds = l_via.bounds(mask=metal2.mask)

            shape = _geo.Rect.from_rect(
                rect=viam2_bounds, top=outerguardring_height,
            )
            layouter.add_wire(net=pad, wire=metal2, pin=metal2.pin, shape=shape)

        # Connect source to ring
        # Cache as polygons will be added during parsing
        for ms in l_clamp.filter_polygons(net=source, mask=metal1.mask, split=True):
            bounds = ms.shape.bounds
            x = bounds.center.x

            l_via = layouter.add_wire(
                net=source, wire=via1, x=x,
                bottom_bottom=bounds.bottom, bottom_top=bounds.top,
            )
            viam2_bounds = l_via.bounds(mask=metal2.mask)

            bottom = 0.5*outerguardring_height - 0.5*innerguardring_height
            top = bottom + comp.guardring_width
            layouter.add_wire(
                net=source, wire=via1, x=x,
                bottom_bottom=bottom, bottom_top=top,
            )
            top = 0.5*outerguardring_height + 0.5*innerguardring_height
            bottom = top - comp.guardring_width
            layouter.add_wire(
                net=source, wire=via1, x=x,
                bottom_bottom=bottom, bottom_top=top,
            )
            shape = _geo.Rect.from_rect(
                rect=viam2_bounds,
                bottom=0.0, top=outerguardring_height,
            )
            layouter.add_wire(net=source, wire=metal2, shape=shape)
            layouter.add_wire(
                net=source, wire=via2, x=x,
                bottom_bottom=0.0, bottom_top=outerguardring_height,
            )

        # Draw gate diode and connect the gates
        if n_drive > 0:
            assert gate is not None
            diode = spec.ndiode if type_ == "n" else spec.pdiode
            well_args = {} if type_ == "n" else {"well_net": iovdd, "bottom_well": nwell}
            l_ch = layoutfab.layout_primitive(
                prim=cont, portnets={"conn": gate}, **well_args, rows=2,
                bottom=diode.wire, bottom_implant=diode.implant,
            )
            chact_bounds = l_ch.bounds(mask=diode.wire.mask)
            dgate = ckt.instantiate(diode, name="DGATE",
                width=(chact_bounds.right - chact_bounds.left),
                height=(chact_bounds.top - chact_bounds.bottom),
            )
            an = dgate.ports.anode
            cath = dgate.ports.cathode
            gate.childports += an if type_ == "p" else cath
            source.childports += an if type_ == "n" else cath

            x = tech.on_grid(0.5*spec.monocell_width + 0.5*(
                clampact_bounds.left - 0.5*innerguardring_width + comp.guardring_width
            ))
            y = 0.5*outerguardring_height + clampact_bounds.top - chact_bounds.top
            l_ch = layouter.place(l_ch, x=x, y=y)
            layouter.place(dgate, x=x, y=y)

            chm1_bounds = l_ch.bounds(mask=metal1.mask)
            clampm1gate_bounds = l_clamp.bounds(mask=metal1.mask, net=gate)

            rect = _geo.Rect.from_rect(
                rect=chm1_bounds, top=clampm1gate_bounds.top,
            )
            layouter.add_wire(wire=metal1, net=gate, shape=rect)
            rect = _geo.Rect.from_rect(
                rect=clampm1gate_bounds, left=chm1_bounds.left,
                bottom=(clampm1gate_bounds.top - metal1.min_width),
            )
            layouter.add_wire(wire=metal1, net=gate, shape=rect)

            bottom = chm1_bounds.bottom
            top = clampm1gate_bounds.top
            l_via = layouter.add_wire(
                wire=via1, net=gate, x=x,
                bottom_bottom=bottom, bottom_top=top,
            )
            viam2_bounds = l_via.bounds(mask=metal2.mask)
            shape = _geo.Rect.from_rect(rect=viam2_bounds, top=outerguardring_height)
            layouter.add_wire(wire=metal2, net=gate, pin=metal2.pin, shape=shape)

        # Draw power off resistor and connect the gates
        if n_drive < n_trans:
            assert off is not None
            res = spec.nres if type_ == "n" else spec.pres
            w = max(res.min_width, comp.minwidth4ext_polywithcontact)
            # Make resistor poly as high as the active of the clamp transistor
            assert res.min_contact_space is not None
            h = (
                (clampact_bounds.top - clampact_bounds.bottom)
                - comp.minwidth_polywithcontact - cont.width - 2*res.min_contact_space
            )
            roff = ckt.instantiate(res, name="Roff", width=w, length=h)
            source.childports += roff.ports.port1
            off.childports += roff.ports.port2

            x = tech.on_grid(0.5*spec.monocell_width + 0.5*(
                clampact_bounds.right + 0.5*innerguardring_width - comp.guardring_width
            ))
            y = 0.5*outerguardring_height
            l_roff = layouter.place(roff, x=x, y=y)
            roffm1source_bounds = l_roff.bounds(mask=metal1.mask, net=source)
            roffm1off_bounds = l_roff.bounds(mask=metal1.mask, net=off)

            # Possibly extend implant if it is the same implant as the guard ring
            guard_impl = comp.pimplant if type_ == "n" else comp.nimplant
            if (guard_impl is not None) and (guard_impl in res.implant):
                roffimpl_bounds = l_roff.bounds(mask=guard_impl.mask)
                shape = _geo.Rect.from_rect(
                    rect=roffimpl_bounds,
                    bottom=(0.5*outerguardring_height - 0.5*innerguardring_height),
                    top=(0.5*outerguardring_height + 0.5*innerguardring_height),
                )
                layouter.add_portless(prim=guard_impl, shape=shape)

            x = roffm1source_bounds.center.x
            y = roffm1source_bounds.center.y
            l_via = layouter.add_wire(
                wire=via1, net=source, x=x, y=y, columns=2,
            )
            viam2_bounds = l_via.bounds(mask=metal2.mask)
            y = comp.guardring_pitch + 0.5*comp.guardring_width
            l_via = layouter.add_wire(
                wire=via1, net=source, x=x, y=y, columns=2,
            )
            viam2_bounds2 = l_via.bounds(mask=metal2.mask)
            shape = _geo.Rect.from_rect(rect=viam2_bounds, bottom=viam2_bounds2.bottom)
            layouter.add_wire(wire=metal2, net=source, shape=shape)

            clampm1off_bounds = l_clamp.bounds(mask=metal1.mask, net=off)
            roffm1off_bounds = l_roff.bounds(mask=metal1.mask, net=off)

            rect = _geo.Rect.from_rect(
                rect=roffm1off_bounds, top=clampm1off_bounds.top,
            )
            layouter.add_wire(wire=metal1, net=off, shape=rect)
            shape = _geo.Rect.from_rect(
                rect=clampm1off_bounds,
                bottom=(clampm1off_bounds.top - metal1.min_width),
                right=roffm1off_bounds.right,
            )
            layouter.add_wire(wire=metal1, net=off, shape=shape)

        self.layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0,
            right=spec.monocell_width, top=outerguardring_height,
        )


class _DCDiode(_FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: "IOFactory", type_: str):
        # This diode is rotated to make it larger in the X direction
        spec = fab.spec
        assert spec.add_dcdiodes, "Internal error"

        assert type_ in ("n", "p"), "Internal error"
        self.type_ = type_

        super().__init__(fab=fab, name=name)

    def _create_circuit(self) -> None:
        fab = self.fab
        spec = fab.spec

        ckt = self.new_circuit()
        type_ = self.type_
        fingers = spec.dcdiode_fingers
        dio = spec.ndiode if type_ == "n" else spec.pdiode

        anode = ckt.new_net(name="anode", external=True)
        cathode = ckt.new_net(name="cathode", external=True)
        ckt.new_net(name="guard", external=True)

        width = spec.dcdiode_inneractheight
        height = spec.dcdiode_actwidth
        for i in range(fingers):
            dio_inst = ckt.instantiate(dio,
                name=self._diode_name(n=i), width=width, height=height,
            )
            anode.childports += dio_inst.ports.anode
            cathode.childports += dio_inst.ports.cathode

    def _create_layout(self) -> None:
        # We rotate the diode
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        type_ = self.type_
        active = comp.active
        cont = comp.contact
        metal1 = comp.metal[1].prim

        ckt = self.circuit
        nets = ckt.nets
        insts = ckt.instances

        guard = nets["guard"]

        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        innerwidth = spec.dcdiode_inneractheight
        innerheight = spec.dcdiode_actwidth
        actwidth = spec.dcdiode_actwidth
        actspace = spec.dcdiode_actspace
        actspace_end = spec.dcdiode_actspace_end
        fingers = spec.dcdiode_fingers

        actpitch = actwidth + actspace

        outerwidth = innerwidth + 2*(actspace_end + actwidth)
        outerheight = actwidth + 2*fingers*actpitch

        d_guard = spec.dcdiode_diodeguardspace + comp.guardring_width
        guardwidth = outerwidth + 2*d_guard
        guardheight = outerheight + 2*d_guard

        if type_ == "n":
            dio_net = nets["cathode"]
            outer_net = nets["anode"]
            outer_impl = comp.pimplant
            well = None
            well_net = None
        else:
            dio_net = nets["anode"]
            outer_net = nets["cathode"]
            outer_impl = comp.nimplant
            well = comp.nwell
            well_net = outer_net

        for i in range(fingers):
            dio_inst = insts[self._diode_name(n=i)]
            x = 0.5*outerwidth
            y = actpitch + 2*i*actpitch + 0.5*innerheight
            dio_lay = layouter.place(dio_inst, x=x, y=y)
            dio_actbb = dio_lay.bounds(mask=active.mask)

            layouter.add_wire(
                net=dio_net, wire=cont, bottom=active, bottom_shape=dio_actbb,
                top_shape=dio_actbb,
            )
            layouter.add_wire(net=dio_net, wire=metal1, pin=metal1.pin, shape=dio_actbb)

        idx = cont.bottom.index(active)
        enc = cont.min_bottom_enclosure[idx]
        hor_enc = _prp.Enclosure((max(enc.max(), cont.min_space), enc.min()))

        # guard contacts
        # left
        bottom = 0.0
        top = outerheight
        left = 0.0
        right = left + actwidth
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(
            net=outer_net, wire=cont, well_net=well_net,
            bottom=active, bottom_shape=shape, bottom_implant=outer_impl,
            bottom_well=well,
            top_shape=shape,
        )
        # right
        right = outerwidth
        left = right - actwidth
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(
            net=outer_net, wire=cont, well_net=well_net,
            bottom=active, bottom_shape=shape, bottom_implant=outer_impl,
            bottom_well=well,
            top_shape=shape,
        )
        # fingers
        left = actwidth
        right = outerwidth - actwidth
        for i in range(fingers + 1):
            bottom = 2*i*actpitch
            top = bottom + actwidth
            shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
            layouter.add_wire(
                net=outer_net, wire=cont, well_net=well_net,
                bottom=active, bottom_shape=shape, bottom_implant=outer_impl,
                bottom_enclosure=hor_enc, bottom_well=well,
                top_shape=shape,
            )
            shape = _geo.Rect.from_rect(rect=shape, left=0.0, right=outerwidth)
            layouter.add_wire(net=outer_net, wire=metal1, pin=metal1.pin, shape=shape)

        if well is not None:
            assert well_net is not None
            bb = layout.bounds(mask=well.mask)
            layouter.add_wire(net=well_net, wire=well, shape=bb)

        guard_cell = fab.guardring(type_=type_, width=guardwidth, height=guardheight)
        guard_inst = ckt.instantiate(guard_cell, name="guard")
        guard.childports += guard_inst.ports["conn"]
        x = -d_guard + 0.5*guardwidth
        y = -d_guard + 0.5*guardheight
        guard_lay = layouter.place(guard_inst, x=x, y=y)

        bnd = guard_lay.boundary
        assert bnd is not None
        if spec.dcdiode_indicator is not None:
            layouter.add_portless(prim=spec.dcdiode_indicator, shape=bnd)
        layout.boundary = bnd

        shape = _geo.Rect.from_rect(rect=bnd, top=(bnd.bottom + comp.guardring_width))
        layouter.add_wire(net=guard, wire=metal1, pin=metal1.pin, shape=shape)
        shape = _geo.Rect.from_rect(rect=bnd, bottom=(bnd.top - comp.guardring_width))
        layouter.add_wire(net=guard, wire=metal1, pin=metal1.pin, shape=shape)

    def _diode_name(self, *, n: int) -> str:
        # Get diode name
        fingers = self.fab.spec.dcdiode_fingers

        assert 0 <= n < fingers, "Internal error"

        return "dcdiode" if fingers == 1 else f"dcdiode[{n}]"

class _Secondary(_FactoryCell):
    def __init__(self, *, fab: "IOFactory"):
        spec = fab.spec
        comp = fab.computed

        cont = comp.contact
        pimplant = comp.pimplant
        metal1 = comp.metal[1].prim
        via1 = comp.vias[1]
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        super().__init__(fab=fab, name="SecondaryProtection")

        ckt = self.new_circuit()
        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        iovdd = ckt.new_net(name="iovdd", external=True)
        iovss = ckt.new_net(name="iovss", external=True)
        pad = ckt.new_net(name="pad", external=True)
        core = ckt.new_net(name="core", external=True)

        # Resistance
        r = ckt.instantiate(
            spec.nres, name="R",
            width=spec.secondres_width, length=spec.secondres_length,
        )
        pad.childports += r.ports.port1
        core.childports += r.ports.port2

        l_res = layouter.inst_layout(inst=r)
        respoly_bounds = l_res.bounds(mask=comp.poly.mask)
        res_width = respoly_bounds.right - respoly_bounds.left
        res_height = respoly_bounds.top - respoly_bounds.bottom

        guard_width = (
            res_width + 2*spec.secondres_active_space + 2*comp.guardring_width
        )
        guard_height = (
            res_height + 2*spec.secondres_active_space + 2*comp.guardring_width
        )
        l_guard = hlp.guardring(
            fab=fab, net=iovss, type_="p", width=guard_width, height=guard_height,
        )

        l_res = layouter.place(l_res, x=0.5*guard_width, y=0.5*guard_height)
        resm1pad_bounds = l_res.bounds(mask=metal1.mask, net=pad)
        resm1core_bounds = l_res.bounds(mask=metal1.mask, net=core)
        l_guard = layouter.place(l_guard, x=0.5*guard_width, y=0.5*guard_height)
        resm1guard_bounds = l_guard.bounds(mask=metal1.mask)

        # if resistor has p implant draw pimplant over whole inner area
        if (pimplant is not None) and (pimplant in spec.nres.implant):
            shape = _geo.Rect(left=0.0, bottom=0.0, right=guard_width, top=guard_height)
            layouter.add_portless(prim=pimplant, shape=shape)

        # N diode
        dn_prim = spec.ndiode
        diode_height = (
            guard_height - 2*comp.guardring_width - 2*comp.min_space_nmos_active
        )
        l_ch = layouter.fab.layout_primitive(
            cont, portnets={"conn": core}, columns=2,
            bottom=dn_prim.wire, bottom_implant=dn_prim.implant,
            bottom_height=diode_height,
        )
        dnchact_bounds = l_ch.bounds(mask=comp.active.mask)
        diode_width = dnchact_bounds.right - dnchact_bounds.left
        dn = ckt.instantiate(
            dn_prim, name="DN", width=diode_width, height=diode_height,
        )
        core.childports += dn.ports.cathode
        iovss.childports += dn.ports.anode

        guard2_width = (
            diode_width + 2*comp.min_space_nmos_active + 2*comp.guardring_width
        )
        l_guard2 = hlp.guardring(
            fab=fab, net=iovss, type_="p", width=guard2_width, height=guard_height,
        )

        x = guard_width + comp.guardring_space + 0.5*guard2_width
        y = 0.5*guard_height
        l_dn_ch = layouter.place(l_ch, x=x, y=y)
        layouter.place(dn, x=x, y=y)
        l_guard2 = layouter.place(l_guard2, x=x, y=y)
        ndiom1guard_bounds = l_guard2.bounds(mask=metal1.mask)

        # connect guard rings
        # currently can't be done in metal1 as no shapes with two or more holes
        # in it are supported.
        _l_via = layouter.fab.layout_primitive(
            via1, portnets={"conn": iovss}, rows=3,
        )
        _m1_bounds = _l_via.bounds(mask=metal1.mask)
        y = (
            max(resm1guard_bounds.bottom, ndiom1guard_bounds.bottom)
            - _m1_bounds.bottom + 2*metal2.min_space
        )
        l = layouter.place(
            _l_via, x=(resm1guard_bounds.right - _m1_bounds.right), y=y,
        )
        m2_bounds1 = l.bounds(mask=metal2.mask)
        l = layouter.place(
            _l_via, x=(ndiom1guard_bounds.left - _m1_bounds.left), y=y,
        )
        m2_bounds2 = l.bounds(mask=metal2.mask)
        shape = _geo.Rect.from_rect(
            rect=m2_bounds1, right=m2_bounds2.right, top=m2_bounds2.top,
        )
        layouter.add_wire(net=iovss, wire=metal2, pin=metal2pin, shape=shape)

        # P diode
        dp_prim = spec.pdiode
        guard3_width = (
            guard_width + comp.guardring_space + guard2_width
        )
        diode2_width = (
            guard3_width - 2*comp.guardring_width - 2*comp.min_space_pmos_active
        )
        l_ch = layouter.fab.layout_primitive(
            cont, portnets={"conn": core}, rows=2,
            bottom=dp_prim.wire, bottom_implant=dp_prim.implant,
            bottom_width=diode2_width,
        )
        dpchact_bounds = l_ch.bounds(mask=comp.active.mask)
        diode2_height = dpchact_bounds.top - dpchact_bounds.bottom
        dp = ckt.instantiate(
            dp_prim, name="DP", width=diode2_width, height=diode2_height,
        )
        core.childports += dp.ports.anode
        iovdd.childports += dp.ports.cathode

        guard3_height = (
            diode2_height + 2*comp.min_space_pmos_active + 2*comp.guardring_width
        )
        l_guard3 = hlp.guardring(
            fab=fab, net=iovdd, type_="n", width=guard3_width, height=guard3_height,
            fill_well=True,
        )

        x = 0.5*guard3_width
        y = guard_height + comp.guardring_space + 0.5*guard3_height
        l_dp_ch = layouter.place(l_ch, x=x, y=y)
        layouter.place(dp, x=x, y=y)
        l_guard3 = layouter.place(l_guard3, x=x, y=y)

        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0,
            right=(guard_width + comp.guardring_space + guard2_width),
            top=(guard_height + comp.guardring_space + guard3_height),
        )

        # Draw interconnects
        w = resm1pad_bounds.right - resm1pad_bounds.left
        x = 0.5*(resm1pad_bounds.left + resm1pad_bounds.right)
        l_via = layouter.fab.layout_primitive(
            via1, portnets={"conn": pad}, bottom_width=w,
        )
        viam1_bounds = l_via.bounds(mask=metal1.mask)
        y = -viam1_bounds.top + resm1pad_bounds.top
        l_via = layouter.place(l_via, x=x, y=y)
        resm2pad_bounds = l_via.bounds(mask=metal2.mask)
        shape = _geo.Rect.from_rect(rect=resm1pad_bounds, bottom=0.0)
        layouter.add_wire(wire=metal2, net=pad, pin=metal2.pin, shape=shape)

        dnm1_bounds = l_dn_ch.bounds(mask=metal1.mask)
        dpm1_bounds = l_dp_ch.bounds(mask=metal1.mask)

        w = resm1core_bounds.right - resm1core_bounds.left
        x = 0.5*(resm1core_bounds.left + resm1core_bounds.right)
        l_via = layouter.fab.layout_primitive(
            via1, portnets={"conn": core}, bottom_width=w
        )
        viam1_bounds = l_via.bounds(mask=metal1.mask)
        y = -viam1_bounds.bottom + resm1core_bounds.bottom
        layouter.place(l_via, x=x, y=y)
        shape = _geo.Rect.from_rect(rect=resm1core_bounds, top=dpm1_bounds.top)
        layouter.add_wire(wire=metal2, net=core, shape=shape)

        layouter.add_wire(wire=via1, net=core, bottom_shape=dnm1_bounds)
        layouter.add_wire(wire=metal2, net=core, shape=dpm1_bounds)

        layouter.add_wire(wire=via1, net=core, bottom_shape=dpm1_bounds)
        shape = _geo.Rect.from_rect(rect=dpm1_bounds, top=layout.boundary.top)
        layouter.add_wire(wire=metal2, net=core, pin=metal2.pin, shape=shape)


class _RCClampResistor(_FactoryCell):
    def __init__(self, *, fab: "IOFactory"):
        # TODO: make3 more general; current only Sky130 compatibility
        super().__init__(fab=fab, name="RCClampResistor")

        spec = fab.spec
        tech = fab.tech

        res_prim = spec.resvdd_prim
        w = spec.resvdd_w
        l_finger = spec.resvdd_lfinger
        fingers = spec.resvdd_fingers
        space = spec.resvdd_space
        is_meander = spec.resvdd_meander

        assert (
            (res_prim is not None) and (w is not None)
            and (l_finger is not None) and (fingers is not None)
            and (space is not None)
        )

        pitch = w + space

        wire = res_prim.wire
        contact = res_prim.contact
        contact_space = res_prim.min_contact_space
        assert (contact is not None) and (contact_space is not None)
        assert len(contact.top) == 1
        metal = contact.top[0]
        assert isinstance(metal, _prm.MetalWire)
        metalpin = metal.pin

        ckt = self.new_circuit()

        res = ckt.new_net(name="res", external=False)
        pin1 = ckt.new_net(name="pin1", external=True)
        pin2 = ckt.new_net(name="pin2", external=True)

        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        if is_meander:
            if len(res_prim.indicator) != 1:
                raise NotImplementedError(
                    "Meander resistor layout for Resistor with multiple indicators"
                )
            indicator = res_prim.indicator[0]

            # TODO: draw real resistor, currently just the wire is drawn
            coords1: List[_geo.Point] = []
            coords2: List[_geo.Point] = []

            _l = layouter.wire_layout(
                net=pin1, wire=contact, bottom=wire,
                bottom_height=w, bottom_enclosure="tall",
                top_enclosure="tall",
            )
            _ch_chbb = _l.bounds(mask=contact.mask)
            _ch_wirebb = _l.bounds(mask=wire.mask)
            x = min(
                -contact_space - _ch_chbb.right,
                -_ch_wirebb.right,
            )
            y = -_ch_wirebb.bottom
            l = layouter.place(_l, x=x, y=y)
            ch_wirebb = l.bounds(mask=wire.mask)
            ch_metalbb = l.bounds(mask=metal.mask)

            if ch_wirebb.right < -_geo.epsilon:
                shape = _geo.Rect.from_rect(rect=ch_wirebb, right=0.0)
                layouter.add_wire(net=pin1, wire=wire, shape=shape)
            if (metal.min_area is None) or (ch_metalbb.area + _geo.epsilon) > metal.min_area:
                shape=ch_metalbb
            else:
                width = tech.on_grid(metal.min_area/ch_metalbb.height, mult=2, rounding="ceiling")
                shape = _geo.Rect.from_rect(rect=ch_metalbb, right=(ch_metalbb.left + width))
            layouter.add_wire(net=pin1, wire=metal, pin=metalpin, shape=shape)

            coords1.extend((_geo.origin, _geo.Point(x=0.0, y=w)))
            coords2.append(_geo.origin)

            if fingers%2 != 0:
                raise NotImplementedError("Odd value for resvdd_fingers")
            for f in range(fingers//2):
                left = 2*f*pitch
                coords1.extend((
                    _geo.Point(x=(left + space), y=w),
                    _geo.Point(x=(left + space), y=l_finger),
                    _geo.Point(x=(left + 2*pitch), y=l_finger),
                    _geo.Point(x=(left + 2*pitch), y=w),
                ))
                coords2.extend((
                    _geo.Point(x=(left + pitch), y=0.0),
                    _geo.Point(x=(left + pitch), y=(l_finger - w)),
                    _geo.Point(x=(left + pitch + space), y=(l_finger - w)),
                    _geo.Point(x=(left + pitch + space), y=0.0),
                ))
            endp = coords1[-1]
            coords1[-1] = _geo.Point.from_point(point=endp, y=0.0)

            meander = _geo.Polygon(points=(*coords1, *reversed(coords2)))
            ms = _geo.MaskShape(mask=wire.mask, shape=meander)
            layout.add_shape(net=res, shape=ms)
            ms = _geo.MaskShape(mask=indicator.mask, shape=meander)
            layout.add_shape(net=None, shape=ms)

            _l = layouter.wire_layout(
                net=pin2, wire=contact, bottom=wire,
                bottom_height=w, bottom_enclosure="tall",
                top_enclosure="tall",
            )
            _ch_chbb = _l.bounds(mask=contact.mask)
            _ch_wirebb = _l.bounds(mask=wire.mask)
            x = fingers*pitch + max(
                contact_space - _ch_chbb.left,
                -ch_wirebb.left,
            )
            y = -_ch_wirebb.bottom
            l = layouter.place(_l, x=x, y=y)
            ch_wirebb = l.bounds(mask=wire.mask)
            ch_metalbb = l.bounds(mask=metal.mask)

            if ch_wirebb.left - _geo.epsilon > fingers*pitch:
                shape = _geo.Rect.from_rect(rect=ch_wirebb, left=fingers*pitch)
                layouter.add_wire(net=pin2, wire=wire, shape=shape)
            if (metal.min_area is None) or ((ch_metalbb.area + _geo.epsilon) > metal.min_area):
                shape = ch_metalbb
            else:
                width = tech.on_grid(metal.min_area/ch_metalbb.height, mult=2, rounding="ceiling")
                shape = _geo.Rect.from_rect(rect=ch_metalbb, left=(ch_metalbb.right - width))
            layouter.add_wire(net=pin2, wire=metal, pin=metalpin, shape=shape)

            # boundary
            bb = _geo.Rect(
                left=0.0, bottom=0.0, right=meander.bounds.right, top=meander.bounds.top,
            )
            layouter.layout.boundary = bb
        else: # not is_meander
            x = 0.0
            prev_conn_net = pin1
            prev_conn_mbb = None
            for i in range(fingers):
                if i == (fingers - 1):
                    conn_net = pin2
                else:
                    conn_net = ckt.new_net(name=f"conn_{i}_{i+1}", external=False)
                res_inst = ckt.instantiate(
                    res_prim, name=f"res_fing[{i}]",
                    width=spec.resvdd_w, length=spec.resvdd_lfinger,
                )
                prev_conn_net.childports += res_inst.ports["port1"]
                conn_net.childports += res_inst.ports["port2"]

                rot = _geo.Rotation.No if (i%2) == 0 else _geo.Rotation.MX
                _res_lay = layouter.inst_layout(inst=res_inst, rotation=rot)
                _res_polybb = _res_lay.bounds(mask=wire.mask)

                res_lay = layouter.place(_res_lay, x=(x - _res_polybb.left), y=(-_res_polybb.bottom))
                res_lay_prevconn_mbb = res_lay.bounds(mask=metal.mask, net=prev_conn_net)
                res_lay_conn_mbb = res_lay.bounds(mask=metal.mask, net=conn_net)

                if prev_conn_mbb is not None:
                    shape = _geo.Rect.from_rect(rect=prev_conn_mbb, right=res_lay_prevconn_mbb.right)
                    layouter.add_wire(net=prev_conn_net, wire=metal, shape=shape)

                x += pitch
                prev_conn_net = conn_net
                prev_conn_mbb = res_lay_conn_mbb

            # Join implant and indicator layers
            for prim in (*res_prim.indicator, *res_prim.implant):
                layouter.add_portless(prim=prim, shape=layout.bounds(mask=prim.mask))

            pin1_mbb = layout.bounds(mask=metal.mask, net=pin1)
            layouter.add_wire(net=pin1, wire=metal, pin=metalpin, shape=pin1_mbb)
            pin2_mbb = layout.bounds(mask=metal.mask, net=pin2)
            layouter.add_wire(net=pin2, wire=metal, pin=metalpin, shape=pin2_mbb)

            layout.boundary = layout.bounds(mask=wire.mask)


class _RCClampInverter(_FactoryCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="RCClampInverter")

        spec = fab.spec
        tech = fab.tech
        comp = fab.computed

        ninv_l = spec.invvdd_n_l
        ninv_w = spec.invvdd_n_w
        inv_nmos = spec.invvdd_n_mosfet
        n_fingers = spec.invvdd_n_fingers
        assert (
            (ninv_l is not None) and (ninv_w is not None)
            and (inv_nmos is not None) and (n_fingers is not None)
        )

        pinv_l = spec.invvdd_p_l
        pinv_w = spec.invvdd_p_w
        inv_pmos = spec.invvdd_p_mosfet
        p_fingers = spec.invvdd_p_fingers
        assert (
            (pinv_l is not None) and (pinv_w is not None)
            and (inv_pmos is not None) and (p_fingers is not None)
        )

        cap_l = spec.capvdd_l
        cap_w = spec.capvdd_w
        cap_mos = spec.capvdd_mosfet
        cap_fingers = spec.capvdd_fingers
        assert (
            (cap_l is not None) and (cap_w is not None)
            and (cap_mos is not None) and (cap_fingers is not None)
        )
        if cap_mos != inv_nmos:
            raise NotImplemented("Cap MOSFET != inverter nmos MOSFET")

        active = comp.active
        poly = comp.poly
        contact = comp.contact
        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        via1 = comp.vias[1]
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        pclamp_cell = fab.clamp(type_="p", n_trans=spec.clampcount, n_drive=0)
        pclamp_lay = pclamp_cell.layout
        pclamp_actbb = pclamp_lay.bounds(mask=active.mask)

        ckt = self.new_circuit()
        supply = ckt.new_net(name="supply", external=True)
        ground = ckt.new_net(name="ground", external=True)
        in_ = ckt.new_net(name="in", external=True)
        out = ckt.new_net(name="out", external=True)

        layouter = self.new_circuitlayouter()

        actpitch = tech.computed.min_pitch(active, up=True)

        min_actpoly_space = tech.computed.min_space(active, poly)

        min_actch_space = None
        try:
            min_actch_space = tech.computed.min_space(active, contact)
        except ValueError:
            pass # Keep value at None

        # Outer ring with same dimensions as for the pclamp
        outerguardring_height = pclamp_actbb.height
        outerring_cell = fab.guardring(
            type_ = "p", width=spec.monocell_width, height=outerguardring_height,
        )
        inst = ckt.instantiate(outerring_cell, name="outerguard")
        ground.childports += inst.ports.conn
        x = 0.5*spec.monocell_width
        y = 0.5*outerguardring_height
        l = layouter.place(inst, x=x, y=y)
        outerguardring_m1bb = l.bounds(mask=metal1.mask)


        # Specs for cap mos and inverter nmos combined
        specs = []

        # inverter cap fingers
        for i in range(cap_fingers):
            inst = ckt.instantiate(cap_mos, name=f"capmos{i}", l=cap_l, w=cap_w)
            in_.childports += inst.ports.gate
            ground.childports += (
                inst.ports.sourcedrain1, inst.ports.sourcedrain2, inst.ports.bulk,
            )
            specs.append(_lay.MOSFETInstSpec(
                inst=inst, contact_left=contact, contact_right=contact,
            ))

        # inverter nmos fingers
        for i in range(n_fingers):
            inst = ckt.instantiate(inv_nmos, name=f"nmos{i}", l=ninv_l, w=ninv_w)
            in_.childports += inst.ports.gate
            ground.childports += inst.ports.bulk
            if i%2 == 0:
                ground.childports += inst.ports.sourcedrain1
                out.childports += inst.ports.sourcedrain2
            else:
                out.childports += inst.ports.sourcedrain1
                ground.childports += inst.ports.sourcedrain2
            specs.append(_lay.MOSFETInstSpec(
                inst=inst, contact_left=contact, contact_right=contact,
            ))

        _l = layouter.transistors_layout(trans_specs=specs)
        _actbb = _l.bounds()
        nmosguardring_height = tech.on_grid(
            _actbb.height + 8*actpitch, mult=2, rounding="ceiling",
        )
        nmosguardring_width = tech.on_grid(
            _actbb.width + 6*actpitch, mult=2, rounding="ceiling",
        )
        x = tech.on_grid(0.5*spec.monocell_width - _actbb.center.x)
        y = 0.5*_actbb.height + 10*actpitch
        nmos_lay = layouter.place(_l, x=x, y=y)
        nmos_actbb = nmos_lay.bounds(mask=active.mask)
        nmos_polybb = nmos_lay.bounds(mask=poly.mask)
        nmos_m1bb = nmos_lay.bounds(mask=metal1.mask)

        nmosguardring_cell = fab.guardring(
            type_="p", width=nmosguardring_width, height=nmosguardring_height,
            fill_implant=True,
        )
        inst = ckt.instantiate(nmosguardring_cell, name="nmosguardring")
        ground.childports += inst.ports.conn
        x = 0.5*spec.monocell_width
        l = layouter.place(inst, x=x, y=y)
        nmosguardring_actbb = l.bounds(mask=active.mask)
        nmosguardring_m1bb = l.bounds(mask=metal1.mask)

        # nmos guardring
        shape=_geo.Rect.from_rect(
            rect=nmosguardring_m1bb,
            top=nmosguardring_m1bb.bottom, bottom=outerguardring_m1bb.bottom,
        )
        layouter.add_wire(net=ground, wire=metal1, pin=metal1pin, shape=shape)

        # nmos ground connection
        for ms in nmos_lay.filter_polygons(
            net=ground, mask=metal1.mask, split=True, depth=1,
        ):
            bb = ms.shape.bounds
            shape = _geo.Rect.from_rect(rect=bb, top=nmosguardring_m1bb.top)
            layouter.add_wire(net=ground, wire=metal1, shape=shape)

        # nmos in connection
        w = nmos_polybb.width
        _l = layouter.wire_layout(
            net=in_, wire=contact, bottom=poly,
            bottom_width=w, bottom_enclosure="wide",
            top_width=w, top_enclosure="wide",
        )
        _ch_polybb = _l.bounds(mask=poly.mask)
        _ch_chbb = _l.bounds(mask=contact.mask)
        _ch_m1bb = _l.bounds(mask=metal1.mask)

        x = nmos_polybb.center.x
        y = min(
            nmos_actbb.bottom - min_actpoly_space - _ch_polybb.top,
            nmos_m1bb.bottom - metal1.min_space - _ch_m1bb.top,
        )
        if min_actch_space is not None:
            y = min(y, nmos_actbb.bottom - min_actch_space - _ch_chbb.top)
        l = layouter.place(_l, x=x, y=y)
        ch_polybb = l.bounds(mask=poly.mask)
        nmosinch_m1bb = l.bounds(mask=metal1.mask)

        for ms in nmos_lay.filter_polygons(net=in_, mask=poly.mask, split=True, depth=1):
            bb = ms.shape.bounds
            if bb.bottom - _geo.epsilon > ch_polybb.top:
                shape = _geo.Rect.from_rect(rect=bb, bottom=ch_polybb.bottom)
                layouter.add_wire(net=in_, wire=poly, shape=shape)

        _l = layouter.wire_layout(
            net=in_, wire=via1,
            bottom_width=w, bottom_enclosure="wide",
            top_width=w, top_enclosure="wide"
        )
        _via1_m1bb = _l.bounds(mask=metal1.mask)
        _via1_m2bb = _l.bounds(mask=metal2.mask)
        y = min(
            nmosinch_m1bb.top - _via1_m1bb.top,
            nmos_m1bb.bottom - metal1.min_space - _via1_m1bb.top,
            nmos_m1bb.bottom - 2*metal2.min_space - _via1_m2bb.top,
        )
        l = layouter.place(_l, x=x, y=y)
        nmosinvia1_m1bb = l.bounds(mask=metal1.mask)
        nmosinvia1_m2bb = l.bounds(mask=metal2.mask)

        if (nmosinvia1_m1bb.top + _geo.epsilon) < nmosinch_m1bb.bottom:
            shape = _geo.Rect.from_rect(rect=nmosinvia1_m1bb, top=nmosinch_m1bb.bottom)
            layouter.add_wire(net=in_, wire=metal1, shape=shape)

        # nmos out connection
        nmosout_m2left = spec.monocell_width
        nmosout_m2right = 0.0
        for ms in nmos_lay.filter_polygons(
            net=out, mask=metal1.mask, split=True, depth=1,
        ):
            bb = ms.shape.bounds
            l = layouter.add_wire(
                net=out, wire=via1, x=bb.center.x,
                bottom_bottom=bb.bottom, bottom_top=bb.top, bottom_enclosure="tall",
                top_bottom=bb.bottom, top_top=bb.top, top_enclosure="tall",
            )
            m2bb = l.bounds(mask=metal2.mask)
            nmosout_m2left = min(nmosout_m2left, m2bb.left)
            nmosout_m2right = max(nmosout_m2right, m2bb.right)

        # inverter pmos fingers
        specs = []
        for i in range(p_fingers):
            inst = ckt.instantiate(inv_pmos, name=f"pmos{i}", l=pinv_l, w=pinv_w)
            in_.childports += inst.ports.gate
            supply.childports += inst.ports.bulk
            if i%2 == 0:
                supply.childports += inst.ports.sourcedrain1
                out.childports += inst.ports.sourcedrain2
            else:
                out.childports += inst.ports.sourcedrain1
                supply.childports += inst.ports.sourcedrain2
            specs.append(_lay.MOSFETInstSpec(
                inst=inst, contact_left=contact, contact_right=contact,
            ))

        _l = layouter.transistors_layout(trans_specs=specs)
        _actbb = _l.bounds(mask=active.mask)
        pmosguardring_height = tech.on_grid(
            _actbb.height + 8*actpitch, mult=2, rounding="ceiling",
        )
        pmosguardring_width = tech.on_grid(
            _actbb.width + 6*actpitch, mult=2, rounding="ceiling",
        )
        x = 0.5*spec.monocell_width - _actbb.center.x
        y = nmosguardring_actbb.top + 8*actpitch - _actbb.bottom
        pmos_lay = layouter.place(_l, x=x, y=y)
        pmos_actbb = pmos_lay.bounds(mask=active.mask)
        pmos_polybb = pmos_lay.bounds(mask=poly.mask)
        pmos_m1bb = pmos_lay.bounds(mask=metal1.mask)

        # pmos guardring
        pmosguardring_cell = fab.guardring(
            type_="n", width=pmosguardring_width, height=pmosguardring_height,
            fill_well=True, fill_implant=True,
        )
        inst = ckt.instantiate(pmosguardring_cell, name="pmosguardring")
        supply.childports += inst.ports.conn
        x = 0.5*spec.monocell_width
        l = layouter.place(inst, x=x, y=y)
        pmosguardring_m1bb = l.bounds(mask=metal1.mask)

        for ms in pmos_lay.filter_polygons(
            net=supply, mask=metal1.mask, split=True, depth=1,
        ):
            bb = ms.shape.bounds
            shape = _geo.Rect.from_rect(rect=bb, bottom=pmosguardring_m1bb.bottom)
            layouter.add_wire(net=supply, wire=metal1, shape=shape)

        shape = _geo.Rect.from_rect(
            rect=pmosguardring_m1bb,
            bottom=(pmosguardring_m1bb.top - comp.guardring_width),
        )
        layouter.add_wire(net=supply, wire=metal1, pin=metal1pin, shape=shape)

        # pmos in connection
        w = pmos_polybb.width
        _l = layouter.wire_layout(
            net=in_, wire=contact, bottom=poly,
            bottom_width=w, bottom_enclosure="wide",
            top_width=w, top_enclosure="wide",
        )
        _ch_polybb = _l.bounds(mask=poly.mask)
        _ch_chbb = _l.bounds(mask=contact.mask)
        _ch_m1bb = _l.bounds(mask=metal1.mask)

        x = pmos_polybb.center.x
        y = max(
            pmos_actbb.top + min_actpoly_space - _ch_polybb.bottom,
            pmos_m1bb.top + metal1.min_space - _ch_m1bb.bottom,
        )
        if min_actch_space is not None:
            y = max(y, pmos_actbb.top + min_actch_space - _ch_chbb.bottom)
        l = layouter.place(_l, x=x, y=y)
        ch_polybb = l.bounds(mask=poly.mask)
        pmosinch_m1bb = l.bounds(mask=metal1.mask)

        for ms in pmos_lay.filter_polygons(net=in_, mask=poly.mask, split=True, depth=1):
            bb = ms.shape.bounds
            if bb.top + _geo.epsilon < ch_polybb.bottom:
                shape = _geo.Rect.from_rect(rect=bb, top=ch_polybb.top)
                layouter.add_wire(net=in_, wire=poly, shape=shape)

        _l = layouter.wire_layout(
            net=in_, wire=via1,
            bottom_width=w, bottom_enclosure="wide",
            top_width=w, top_enclosure="wide",
        )
        _via1_m1bb = _l.bounds(mask=metal1.mask)
        _via1_m2bb = _l.bounds(mask=metal2.mask)
        y = max(
            pmosinch_m1bb.bottom - _via1_m1bb.bottom,
            pmos_m1bb.top + metal1.min_space - _via1_m1bb.bottom,
            pmos_m1bb.top + 2*metal2.min_space - _via1_m2bb.bottom,
        )
        l = layouter.place(_l, x=x, y=y)
        pmosinvia1_m1bb = l.bounds(mask=metal1.mask)
        pmosinvia1_m2bb = l.bounds(mask=metal2.mask)

        if (pmosinvia1_m1bb.bottom - _geo.epsilon) > pmosinch_m1bb.top:
            shape = _geo.Rect.from_rect(rect=pmosinvia1_m1bb, bottom=pmosinch_m1bb.top)
            layouter.add_wire(net=in_, wire=metal1, shape=shape)

        # pmos out connection
        pmosout_m2left = spec.monocell_width
        pmosout_m2right = 0.0
        for ms in pmos_lay.filter_polygons(
            net=out, mask=metal1.mask, split=True, depth=1,
        ):
            bb = ms.shape.bounds
            l = layouter.add_wire(
                net=out, wire=via1, x=bb.center.x,
                bottom_bottom=bb.bottom, bottom_top=bb.top, bottom_enclosure="tall",
                top_bottom=bb.bottom, top_top=bb.top, top_enclosure="tall",
            )
            m2bb = l.bounds(mask=metal2.mask)
            pmosout_m2left = min(pmosout_m2left, m2bb.left)
            pmosout_m2right = max(pmosout_m2right, m2bb.right)

        assert nmosout_m2left > pmosout_m2left
        shape = _geo.Rect(
            left=pmosout_m2left, bottom=pmos_m1bb.bottom,
            right=max(nmosout_m2right, pmosout_m2right), top=pmos_m1bb.top,
        )
        layouter.add_wire(net=out, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=nmosout_m2left, bottom=nmos_m1bb.bottom,
            right=nmosout_m2right, top=pmos_m1bb.top,
        )
        layouter.add_wire(net=out, wire=metal2, pin=metal2pin, shape=shape)

        # in pin
        assert pmosinvia1_m2bb.left > nmosinvia1_m2bb.left
        shape = _geo.Rect.from_rect(rect=pmosinvia1_m2bb, left=nmosinvia1_m2bb.left)
        layouter.add_wire(net=in_, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=nmosinvia1_m2bb.left, bottom=nmosinvia1_m2bb.bottom,
            right=(pmosout_m2left - 3*metal2.min_space), top=pmosinvia1_m2bb.top,
        )
        layouter.add_wire(net=in_, wire=metal2, pin=metal2pin, shape=shape)

        # boundary
        layouter.layout.boundary = outerguardring_m1bb


class _Pad(_FactoryOnDemandCell):
    def __init__(self, *,
        name: str, fab: "IOFactory", width: float, height: float, start_via: int,
    ):
        super().__init__(fab=fab, name=name)

        self.width = width
        self.height = height
        self.start_via = start_via

    def _create_circuit(self):
        ckt = self.new_circuit()
        ckt.new_net(name="pad", external=True)

    def _create_layout(self):
        fab = self.fab
        width = self.width
        height = self.height
        start_via = self.start_via
        framespec = fab.frame.framespec

        comp = fab.computed
        pad = comp.pad
        topmetal = pad.bottom
        topmetalpin = topmetal.pin

        pad_net = self.circuit.nets.pad
        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        enc = comp.pad.min_bottom_enclosure.max()
        metal_width = width + 2*enc
        metal_height = height + 2*enc

        metal_bounds = _geo.Rect.from_size(width=metal_width, height=metal_height)
        pad_bounds = _geo.Rect.from_size(width=width, height=height)

        # TODO: add support in layouter.add_wire for PadOpening
        layouter.add_wire(net=pad_net, wire=topmetal, pin=topmetalpin, shape=metal_bounds)
        layout.add_shape(layer=comp.pad, net=pad_net, shape=pad_bounds)

        if framespec.pad_viapitch is None:
            top_via = comp.vias[-1]
            via_pitch = top_via.width + top_via.min_space
        else:
            via_pitch = framespec.pad_viapitch

        for i, via in enumerate(comp.vias[start_via:]):
            l_via = hlp.diamondvia(
                fab=fab, net=pad_net, via=via,
                width=metal_width, height=metal_height,
                space=(via_pitch - via.width),
                enclosure=_prp.Enclosure(framespec.pad_viametal_enclosure),
                center_via=((i%2) == 0), corner_distance=framespec.pad_viacorner_distance,
            )
            layouter.place(l_via, x=0.0, y=0.0)

        layout.boundary = metal_bounds


class _LevelUp(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="LevelUp")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        circuit = self.new_circuit()

        iopmos_lvlshift_w = max(
            spec.iopmos.computed.min_w, fab.computed.minwidth4ext_activewithcontact,
        )

        # Input inverter
        n_i_inv = circuit.instantiate(spec.nmos, name="n_i_inv", w=comp.maxnmos_w)
        p_i_inv = circuit.instantiate(spec.pmos, name="p_i_inv", w=comp.maxpmos_w)

        # Level shifter
        n_lvld_n = circuit.instantiate(
            spec.ionmos, name="n_lvld_n", w=comp.maxionmos_w,
        )
        n_lvld = circuit.instantiate(
            spec.ionmos, name="n_lvld", w=comp.maxionmos_w,
        )
        p_lvld_n = circuit.instantiate(
            spec.iopmos, name="p_lvld_n", w=iopmos_lvlshift_w,
        )
        p_lvld = circuit.instantiate(
            spec.iopmos, name="p_lvld", w=iopmos_lvlshift_w,
        )

        # Output inverter/driver
        n_lvld_n_inv = circuit.instantiate(
            spec.ionmos, name="n_lvld_n_inv", w=comp.maxionmos_w,
        )
        p_lvld_n_inv = circuit.instantiate(
            spec.iopmos, name="p_lvld_n_inv", w=comp.maxiopmos_w,
        )

        # Create the nets
        circuit.new_net(name="vdd", external=True, childports=(
            p_i_inv.ports.sourcedrain2, p_i_inv.ports.bulk,
        ))
        circuit.new_net(name="iovdd", external=True, childports=(
            p_lvld_n.ports.sourcedrain1, p_lvld_n.ports.bulk,
            p_lvld.ports.sourcedrain2, p_lvld.ports.bulk,
            p_lvld_n_inv.ports.sourcedrain1, p_lvld_n_inv.ports.bulk,
        ))
        circuit.new_net(name="vss", external=True, childports=(
            n_i_inv.ports.sourcedrain2, n_i_inv.ports.bulk,
            n_lvld_n.ports.sourcedrain1, n_lvld_n.ports.bulk,
            n_lvld.ports.sourcedrain2, n_lvld.ports.bulk,
            n_lvld_n_inv.ports.sourcedrain1, n_lvld_n_inv.ports.bulk,
        ))

        circuit.new_net(name="i", external=True, childports=(
            n_i_inv.ports.gate, p_i_inv.ports.gate,
            n_lvld_n.ports.gate,
        ))
        circuit.new_net(name="i_n", external=False, childports=(
            n_i_inv.ports.sourcedrain1, p_i_inv.ports.sourcedrain1,
            n_lvld.ports.gate,
        ))
        circuit.new_net(name="lvld", external=False, childports=(
            p_lvld_n.ports.gate,
            n_lvld.ports.sourcedrain1, p_lvld.ports.sourcedrain1,
        ))
        circuit.new_net(name="lvld_n", external=False, childports=(
            n_lvld_n.ports.sourcedrain2, p_lvld_n.ports.sourcedrain2,
            p_lvld.ports.gate,
            n_lvld_n_inv.ports.gate, p_lvld_n_inv.ports.gate,
        ))
        circuit.new_net(name="o", external=True, childports=(
            n_lvld_n_inv.ports.sourcedrain2, p_lvld_n_inv.ports.sourcedrain2,
        ))

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        comp = fab.computed

        circuit = self.circuit
        insts = circuit.instances
        nets = circuit.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        ionimplant = comp.ionimplant
        iopimplant = comp.iopimplant
        assert pimplant == iopimplant
        nwell = comp.nwell
        poly = comp.poly
        contact = comp.contact
        metal1 = contact.top[0]
        assert isinstance(metal1, _prm.MetalWire)
        metal1pin = metal1.pin
        via1 = comp.vias[1]
        metal2 = via1.top[0]
        assert isinstance(metal2, _prm.MetalWire)

        chm1_enc = contact.min_top_enclosure[0]
        chm1_wideenc = _prp.Enclosure((chm1_enc.max(), chm1_enc.min()))

        actox_enc = (
            comp.activeoxide_enclosure.max() if comp.activeoxide_enclosure is not None
            else comp.iogateoxide_enclosure.max()
        )

        iopmos_lvlshift_w = max(
            spec.iopmos.computed.min_w, comp.minwidth4ext_activewithcontact,
        )

        layouter = self.new_circuitlayouter()
        layout = self.layout
        active_left = 0.5*active.min_space

        if metal2.pin is not None:
            pin_args = {"pin": metal2.pin}
        else:
            pin_args = {}

        min_actpoly_space = tech.computed.min_space(active, poly)
        try:
            min_actch_space = tech.computed.min_space(active, contact)
        except AttributeError:
            min_actch_space = None

        #
        # Core row
        #

        x = active_left + 0.5*comp.minwidth_activewithcontact
        bottom = comp.maxnmos_activebottom
        top = comp.maxnmos_activetop
        l = layouter.add_wire(
            net=nets.i_n, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=nimplant,
            bottom_height=(top - bottom),
        )
        chvss_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i_n, wire=active, implant=nimplant,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxnmos_y, height=comp.maxnmos_w,
        )
        bottom = comp.maxpmos_activebottom
        top = comp.maxpmos_activetop
        l = layouter.add_wire(
            net=nets.i_n, well_net=nets.vdd, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=pimplant, bottom_well=nwell,
            bottom_height=(top - bottom),
        )
        chvdd_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i_n, well_net=nets.vdd, wire=active, implant=pimplant, well=nwell,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxpmos_y, height=comp.maxpmos_w,
        )
        shape = _geo.Rect.from_rect(
            rect=chvss_m1bounds, bottom=chvss_m1bounds.top, top=chvdd_m1bounds.bottom,
        )
        layouter.add_wire(net=nets.i_n, wire=metal1, shape=shape)
        bottom_shape = _geo.Rect(
            bottom=chvss_m1bounds.bottom, top=chvdd_m1bounds.top,
            right=chvss_m1bounds.right, left=(chvss_m1bounds.right - comp.metal[1].minwidth_up),
        )
        m2bounds = layouter.add_wire(
            net=nets.i_n, wire=via1, bottom_shape=bottom_shape,
        ).bounds(mask=metal2.mask)
        i_n_m2bounds = _geo.Rect.from_rect(rect=m2bounds, bottom=spec.iorow_height)
        layouter.add_wire(net=nets.i_n, wire=metal2, shape=i_n_m2bounds)

        x += max((
            comp.minnmos_contactgatepitch,
            comp.minpmos_contactgatepitch,
        ))
        n_i_inv_lay = l = layouter.place(insts.n_i_inv, x=x, y=comp.maxnmos_y)
        gatebounds_n = l.bounds(mask=poly.mask)
        p_i_inv_lay = l = layouter.place(insts.p_i_inv, x=x, y=comp.maxpmos_y)
        gatebounds_p = l.bounds(mask=poly.mask)

        shape = _geo.Rect(
            left=min(gatebounds_n.left, gatebounds_p.left), bottom=gatebounds_n.top,
            right=max(gatebounds_n.right, gatebounds_p.right), top=gatebounds_p.bottom,
        )
        polybounds = layouter.add_wire(
            net=nets.i, wire=poly, shape=shape,
        ).bounds(mask=poly.mask)
        x_pad = max(
            polybounds.left + 0.5*comp.minwidth4ext_polywithcontact,
            chvss_m1bounds.right + metal1.min_space
            + 0.5*comp.metal[1].minwidth4ext_down,
        )
        l = layouter.add_wire(
            net=nets.i, wire=contact, bottom=poly, x=x_pad,
            y=tech.on_grid(0.5*(polybounds.bottom + polybounds.top)),
        )
        ppad_m1bounds = l.bounds(mask=metal1.mask)
        ppad_polybounds = l.bounds(mask=poly.mask)
        if ppad_polybounds.left > polybounds.right:
            shape = _geo.Rect.from_rect(rect=ppad_polybounds, left=polybounds.left)
            layouter.add_wire(net=nets.i, wire=poly, shape=shape)

        x += max((
            comp.minnmos_contactgatepitch,
            comp.minpmos_contactgatepitch,
        ))
        bottom = comp.maxnmos_activebottom
        top = min(comp.maxnmos_activetop, ppad_m1bounds.bottom - metal1.min_width)
        chvss_m1bounds = layouter.add_wire(
            net=nets.vss, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=nimplant,
            bottom_height=(top - bottom), top_height=(top - bottom - metal1.min_space)
        ).bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.vss, wire=active, implant=nimplant,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxnmos_y, height=comp.maxnmos_w,
        )
        bottom = max(comp.maxpmos_activebottom, ppad_m1bounds.top + metal1.min_width)
        top = comp.maxpmos_activetop
        chvdd_m1bounds = layouter.add_wire(
            net=nets.vdd, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=pimplant,
            bottom_height=(top - bottom), top_height=(top - bottom - metal1.min_space),
        ).bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.vdd, well_net=nets.vdd, wire=active, implant=pimplant, well=nwell,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxpmos_y, height=comp.maxpmos_w,
        )

        shape = _geo.Rect.from_rect(
            rect=chvss_m1bounds, bottom=spec.iorow_height, top=chvss_m1bounds.bottom,
        )
        layouter.add_wire(net=nets.vss, wire=metal1, shape=shape)
        shape = _geo.Rect.from_rect(rect=chvdd_m1bounds, top=spec.cells_height)
        layouter.add_wire(net=nets.vdd, wire=metal1, shape=shape)

        x += comp.minwidth_activewithcontact + active.min_space
        bottom = comp.maxnmos_activebottom
        top = comp.maxnmos_activetop
        i_nactcont_lay = l = layouter.add_wire(
            net=nets.i, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=nimplant,
            bottom_height=(top - bottom),
        )
        ndio_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i, wire=active, implant=nimplant,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxnmos_y, height=comp.maxnmos_w,
        )
        bottom = comp.maxpmos_activebottom
        top = comp.maxpmos_activetop
        i_pactcont_lay = l = layouter.add_wire(
            net=nets.i, wire=contact, x=x, y=0.5*(bottom + top),
            bottom=active, bottom_implant=pimplant,
            bottom_height=(top - bottom),
        )
        pdio_m1bounds = l.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.i, well_net=nets.vdd, wire=active, implant=pimplant, well=nwell,
            x=x, width=comp.minwidth_activewithcontact,
            y=comp.maxpmos_y, height=comp.maxpmos_w,
        )
        shape = _geo.Rect.from_rect(
            rect=ndio_m1bounds, bottom=ndio_m1bounds.top, top=pdio_m1bounds.bottom,
        )
        layouter.add_wire(net=nets.i, wire=metal1, shape=shape)
        shape = _geo.Rect(
            left=ppad_m1bounds.left, bottom=(chvss_m1bounds.top + metal1.min_space),
            right=ndio_m1bounds.right, top=(chvdd_m1bounds.bottom - metal1.min_space),
        )
        layouter.add_wire(net=nets.i, wire=metal1, shape=shape)
        bottom = ndio_m1bounds.bottom
        top = pdio_m1bounds.top
        i_m2bounds = layouter.add_wire(
            net=nets.i, wire=via1, x=x, bottom_bottom=bottom, bottom_top=top,
        ).bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.i, wire=metal2, **pin_args, shape=i_m2bounds) # pyright: ignore

        # Fill implants
        if nimplant is not None:
            bb = i_nactcont_lay.bounds(mask=nimplant.mask)
            bb2 = n_i_inv_lay.bounds(mask=nimplant.mask)
            layouter.add_portless(prim=nimplant, shape=_geo.Rect.from_rect(
                rect=bb2, right=bb.right,
            ))
        if pimplant is not None:
            bb = i_pactcont_lay.bounds(mask=pimplant.mask)
            bb2 = p_i_inv_lay.bounds(mask=pimplant.mask)
            layouter.add_portless(prim=pimplant, shape=_geo.Rect.from_rect(
                rect=bb2, right=bb.right,
            ))

        #
        # IO row
        #
        active_left = 0.5*comp.min_oxactive_space
        y_iopmos_lvlshift = comp.maxiopmos_y

        # Place left source-drain contacts
        _nch_lvld_lay = layouter.wire_layout(
            net=nets.lvld, wire=contact, bottom=active, bottom_implant=ionimplant,
            bottom_height=comp.maxionmos_w,
        )
        _nch_lvld_actbounds = _nch_lvld_lay.bounds(mask=active.mask)
        x = active_left - _nch_lvld_actbounds.left
        y = comp.maxionmos_y
        nch_lvld_lay = layouter.place(object_=_nch_lvld_lay, x=x, y=y)
        nch_lvld_chbounds = nch_lvld_lay.bounds(mask=contact.mask)
        nch_lvld_m1bounds = nch_lvld_lay.bounds(mask=metal1.mask)
        _pch_lvld_lay = layouter.wire_layout(
            net=nets.lvld, well_net=nets.iovdd, wire=contact,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            bottom_height=iopmos_lvlshift_w,
        )
        _pch_lvld_actbounds = _pch_lvld_lay.bounds(mask=active.mask)
        x = active_left - _pch_lvld_actbounds.left
        y = y_iopmos_lvlshift
        pch_lvld_lay = layouter.place(object_=_pch_lvld_lay, x=x, y=y)
        pch_lvld_chbounds = pch_lvld_lay.bounds(mask=contact.mask)
        pch_lvld_m1bounds = pch_lvld_lay.bounds(mask=metal1.mask)
        lvld_m1_lay = layouter.add_wire(
            net=nets.lvld, wire=metal1, shape=_geo.Rect.from_rect(
                rect=nch_lvld_m1bounds, bottom=pch_lvld_m1bounds.bottom,
            ),
        )
        lvld_m1_bounds = lvld_m1_lay.bounds()

        poly_left = max(
            nch_lvld_chbounds.right + spec.ionmos.computed.min_contactgate_space,
            pch_lvld_chbounds.right + spec.iopmos.computed.min_contactgate_space,
        )

        # Place n_lvld and p_lvld, and compute pad y placements
        _n_lvld_lay = layouter.inst_layout(
            inst=insts.n_lvld, sd_width=0.5*spec.ionmos.computed.min_gate_space,
        )
        _n_lvld_polybounds = _n_lvld_lay.bounds(mask=poly.mask)
        x = poly_left - _n_lvld_polybounds.left
        y = comp.maxionmos_y
        n_lvld_lay = layouter.place(_n_lvld_lay, x=x, y=y)
        n_lvld_actbounds = n_lvld_lay.bounds(mask=active.mask)
        n_lvld_polybounds = n_lvld_lay.bounds(mask=poly.mask)
        _p_lvld_lay = layouter.inst_layout(
            inst=insts.p_lvld, sd_width=0.5*spec.iopmos.computed.min_gate_space,
        )
        _p_lvld_polybounds = _p_lvld_lay.bounds(mask=poly.mask)
        x = poly_left - _p_lvld_polybounds.left
        y = y_iopmos_lvlshift
        p_lvld_lay = layouter.place(_p_lvld_lay, x=x, y=y)
        p_lvld_actbounds = p_lvld_lay.bounds(mask=active.mask)
        p_lvld_polybounds = p_lvld_lay.bounds(mask=poly.mask)
        w = cast(_ckt._PrimitiveInstance, insts.p_lvld).params["w"]
        p_lvld_pad_bottom = (
            y_iopmos_lvlshift + 0.5*w
            + tech.computed.min_space(active, poly)
        )
        p_lvld_pad_top = (
            p_lvld_pad_bottom + comp.minwidth4ext_polywithcontact
        )
        p_lvld_n_pad_bottom = p_lvld_pad_top + poly.min_space

        # Place mid source-drain contacts
        _lvlshift_chiovss_lay = layouter.wire_layout(
            net=nets.vss, wire=contact, bottom=active, bottom_implant=ionimplant,
            bottom_height=comp.maxionmos_w,
        )
        _lvlshift_chvss_chbounds = _lvlshift_chiovss_lay.bounds(mask=contact.mask)
        x = (
            n_lvld_polybounds.right + spec.ionmos.computed.min_contactgate_space
            - _lvlshift_chvss_chbounds.left
        )
        y = comp.maxionmos_y
        lvlshit_chiovss_lay = layouter.place(object_=_lvlshift_chiovss_lay, x=x, y=y)
        lvlshift_chiovss_chbounds = lvlshit_chiovss_lay.bounds(mask=contact.mask)
        lvlshift_chiovss_m1bounds = lvlshit_chiovss_lay.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.vss, wire=metal1, shape=_geo.Rect.from_rect(
                rect=lvlshift_chiovss_m1bounds, top=spec.iorow_height,
            ),
        )
        _lvlshift_chiovdd_lay = layouter.wire_layout(
            net=nets.iovdd, well_net=nets.iovdd, wire=contact, bottom_height=iopmos_lvlshift_w,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            top_enclosure=chm1_wideenc,
        )
        _lvlshift_chiovdd_chbounds = _lvlshift_chiovdd_lay.bounds(mask=contact.mask)
        x = (
            p_lvld_polybounds.right + spec.iopmos.computed.min_contactgate_space
            - _lvlshift_chiovdd_chbounds.left
        )
        y = y_iopmos_lvlshift
        lvlshift_chiovdd_lay = layouter.place(object_=_lvlshift_chiovdd_lay, x=x, y=y)
        lvlshift_chiovdd_chbounds = lvlshift_chiovdd_lay.bounds(mask=contact.mask)
        lvlshift_chiovdd_m1bounds = lvlshift_chiovdd_lay.bounds(mask=metal1.mask)
        layouter.add_wire(
            net=nets.iovdd, wire=metal1, shape=_geo.Rect.from_rect(
                rect=lvlshift_chiovdd_m1bounds, bottom=0.0,
            ),
        )

        poly_left = max(
            lvlshift_chiovss_chbounds.right + spec.ionmos.computed.min_contactgate_space,
            lvlshift_chiovdd_chbounds.right + spec.iopmos.computed.min_contactgate_space,
        )

        # Place n_lvld_n and p_lvld_n
        _n_lvld_n_lay = layouter.inst_layout(
            inst=insts.n_lvld_n, sd_width=0.5*spec.ionmos.computed.min_gate_space,
        )
        _n_lvld_n_polybounds = _n_lvld_n_lay.bounds(mask=poly.mask)
        x = poly_left - _n_lvld_n_polybounds.left
        y = comp.maxionmos_y
        n_lvld_n_lay = layouter.place(object_=_n_lvld_lay, x=x, y=y)
        n_lvld_n_actbounds = n_lvld_n_lay.bounds(mask=active.mask)
        n_lvld_n_polybounds = n_lvld_n_lay.bounds(mask=poly.mask)
        _p_lvld_n_lay = layouter.inst_layout(
            inst=insts.p_lvld_n, sd_width=0.5*spec.iopmos.computed.min_gate_space,
        )
        _p_lvld_n_polybounds = _p_lvld_n_lay.bounds(mask=poly.mask)
        x = poly_left - _p_lvld_n_polybounds.left
        y = y_iopmos_lvlshift
        p_lvld_n_lay = layouter.place(object_=_p_lvld_n_lay, x=x, y=y)
        p_lvld_n_polybounds = p_lvld_n_lay.bounds(mask=poly.mask)

        # Place right source-drain contacts
        _nch_lvld_n_lay = layouter.wire_layout(
            net=nets.lvld_n, wire=contact, bottom_height=comp.maxionmos_w,
            bottom=active, bottom_implant=ionimplant,
        )
        _nch_lvld_n_chbounds = _nch_lvld_lay.bounds(mask=contact.mask)
        nch_lvld_n_x = (
            n_lvld_n_polybounds.right + spec.nmos.computed.min_contactgate_space
            - _nch_lvld_n_chbounds.left
        )
        nch_lvld_n_y = comp.maxionmos_y
        nch_lvld_n_lay = layouter.place(
            object_=_nch_lvld_n_lay, x=nch_lvld_n_x, y=nch_lvld_n_y,
        )
        nch_lvld_n_actbounds = nch_lvld_n_lay.bounds(mask=active.mask)
        nch_lvld_n_m1bounds = nch_lvld_n_lay.bounds(mask=metal1.mask)
        _pch_lvld_n_lay = layouter.wire_layout(
            net=nets.lvld_n, well_net=nets.iovdd, wire=contact,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            bottom_height=iopmos_lvlshift_w,
        )
        _pch_lvld_n_chbounds = _pch_lvld_n_lay.bounds(mask=contact.mask)
        pch_lvld_n_x = (
            p_lvld_n_polybounds.right + spec.pmos.computed.min_contactgate_space
            - _pch_lvld_n_chbounds.left
        )
        pch_lvld_n_y = y_iopmos_lvlshift
        pch_lvld_n_lay = layouter.place(
            object_=_pch_lvld_n_lay, x=pch_lvld_n_x, y=pch_lvld_n_y
        )
        pch_lvld_n_actbounds = pch_lvld_n_lay.bounds(mask=active.mask)
        pch_lvld_n_m1bounds = pch_lvld_n_lay.bounds(mask=metal1.mask)
        lvld_n_m1_lay = layouter.add_wire(
            net=nets.lvld_n, wire=metal1, shape=_geo.Rect.from_rect(
                rect=nch_lvld_n_m1bounds, bottom=pch_lvld_n_m1bounds.bottom,
            ),
        )
        lvld_n_m1_bounds = lvld_n_m1_lay.bounds()
        # Add manual implant rectangle
        if iopimplant is not None:
            bb1 = pch_lvld_lay.bounds(mask=iopimplant.mask)
            bb2 = pch_lvld_n_lay.bounds(mask=iopimplant.mask)
            if iopimplant is not None:
                layouter.add_portless(prim=iopimplant, shape=_geo.Rect(
                    left=bb1.left, bottom=bb1.bottom,
                    right=bb2.right, top=bb1.top,
                ))

        # Poly pads for nmoses of the level shifter
        _n_lvld_ppad_lay = layouter.wire_layout(
            net=nets.i_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _n_lvld_ppad_polybounds = _n_lvld_ppad_lay.bounds(mask=poly.mask)
        _n_lvld_ppad_chbounds = _n_lvld_ppad_lay.bounds(mask=contact.mask)
        _n_lvld_ppad_m1bounds = _n_lvld_ppad_lay.bounds(mask=metal1.mask)
        _n_lvld_n_ppad_lay = layouter.wire_layout(
            net=nets.i_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _n_lvld_n_ppad_polybounds = _n_lvld_n_ppad_lay.bounds(mask=poly.mask)
        _n_lvld_n_ppad_chbounds = _n_lvld_n_ppad_lay.bounds(mask=contact.mask)
        _n_lvld_n_ppad_m1bounds = _n_lvld_n_ppad_lay.bounds(mask=metal1.mask)

        n_lvld_ppad_x = max(
            n_lvld_polybounds.left - _n_lvld_ppad_polybounds.left,
            n_lvld_polybounds.right - _n_lvld_ppad_polybounds.right,
            lvld_m1_bounds.right + metal1.min_space - _n_lvld_ppad_m1bounds.left,
        )
        n_lvld_ppad_y = min(
            n_lvld_actbounds.bottom - min_actpoly_space - _n_lvld_ppad_polybounds.top,
            lvlshift_chiovss_m1bounds.bottom - metal1.min_space - _n_lvld_ppad_m1bounds.top,
        )
        if min_actch_space is not None:
            n_lvld_ppad_y = min(
                n_lvld_ppad_y,
                n_lvld_actbounds.bottom - min_actch_space - _n_lvld_ppad_chbounds.top,
            )
        n_lvld_n_ppad_x = min(
            n_lvld_n_polybounds.left - _n_lvld_n_ppad_polybounds.left,
            n_lvld_n_polybounds.right - _n_lvld_n_ppad_polybounds.right,
            lvld_n_m1_bounds.left - metal1.min_space - _n_lvld_n_ppad_m1bounds.right,
        )
        n_lvld_n_ppad_y = min(
            n_lvld_n_actbounds.bottom - min_actpoly_space - _n_lvld_n_ppad_polybounds.top,
            lvlshift_chiovss_m1bounds.bottom - metal1.min_space - _n_lvld_n_ppad_m1bounds.top,
        )
        if min_actch_space is not None:
            n_lvld_n_ppad_y = min(
                n_lvld_n_ppad_y,
                n_lvld_n_actbounds.bottom - min_actch_space - _n_lvld_n_ppad_chbounds.top,
            )

        n_lvld_ppad_lay = layouter.place(
            object_=_n_lvld_ppad_lay, x=n_lvld_ppad_x, y=n_lvld_ppad_y,
        )
        n_lvld_ppad_polybounds = n_lvld_ppad_lay.bounds(mask=poly.mask)
        n_lvld_ppad_m1bounds = n_lvld_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_lvld_polybounds, bottom=n_lvld_ppad_polybounds.bottom,
        ))
        n_lvld_n_ppad_lay = layouter.place(
            object_=_n_lvld_n_ppad_lay, x=n_lvld_n_ppad_x, y=n_lvld_n_ppad_y,
        )
        n_lvld_n_ppad_polybounds = n_lvld_n_ppad_lay.bounds(mask=poly.mask)
        n_lvld_n_ppad_m1bounds = n_lvld_n_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld_n, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_lvld_n_polybounds, bottom=n_lvld_n_ppad_polybounds.bottom,
        ))

        # via1 pads on the poly pads
        # draw two vias to make sure metal1 area is big enough
        _n_lvld_via_lay = layouter.wire_layout(net=nets.i_n, wire=via1, rows=2)
        _n_lvld_via_m1bounds = _n_lvld_via_lay.bounds(mask=metal1.mask)
        n_lvld_via_x = n_lvld_ppad_m1bounds.left - _n_lvld_via_m1bounds.left
        n_lvld_via_y = n_lvld_ppad_m1bounds.top - _n_lvld_via_m1bounds.top
        n_lvld_via_lay = layouter.place(
            object_=_n_lvld_via_lay, x=n_lvld_via_x, y=n_lvld_via_y,
        )
        n_lvld_n_via_m2bounds = n_lvld_via_lay.bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.i_n, wire=metal2, shape=_geo.Rect.from_rect(
            rect=i_n_m2bounds, bottom=n_lvld_n_via_m2bounds.bottom,
        ))
        layouter.add_wire(net=nets.i_n, wire=metal2, shape=_geo.Rect.from_rect(
            rect=n_lvld_n_via_m2bounds, left=i_n_m2bounds.left,
        ))
        _n_lvld_n_via_lay = layouter.wire_layout(net=nets.i, wire=via1, rows=2)
        _n_lvld_n_via_m1bounds = _n_lvld_n_via_lay.bounds(mask=metal1.mask)
        n_lvld_n_via_x = n_lvld_n_ppad_m1bounds.right - _n_lvld_n_via_m1bounds.right
        n_lvld_n_via_y = n_lvld_n_ppad_m1bounds.top - _n_lvld_n_via_m1bounds.top
        n_lvld_n_via_lay = layouter.place(
            object_=_n_lvld_n_via_lay, x=n_lvld_n_via_x, y=n_lvld_n_via_y,
        )
        n_lvld_n_via_m2bounds = n_lvld_n_via_lay.bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.i, wire=metal2, shape=_geo.Rect.from_rect(
            rect=i_m2bounds, bottom=n_lvld_n_via_m2bounds.bottom,
        ))
        assert i_m2bounds.left <= n_lvld_n_via_m2bounds.right
        layouter.add_wire(net=nets.i, wire=metal2, shape=_geo.Rect.from_rect(
            rect=n_lvld_n_via_m2bounds, left=i_m2bounds.left,
        ))

        # Poly pads for the pmoses of the level shifter
        _p_lvld_ppad_lay = layouter.wire_layout(
            net=nets.lvld, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _p_lvld_ppad_polybounds = _p_lvld_ppad_lay.bounds(mask=poly.mask)
        _p_lvld_ppad_chbounds = _p_lvld_ppad_lay.bounds(mask=contact.mask)
        _p_lvld_ppad_m1bounds = _p_lvld_ppad_lay.bounds(mask=metal1.mask)
        p_lvld_ppad_x = max(
            lvld_m1_bounds.right + metal1.min_space - _p_lvld_ppad_m1bounds.left,
            p_lvld_polybounds.left - _p_lvld_ppad_polybounds.left,
            p_lvld_polybounds.right - _p_lvld_ppad_polybounds.right,
        )
        p_lvld_ppad_y = max(
            p_lvld_actbounds.top + min_actpoly_space - _p_lvld_ppad_polybounds.bottom,
            lvlshift_chiovdd_m1bounds.top + metal1.min_space - _p_lvld_ppad_m1bounds.bottom,
        )
        if min_actch_space is not None:
            p_lvld_ppad_y = max(
                p_lvld_ppad_y,
                p_lvld_actbounds.top + min_actch_space - _p_lvld_ppad_chbounds.bottom
            )
        p_lvld_ppad_lay = layouter.place(
            object_=_p_lvld_ppad_lay, x=p_lvld_ppad_x, y=p_lvld_ppad_y,
        )
        p_lvld_ppad_polybounds = p_lvld_ppad_lay.bounds(mask=poly.mask)
        p_lvld_ppad_m1bounds = p_lvld_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld, wire=poly, shape=_geo.Rect.from_rect(
            rect=p_lvld_polybounds, top=p_lvld_ppad_polybounds.top,
        ))
        layouter.add_wire(net=nets.lvld_n, wire=metal1, shape=_geo.Rect.from_rect(
            rect=p_lvld_ppad_m1bounds, right=lvld_n_m1_bounds.right,
        ))

        _p_lvld_n_ppad_lay = layouter.wire_layout(
            net=nets.lvld_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _p_lvld_n_ppad_polybounds = _p_lvld_n_ppad_lay.bounds(mask=poly.mask)
        _p_lvld_n_ppad_m1bounds = _p_lvld_n_ppad_lay.bounds(mask=metal1.mask)
        p_lvld_n_ppad_x = min(
            lvld_n_m1_bounds.left - metal1.min_space - _p_lvld_n_ppad_m1bounds.right,
            p_lvld_n_polybounds.left - _p_lvld_n_ppad_polybounds.left,
            p_lvld_n_polybounds.right - _p_lvld_n_ppad_polybounds.right,
        )
        p_lvld_n_ppad_y = (
            p_lvld_ppad_m1bounds.top + metal1.min_space - _p_lvld_n_ppad_m1bounds.bottom
        )
        p_lvld_n_ppad_lay = layouter.place(
            object_=_p_lvld_n_ppad_lay, x=p_lvld_n_ppad_x, y=p_lvld_n_ppad_y,
        )
        p_lvld_n_ppad_polybounds = p_lvld_n_ppad_lay.bounds(mask=poly.mask)
        p_lvld_n_ppad_m1bounds = p_lvld_n_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld, wire=poly, shape=_geo.Rect.from_rect(
            rect=p_lvld_n_polybounds, top=p_lvld_n_ppad_polybounds.top,
        ))
        layouter.add_wire(net=nets.lvld, wire=metal1, shape=_geo.Rect.from_rect(
            rect=p_lvld_n_ppad_m1bounds, left=lvld_m1_bounds.left,
        ))

        # Output buffer
        active_left = (
            max(nch_lvld_n_actbounds.right, pch_lvld_n_actbounds.right)
            + comp.min_oxactive_space
        )

        # Place left source-drain contacts
        _obuf_chiovss_lay = layouter.wire_layout(
            net=nets.vss, wire=contact, bottom_height=comp.maxionmos_w,
            bottom=active, bottom_implant=ionimplant,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _obuf_chiovss_actbounds = _obuf_chiovss_lay.bounds(mask=active.mask)
        obuf_chiovss_x = active_left - _obuf_chiovss_actbounds.left
        obuf_chiovss_y = comp.maxionmos_y
        obuf_chiovss_lay = layouter.place(
            object_=_obuf_chiovss_lay, x=obuf_chiovss_x, y=obuf_chiovss_y,
        )
        obuf_chiovss_chbounds = obuf_chiovss_lay.bounds(mask=contact.mask)
        obuf_chiovss_m1bounds = obuf_chiovss_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.vss, wire=metal1, shape=_geo.Rect.from_rect(
            rect=obuf_chiovss_m1bounds, top=spec.iorow_height,
        ))
        _obuf_chiovdd_lay = layouter.wire_layout(
            net=nets.iovdd, well_net=nets.iovdd, wire=contact,
            bottom_height=comp.maxiopmos_w,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
        )
        _obuf_chiovdd_actbounds = _obuf_chiovdd_lay.bounds(mask=active.mask)
        obuf_chiovdd_x = active_left - _obuf_chiovdd_actbounds.left
        obuf_chiovdd_y = comp.maxiopmos_y
        obuf_chiovdd_lay = layouter.place(
            object_=_obuf_chiovdd_lay, x=obuf_chiovdd_x, y=obuf_chiovdd_y,
        )
        obuf_chiovdd_chbounds = obuf_chiovdd_lay.bounds(mask=contact.mask)
        obuf_chiovdd_m1bounds = obuf_chiovdd_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.iovdd, wire=metal1, shape=_geo.Rect.from_rect(
            rect=obuf_chiovdd_m1bounds, bottom=0.0,
        ))

        poly_left = max(
            obuf_chiovss_chbounds.right + spec.ionmos.computed.min_contactgate_space,
            obuf_chiovdd_chbounds.right + spec.iopmos.computed.min_contactgate_space,
        )

        # Output buffer ionmos+iopmos
        x = obuf_chiovss_m1bounds.center.x + max(
            comp.minionmos_contactgatepitch,
            comp.miniopmos_contactgatepitch,
        )
        _n_obuf_lay = layouter.inst_layout(inst=insts.n_lvld_n_inv)
        _n_obuf_polybounds = _n_obuf_lay.bounds(mask=poly.mask)
        n_obuf_x = poly_left - _n_obuf_polybounds.left
        n_obuf_y = comp.maxionmos_y
        n_obuf_lay = layouter.place(
            object_=_n_obuf_lay, x=n_obuf_x, y=n_obuf_y
        )
        n_obuf_polybounds = n_obuf_lay.bounds(mask=poly.mask)
        _p_obuf_lay = layouter.inst_layout(inst=insts.p_lvld_n_inv)
        _p_obuf_polybounds = _p_obuf_lay.bounds(mask=poly.mask)
        p_obuf_x = poly_left - _p_obuf_polybounds.left
        p_obuf_y = comp.maxiopmos_y
        p_obuf_lay = layouter.place(object_=_p_obuf_lay, x=p_obuf_x, y=p_obuf_y)
        p_obuf_polybounds = p_obuf_lay.bounds(mask=poly.mask)
        layouter.add_wire(net=nets.lvld_n, wire=poly, shape=_geo.Rect.from_rect(
            rect=n_obuf_polybounds, bottom=p_obuf_polybounds.top,
        ))

        # poly pad
        _obuf_ppad_lay = layouter.wire_layout(
            net=nets.lvld_n, wire=contact, bottom=poly,
            bottom_enclosure="wide", top_enclosure="tall",
        )
        _obuf_ppad_polybounds = _obuf_ppad_lay.bounds(mask=poly.mask)
        obuf_ppad_x = min(
            n_obuf_polybounds.left - _obuf_ppad_polybounds.left,
            n_obuf_polybounds.right - _obuf_ppad_polybounds.right,
        )
        obuf_ppad_y = tech.on_grid(0.5*(n_obuf_polybounds.bottom + p_obuf_polybounds.top))
        obuf_ppad_lay = layouter.place(object_=_obuf_ppad_lay, x=obuf_ppad_x, y=obuf_ppad_y)
        obuf_ppad_m1bounds = obuf_ppad_lay.bounds(mask=metal1.mask)
        layouter.add_wire(net=nets.lvld_n, wire=metal1, shape=_geo.Rect.from_rect(
            rect=obuf_ppad_m1bounds, left=nch_lvld_n_m1bounds.left,
        ))

        # Place right source-drain contacts
        _nch_o_lay = layouter.wire_layout(
            net=nets.o, wire=contact, bottom_height=comp.maxionmos_w,
            bottom=active, bottom_implant=ionimplant,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _nch_o_chbounds = _nch_o_lay.bounds(mask=contact.mask)
        nch_o_x = (
            n_obuf_polybounds.right + spec.ionmos.computed.min_contactgate_space
            - _nch_o_chbounds.left
        )
        nch_o_y = comp.maxionmos_y
        nch_o_lay = layouter.place(object_=_nch_o_lay, x=nch_o_x, y=nch_o_y)
        nch_o_m1bounds = nch_o_lay.bounds(mask=metal1.mask)
        _pch_o_lay = layouter.wire_layout(
            net=nets.o, well_net=nets.iovdd, wire=contact, bottom_height=comp.maxiopmos_w,
            bottom=active, bottom_implant=iopimplant, bottom_well=nwell,
            bottom_enclosure="tall", top_enclosure="tall",
        )
        _pch_o_chbounds = _pch_o_lay.bounds(mask=contact.mask)
        pch_o_x = (
            p_obuf_polybounds.right + spec.iopmos.computed.min_contactgate_space
            - _pch_o_chbounds.left
        )
        pch_o_y = comp.maxiopmos_y
        pch_o_lay = layouter.place(object_=_pch_o_lay, x=pch_o_x, y=pch_o_y)
        pch_o_m1bounds = pch_o_lay.bounds(mask=metal1.mask)
        m1_o_lay = layouter.add_wire(net=nets.o, wire=metal1, shape=_geo.Rect.from_rect(
            rect=nch_o_m1bounds, bottom=pch_o_m1bounds.bottom,
        ))
        m1_o_bounds = m1_o_lay.bounds()
        _via1_o_lay = layouter.wire_layout(
            net=nets.o, wire=via1, bottom_height=m1_o_bounds.height
        )
        _via1_o_m1bounds = _via1_o_lay.bounds(mask=metal1.mask)
        via1_o_x = m1_o_bounds.left - _via1_o_m1bounds.left
        via1_o_y = m1_o_bounds.bottom - _via1_o_m1bounds.bottom
        via1_o_lay = layouter.place(object_=_via1_o_lay, x=via1_o_x, y=via1_o_y)
        via1_o_m2bounds = via1_o_lay.bounds(mask=metal2.mask)
        layouter.add_wire(net=nets.o, wire=metal2, **pin_args, shape=via1_o_m2bounds) # pyright: ignore

        cells_right = layout.bounds(mask=active.mask).right + 0.5*comp.min_oxactive_space

        # fill implants
        if nimplant is not None:
            bb = n_obuf_lay.bounds(mask=nimplant.mask)
            layouter.add_portless(
                prim=nimplant, shape=_geo.Rect(
                    left=0.0, bottom=bb.bottom,
                    right=cells_right, top=bb.top,
                ),
            )
        if pimplant is not None:
            bb = p_obuf_lay.bounds(mask=pimplant.mask)
            layouter.add_portless(
                prim=pimplant, shape=_geo.Rect(
                    left=0.0, bottom=bb.bottom,
                    right=cells_right, top=bb.top,
                ),
            )

        #
        # Set boundary
        #

        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=cells_right, top=spec.cells_height,
        )

        #
        # Well/bulk contacts
        #

        l1 = layouter.add_wire(
            net=nets.iovdd, wire=contact, well_net=nets.iovdd,
            bottom=active, bottom_implant=ionimplant, bottom_well=nwell,
            top_enclosure=comp.chm1_enclosure.wide(),
            x=0.5*cells_right, bottom_width=(cells_right - contact.min_space),
            y=0, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        bb1 = l1.bounds(mask=nwell.mask)
        l2 = layouter.add_wire(
            net=nets.iovdd, wire=active, implant=ionimplant,
            well_net=nets.iovdd, well=nwell,
            x=0.5*cells_right, width=cells_right,
            y=0, height=comp.minwidth_activewithcontact,
        )
        bb2 = l2.bounds(mask=nwell.mask)
        shape = _geo.Rect(
            left=min(bb1.left, bb2.left),
            bottom=min(bb1.bottom, bb2.bottom),
            right=max(bb1.right, bb2.right),
            top=spec.iorow_nwell_height,
        )
        layouter.add_wire(net=nets.iovdd, wire=nwell, shape=shape)
        layouter.add_wire(
            net=nets.iovdd, wire=metal1, pin=metal1pin,
            x=0.5*cells_right, width=cells_right,
            y=0, height=comp.metal[1].minwidth_updown,
        )

        layouter.add_wire(
            net=nets.vss, wire=contact, bottom=active,
            bottom_implant=pimplant, top_enclosure=comp.chm1_enclosure.wide(),
            x=0.5*cells_right, bottom_width=(cells_right - contact.min_space),
            y=spec.iorow_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        layouter.add_wire(
            net=nets.vss, wire=active, implant=pimplant,
            x=0.5*cells_right, width=cells_right,
            y=spec.iorow_height, height=comp.minwidth_activewithcontact,
        )
        layouter.add_wire(
            net=nets.vss, wire=metal1, pin=metal1pin,
            x=0.5*cells_right, width=cells_right,
            y=spec.iorow_height, height=comp.metal[1].minwidth_updown,
        )

        l1 = layouter.add_wire(
            net=nets.vdd, well_net=nets.vdd, wire=contact, bottom=active,
            bottom_implant=nimplant, bottom_well=nwell,
            top_enclosure=comp.chm1_enclosure.wide(),
            x=0.5*cells_right, bottom_width=(cells_right - contact.min_space),
            y=spec.cells_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        bb1 = l1.bounds(mask=nwell.mask)
        l2 = layouter.add_wire(
            net=nets.vdd, well_net=nets.vdd, wire=active,
            implant=nimplant, well=nwell,
            x=0.5*cells_right, width=cells_right,
            y=spec.cells_height, height=comp.minwidth_activewithcontact,
        )
        bb2 = l2.bounds(mask=nwell.mask)
        layouter.add_wire(
            net=nets.vdd, wire=metal1, pin=metal1pin,
            x=0.5*cells_right, width=cells_right,
            y=spec.cells_height, height=comp.metal[1].minwidth_updown,
        )
        shape = _geo.Rect(
            left=min(bb1.left, bb2.left),
            bottom=(spec.cells_height - spec.corerow_nwell_height),
            right=max(bb1.right, bb2.right),
            top=max(bb1.top, bb2.top),
        )
        layouter.add_wire(net=nets.vdd, wire=nwell, shape=shape)

        # Thick oxide
        assert comp.ionmos.gate.oxide is not None
        layouter.add_portless(prim=comp.ionmos.gate.oxide, shape=_geo.Rect(
            left=-actox_enc, bottom=comp.io_oxidebottom,
            right=(cells_right + actox_enc), top=comp.io_oxidetop,
        ))


class _LevelDown(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="LevelDown")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        circuit = self.new_circuit()

        # inverter with 5V gates
        n_hvinv = circuit.instantiate(
            spec.ionmos, name="n_hvinv", w=comp.maxionmoscore_w,
        )
        p_hvinv = circuit.instantiate(
            spec.iopmos, name="p_hvinv", w=comp.maxiopmoscore_w,
        )

        # second inverter, keep same w
        n_lvinv = circuit.instantiate(
            spec.nmos, name="n_lvinv", w=comp.maxnmos_w,
        )
        p_lvinv = circuit.instantiate(
            spec.pmos, name="p_lvinv", w=comp.maxpmos_w,
        )

        prot = circuit.instantiate(fab.get_cell("SecondaryProtection"), name="secondprot")

        # Create the nets
        circuit.new_net(name="vdd", external=True, childports=(
            p_hvinv.ports.sourcedrain1, p_hvinv.ports.bulk,
            p_lvinv.ports.sourcedrain2, p_lvinv.ports.bulk,
        ))
        circuit.new_net(name="vss", external=True, childports=(
            n_hvinv.ports.sourcedrain1, n_hvinv.ports.bulk,
            n_lvinv.ports.sourcedrain2, n_lvinv.ports.bulk,
        ))
        circuit.new_net(name="iovdd", external=True, childports=(
            prot.ports.iovdd,
        ))
        circuit.new_net(name="iovss", external=True, childports=(
            prot.ports.iovss,
        ))
        circuit.new_net(name="pad", external=True, childports=(
            prot.ports.pad,
        ))
        circuit.new_net(name="padres", external=False, childports=(
            prot.ports.core,
            n_hvinv.ports.gate, p_hvinv.ports.gate,
        ))
        circuit.new_net(name="padres_n", external=False, childports=(
            n_hvinv.ports.sourcedrain2, p_hvinv.ports.sourcedrain2,
            n_lvinv.ports.gate, p_lvinv.ports.gate,
        ))
        circuit.new_net(name="core", external=True, childports=(
            n_lvinv.ports.sourcedrain1, p_lvinv.ports.sourcedrain1,
        ))

    def _create_layout(self):
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed

        circuit = self.circuit
        insts = circuit.instances
        nets = circuit.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        oxide = comp.oxide
        nwell = comp.nwell
        poly = comp.poly
        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        contact = comp.contact
        chm1_enclosure = contact.min_top_enclosure[0]
        via1 = comp.vias[1]

        layouter = self.new_circuitlayouter()
        layout = self.layout

        left = 0.5*comp.active.min_space

        # Place instances
        #

        # transistors + contacts
        l = layouter.transistors_layout(trans_specs=(
            _lay.MOSFETInstSpec(
                inst=cast(_ckt._PrimitiveInstance, insts.n_lvinv),
                contact_left=contact, contact_right=contact,
            ),
        ))
        act_left = l.bounds(mask=active.mask).left
        l_n_lvinv = layouter.place(l, x=(left - act_left), y=comp.maxnmos_y)

        l = layouter.transistors_layout(trans_specs=(
            _lay.MOSFETInstSpec(
                inst=cast(_ckt._PrimitiveInstance, insts.p_lvinv),
                contact_left=contact, contact_right=contact,
            ),
        ))
        act_left = l.bounds(mask=active.mask).left
        l_p_lvinv = layouter.place(l, x=(left - act_left), y=comp.maxpmos_y)

        rect1 = l_n_lvinv.bounds(mask=active.mask)
        rect2 = l_p_lvinv.bounds(mask=active.mask)
        ox_left = (
            max(rect1.right, rect2.right)
            + tech.computed.min_space(oxide, active)
        )

        l = layouter.transistors_layout(trans_specs=(
            _lay.MOSFETInstSpec(
                inst=cast(_ckt._PrimitiveInstance, insts.n_hvinv),
                contact_left=contact, contact_right=contact,
            ),
        ))
        ox_left2 = l.bounds(mask=oxide.mask).left
        l_n_hvinv = layouter.place(l, x=(ox_left - ox_left2), y=comp.maxionmoscore_y)

        l = layouter.transistors_layout(trans_specs=(
            _lay.MOSFETInstSpec(
                inst=cast(_ckt._PrimitiveInstance, insts.p_hvinv),
                contact_left=contact, contact_right=contact,
            ),
        ))
        ox_left2 = l.bounds(mask=oxide.mask).left
        l_p_hvinv = layouter.place(l, x=(ox_left - ox_left2), y=comp.maxiopmoscore_y)

        # secondary protection
        l = layouter.inst_layout(inst=insts.secondprot)
        _actvdd_bounds = l.bounds(net=nets.iovdd, mask=active.mask)
        l_prot = layouter.place(
            l, x=0,
            y=(-_actvdd_bounds.top + 0.5*comp.minwidth_activewithcontact),
        )

        # Cell boundary
        #
        secprot = fab.get_cell("SecondaryProtection")
        assert secprot.layout.boundary is not None
        cell_width = tech.on_grid(
            max(
                layout.bounds(mask=active.mask).right + 0.5*active.min_space,
                secprot.layout.boundary.right,
            ),
            mult=2, rounding="ceiling",
        )
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=cell_width, top=spec.cells_height,
        )
        x_mid = 0.5*cell_width

        # Connect nets
        #

        # core
        net = nets.core # Output of lv inverter
        rect1 = l_n_lvinv.bounds(mask=metal1.mask, net=net)
        rect2 = l_p_lvinv.bounds(mask=metal1.mask, net=net)
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=_geo.Rect(
            left=min(rect1.left, rect2.left), bottom=rect1.bottom,
            right=max(rect1.right, rect2.right), top=rect2.top,
        ))

        # pad
        net = nets.pad
        rect = l_prot.bounds(net=net, mask=metal2pin.mask)
        layouter.add_wire(net=net, wire=metal2, pin=metal2pin, shape=rect)

        # padres
        net = nets.padres
        rect1 = l_n_hvinv.bounds(mask=poly.mask)
        rect2 = l_p_hvinv.bounds(mask=poly.mask)
        assert rect1.top < rect2.bottom
        layouter.add_wire(wire=poly, net=nets.padres, shape=_geo.Rect(
            left=min(rect1.left, rect2.left), bottom=rect1.top,
            right=max(rect1.right, rect2.right), top=rect2.bottom,
        ))
        l = layouter.wire_layout(
            net=net, wire=contact, bottom=poly, top_enclosure=chm1_enclosure.wide(),
        )
        rect3 = l.bounds(mask=poly.mask)
        x = max(rect1.right, rect2.right) - rect3.right
        y = tech.on_grid(0.5*(rect1.top + rect2.bottom))
        l_hv_ch = layouter.place(l, x=x, y=y)

        # y = y
        l = layouter.wire_layout(net=net, wire=via1, bottom_enclosure="wide")
        rect1 = l_hv_ch.bounds(mask=metal1.mask)
        rect2 = l.bounds(mask=metal1.mask)
        x = rect1.right - rect2.right
        l_hv_via1 = layouter.place(l, x=x, y=y)

        rect1 = l_hv_via1.bounds(mask=metal2.mask)
        rect2 = l_prot.bounds(net=net, mask=metal2pin.mask)
        assert rect1.left >= rect2.left
        l_m2_padres = layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=rect1, bottom=rect2.top,
        ))

        # padres_n
        net = nets.padres_n # Output of hv inverter
        rect1 = l_n_lvinv.bounds(mask=poly.mask)
        rect2 = l_p_lvinv.bounds(mask=poly.mask)
        assert rect1.top < rect2.bottom
        layouter.add_wire(wire=poly, net=nets.padres_n, shape=_geo.Rect(
            left=min(rect1.left, rect2.left), bottom=rect1.top,
            right=max(rect1.right, rect2.right), top=rect2.bottom,
        ))
        l = layouter.wire_layout(
            net=net, wire=contact, bottom=poly, top_enclosure=chm1_enclosure.wide(),
        )
        rect3 = l.bounds(mask=poly.mask)
        x = max(rect1.right, rect2.right) - rect3.left
        y = tech.on_grid(0.5*(rect1.top + rect2.bottom))
        l_lv_ch = layouter.place(object_=l, x=x, y=y)

        rect1 = l_lv_ch.bounds(mask=metal1.mask)
        l = layouter.wire_layout(net=net, wire=via1, bottom_enclosure="wide")
        rect2 = l.bounds(mask=metal1.mask)
        x = rect1.right - rect2.right
        # y = y
        l_lv_via1 = layouter.place(l, x=x, y=y)

        rect1 = l_n_hvinv.bounds(mask=metal1.mask, net=net)
        rect2 = l_p_hvinv.bounds(mask=metal1.mask, net=net)
        left = min(rect1.right, rect2.right)
        right = left + metal1.min_space
        bottom = rect1.bottom
        top = rect2.top
        l_hv_m1 = layouter.add_wire(net=net, wire=metal1, shape=_geo.Rect(
            left=left, bottom=bottom, right=right, top=top,
        ))

        m1rect1 = l_hv_m1.bounds(mask=metal1.mask)
        m2rect1 = l_lv_via1.bounds(mask=metal2.mask)
        m2rect2 = l_m2_padres.bounds(mask=metal2.mask)
        l = layouter.wire_layout(net=net, wire=via1)
        m1rect2 = l.bounds(mask=metal1.mask)
        m2rect3 = l.bounds(mask=metal2.mask)
        x = m1rect1.left - m1rect2.left
        y = (m2rect2.top + metal2.min_space) - m2rect3.bottom
        l_via1 = layouter.place(l, x=x, y=y)
        m2rect3 = l_via1.bounds(mask=metal2.mask)
        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=m2rect1, top=m2rect3.top,
        ))
        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=m2rect3, left=m2rect1.left,
        ))

        # Increase metal1 area for padres & padres_n poly pad connections
        rect1 = l_lv_via1.bounds(mask=metal1.mask)
        rect2 = l_hv_via1.bounds(mask=metal1.mask)
        mid = 0.5*(rect1.right + rect2.left)
        right = tech.on_grid(mid - 0.5*metal1.min_space, rounding="floor")
        shape = _geo.Rect.from_rect(rect=rect1, right=right)
        layouter.add_wire(net=nets.padres_n, wire=metal1, shape=shape)
        left = tech.on_grid(mid + 0.5*metal1.min_space, rounding="ceiling")
        shape = _geo.Rect.from_rect(rect=rect2, left=left)
        layouter.add_wire(net=nets.padres, wire=metal1, shape=shape)

        # vss
        net = nets.vss
        layouter.add_wire(
            net=net, wire=contact, bottom=active,
            bottom_implant=pimplant, top_enclosure=comp.chm1_enclosure.wide(),
            x=x_mid, bottom_width=(cell_width - contact.min_space),
            y=spec.iorow_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        layouter.add_wire(
            net=net, wire=active, implant=pimplant,
            x=x_mid, width=cell_width,
            y=spec.iorow_height, height=comp.minwidth_activewithcontact,
        )
        layouter.add_wire(
            net=net, wire=metal1, pin=metal1pin,
            x=x_mid, width=cell_width,
            y=spec.iorow_height, height=comp.metal[1].minwidth_updown,
        )

        rect1 = l_n_lvinv.bounds(net=net, mask=metal1.mask)
        rect2 = l_n_hvinv.bounds(net=net, mask=metal1.mask)
        layouter.add_wire(net=net, wire=metal1, shape=_geo.Rect(
            left=rect1.left, bottom=spec.iorow_height,
            right=rect2.right, top=min(rect1.top, rect2.top),
        ))

        # vdd
        net = nets.vdd
        l = layouter.add_wire(
            net=net, well_net=net, wire=contact, bottom=active,
            bottom_implant=nimplant, bottom_well=nwell,
            top_enclosure=comp.chm1_enclosure.wide(),
            x=x_mid, bottom_width=(cell_width - contact.min_space),
            y=spec.cells_height, bottom_height=comp.minwidth_activewithcontact,
            bottom_enclosure=comp.chact_enclosure.wide(),
        )
        l = layouter.add_wire(
            net=net, well_net=net, wire=active,
            implant=nimplant, well=nwell,
            x=x_mid, width=cell_width,
            y=spec.cells_height, height=comp.minwidth_activewithcontact,
        )
        layouter.add_wire(
            net=net, wire=metal1, pin=metal1pin,
            x=x_mid, width=cell_width,
            y=spec.cells_height, height=comp.metal[1].minwidth_updown,
        )
        strap_vdd_nwellbounds = l.bounds(mask=nwell.mask)
        shape = _geo.Rect.from_rect(
            rect=strap_vdd_nwellbounds,
            bottom=(spec.cells_height - spec.corerow_nwell_height),
        )
        layouter.add_wire(net=net, wire=nwell, shape=shape)

        rect1 = l_p_lvinv.bounds(net=net, mask=metal1.mask)
        rect2 = l_p_hvinv.bounds(net=net, mask=metal1.mask)
        layouter.add_wire(net=net, wire=metal1, shape=_geo.Rect(
            left=rect1.left, bottom=max(rect1.bottom, rect2.bottom),
            right=rect2.right, top=spec.cells_height,
        ))

        # iovss
        net = nets.iovss
        rect = l_prot.bounds(net=net, mask=metal2pin.mask)
        layouter.add_wire(net=net, wire=metal2, pin=metal2pin, shape=rect)

        # iovdd
        layouter.add_wire(
            net=nets.iovdd, wire=metal1, pin=metal1pin,
            x=x_mid, width=cell_width,
            y=0, height=comp.metal[1].minwidth_updown,
        )

        # Netless polygons
        #

        # Join transistor implant layers
        if nimplant is not None:
            n_lvinv_implbounds = l_n_lvinv.bounds(mask=nimplant.mask)
            n_hvinv_implbounds = l_n_hvinv.bounds(mask=nimplant.mask)
            shape = _geo.Rect.from_rect(rect=n_lvinv_implbounds, right=n_hvinv_implbounds.right)
            layouter.add_portless(prim=nimplant, shape=shape)

        if pimplant is not None:
            p_lvinv_implbounds = l_p_lvinv.bounds(mask=pimplant.mask)
            p_hvinv_implbounds = l_p_hvinv.bounds(mask=pimplant.mask)
            shape = _geo.Rect.from_rect(rect=p_lvinv_implbounds, right=p_hvinv_implbounds.right)
            layouter.add_portless(prim=pimplant, shape=shape)

        # Join transistor oxide layer
        bounds = layout.bounds(mask=oxide.mask)
        layouter.add_portless(prim=oxide, shape=bounds)


class _TrackConn(_FactoryOnDemandCell):
    def __init__(
        self, *, fab: "IOFactory", name: str,
        cell_width: float,
    ):
        super().__init__(fab=fab, name=name)

        self.cell_width = cell_width

    def _create_circuit(self):
        ckt = self.new_circuit()

        ckt.new_net(name="vdd", external=True)
        ckt.new_net(name="vss", external=True)
        ckt.new_net(name="iovdd", external=True)
        ckt.new_net(name="iovss", external=True)

    def _create_layout(self):
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed
        frame = fab.frame

        cell_width = self.cell_width

        nets = self.circuit.nets

        active = comp.active
        nimplant = comp.nimplant
        pimplant = comp.pimplant
        nwell = comp.nwell
        contact = comp.contact
        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        via1 = comp.vias[1]
        metal2 = comp.metal[2].prim
        via2 = comp.vias[2]
        metal3 = comp.metal[3].prim

        iovdd_trackspec = frame.track_specs["iovdd"]

        layouter = self.new_circuitlayouter()
        layout = self.layout

        c_pclamp = fab.clamp(type_="p", n_trans=spec.clampcount, n_drive=spec.clampdrive)
        _l_pclamp = c_pclamp.layout
        clact_bounds = _l_pclamp.bounds(mask=active.mask)
        clm1_bounds = _l_pclamp.bounds(mask=metal1.mask)

        # iovdd
        net = nets.iovdd
        _l_ch = layouter.fab.layout_primitive(
            prim=contact, portnets={"conn": net}, well_net=net,
            bottom=active, bottom_implant=nimplant, bottom_well=nwell,
            columns=8, bottom_enclosure="wide", top_enclosure="wide",
        )
        _act_bounds = _l_ch.bounds(mask=active.mask)
        y = 0.0
        x = 0.5*cell_width

        x = -_act_bounds.left + contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        x = cell_width - x
        layouter.place(_l_ch, x=x, y=y)

        _l_via = layouter.fab.layout_primitive(
            prim=via1, portnets={"conn": net}, columns=2,
        )
        _m2_bounds = _l_via.bounds(mask=metal2.mask)
        x = cell_width - _m2_bounds.right - metal2.min_space
        l = layouter.place(_l_via, x=x, y=y)
        m2_bounds1 = l.bounds(mask=metal2.mask)
        _l_via = layouter.fab.layout_primitive(
            prim=via2, portnets={"conn": net}, columns=2,
        )
        _m2_bounds = _l_via.bounds(mask=metal2.mask)
        track_spec = frame.framespec._track_specs_dict["iovdd"]
        metal_spec = comp.metal[3]
        track_m3top = track_spec.top - 0.5*metal_spec.tracksegment_space
        y = track_m3top - _m2_bounds.top - frame.cells_y
        l = layouter.place(_l_via, x=x, y=y)
        m2_bounds2 = l.bounds(mask=metal2.mask)
        iovdd_m2bb = shape = _geo.Rect.from_rect(rect=m2_bounds2, top=m2_bounds1.top)
        layouter.add_wire(wire=metal2, net=net, shape=shape)

        # vss
        net = nets.vss
        _l_ch = layouter.fab.layout_primitive(
            prim=contact, portnets={"conn": net},
            bottom=active, bottom_implant=pimplant,
            columns=8, bottom_enclosure="wide", top_enclosure="wide",
        )
        _act_bounds = _l_ch.bounds(mask=active.mask)
        y = spec.iorow_height
        x = -_act_bounds.left + contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        x = cell_width - _act_bounds.right - contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        _l_via = layouter.fab.layout_primitive(
            prim=via1, portnets={"conn": net}, columns=8,
        )
        _m2_bounds = _l_via.bounds(mask=metal2.mask)
        x = -_m2_bounds.left + metal2.min_space
        layouter.place(_l_via, x=x, y=y)
        x = cell_width -_m2_bounds.right - metal2.min_space
        layouter.place(_l_via, x=x, y=y)
        _l_via = layouter.fab.layout_primitive(
            prim=via2, portnets={"conn": net}, columns=8,
        )
        _m3_bounds = _l_via.bounds(mask=metal3.mask)
        x = -_m3_bounds.left + metal3.min_space
        layouter.place(_l_via, x=x, y=y)
        x = cell_width - x
        layouter.place(_l_via, x=x, y=y)

        # vdd
        net = nets.vdd
        _l_ch = layouter.fab.layout_primitive(
            prim=contact, portnets={"conn": net}, well_net=net,
            bottom=active, bottom_implant=nimplant, bottom_well=nwell,
            columns=8, bottom_enclosure="wide", top_enclosure="wide",
        )
        _act_bounds = _l_ch.bounds(mask=active.mask)
        y = spec.cells_height
        x = -_act_bounds.left + contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        x = cell_width - _act_bounds.right- contact.min_space
        layouter.place(_l_ch, x=x, y=y)
        _l_via = layouter.fab.layout_primitive(
            prim=via1, portnets={"conn": net}, columns=8,
        )
        _m2_bounds = _l_via.bounds(mask=metal2.mask)
        x = -_m2_bounds.left + metal2.min_space
        layouter.place(_l_via, x=x, y=y)
        x = cell_width -_m2_bounds.right - metal2.min_space
        layouter.place(_l_via, x=x, y=y)
        _l_via = layouter.fab.layout_primitive(
            prim=via2, portnets={"conn": net}, columns=8,
        )
        _m3_bounds = _l_via.bounds(mask=metal3.mask)
        x = -_m3_bounds.left + metal3.min_space
        layouter.place(_l_via, x=x, y=y)
        x = cell_width - x
        layouter.place(_l_via, x=x, y=y)

        # iovss
        net = nets.iovss
        left = 0.0
        right = cell_width
        act_bottom = iovdd_trackspec.bottom + clact_bounds.top - frame.cells_y
        track_spec = frame.framespec._track_specs_dict["iovdd"]
        m1_bottom = track_spec.bottom + clm1_bounds.top - frame.cells_y
        # secondary protection is put below iorow cells
        act_top = frame._track_segments["actiovss"][-1].top - frame.cells_y
        # active and metal1 edge overlap in secondary protection cell
        m1_top = act_top

        shape = _geo.Rect(
            left=left, bottom=act_bottom, right=right, top=act_top,
        )
        layouter.add_wire(net=net, wire=active, implant=pimplant, shape=shape)

        bottom_shape = _geo.Rect(
            left=(left + contact.min_space),
            right=(right - contact.min_space),
            bottom=(act_bottom + contact.min_space),
            top=(act_top - contact.min_space),
        )
        xy = tech.on_grid(bottom_shape.center)
        w = tech.on_grid(bottom_shape.width, mult=2, rounding="floor")
        h = tech.on_grid(bottom_shape.height, mult=2, rounding="floor")
        layouter.add_wire(
            net=net, wire=contact, bottom=active, bottom_implant=pimplant,
            origin=xy, space=2*contact.min_space,
            bottom_width=w, bottom_height=h,
        )
        shape = _geo.Rect(
            left=left, bottom=m1_bottom, right=right, top=m1_top,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)
        if frame.has_secondiovss:
            iovss2_trackspec = frame.track_specs["secondiovss"]

            # We assume bottom tracl metal is metal3
            assert comp.metal[3].prim == comp.track_metalspecs[0].prim

            # Take space of the bottom layer of the track layers as segment space
            # draw after full height of the segment, even when
            metal_space = comp.track_metalspecs[0].tracksegment_space
            y = iovss2_trackspec.center - frame.cells_y
            height = iovss2_trackspec.top - iovss2_trackspec.bottom - metal_space

            _lay = layouter.wire_layout(
                net=net, wire=via1, columns=10,
                bottom_height=height, bottom_enclosure="wide",
                top_height=height, top_enclosure="wide",
            )
            _m2_bb = _lay.bounds(mask=metal2.mask)
            x = metal2.min_space - _m2_bb.left
            layouter.place(_lay, x=x, y=y)
            x = iovdd_m2bb.left - 2*metal2.min_space - _m2_bb.right
            layouter.place(_lay, x=x, y=y)

            _lay = layouter.wire_layout(
                net=net, wire=via2, columns=10,
                bottom_height=height, bottom_enclosure="wide",
                top_height=height, top_enclosure="wide",
            )
            _m2_bb = _lay.bounds(mask=metal2.mask)
            x = metal2.min_space - _m2_bb.left
            layouter.place(_lay, x=x, y=y)
            x = iovdd_m2bb.left - 2*metal2.min_space - _m2_bb.right
            layouter.place(_lay, x=x, y=y)

        bb = layout.bounds()
        layout.boundary = _geo.Rect(
            left=0.0, bottom=bb.bottom, right=cell_width, top=bb.top,
        )


class _GateLevelUp(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="GateLevelUp")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec

        levelup = fab.get_cell("LevelUp")

        ckt = self.new_circuit()

        ngatelu = ckt.instantiate(levelup, name="ngate_levelup")
        pgatelu = ckt.instantiate(levelup, name="pgate_levelup")

        ckt.new_net(name="vdd", external=True, childports=(
            ngatelu.ports.vdd, pgatelu.ports.vdd,
        ))
        ckt.new_net(name="vss", external=True, childports=(
            ngatelu.ports.vss, pgatelu.ports.vss,
        ))
        ckt.new_net(name="iovdd", external=True, childports=(
            ngatelu.ports.iovdd, pgatelu.ports.iovdd,
        ))

        ckt.new_net(name="core", external=True, childports=(
            ngatelu.ports.i, pgatelu.ports.i,
        ))
        ckt.new_net(name="ngate", external=True, childports=(ngatelu.ports.o))
        ckt.new_net(name="pgate", external=True, childports=(pgatelu.ports.o))

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed

        insts = self.circuit.instances
        nets = self.circuit.nets

        levelup = fab.get_cell("LevelUp")
        assert levelup.layout.boundary is not None

        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        layouter = self.new_circuitlayouter()
        fab = layouter.fab
        layout = self.layout

        # Place the cells
        x_lu = 0.0
        y_lu = -levelup.layout.boundary.top - spec.levelup_core_space
        l_ngatelu = layouter.place(insts.ngate_levelup, x=x_lu, y=y_lu)
        ngatelu_d_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.core)
        ngatelu_ngate_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.ngate)
        ngatelu_bb = l_ngatelu.boundary
        assert ngatelu_bb is not None

        x_lu = ngatelu_bb.right
        l_pgatelu = layouter.place(insts.pgate_levelup, x=x_lu, y=y_lu)
        pgatelu_d_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.core)
        pgatelu_pgate_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.pgate)
        pgatelu_bb = l_pgatelu.boundary
        assert pgatelu_bb is not None

        # Set the boundary
        cell_bb = _geo.Rect.from_rect(rect=ngatelu_bb, right=pgatelu_bb.right)
        layout.boundary = cell_bb

        # Connect the nets
        # core
        net = nets.core

        shape = _geo.Rect.from_rect(rect=ngatelu_d_m2pinbounds, top=cell_bb.top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(rect=pgatelu_d_m2pinbounds, top=cell_bb.top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=ngatelu_d_m2pinbounds.left, bottom=cell_bb.top,
            right=pgatelu_d_m2pinbounds.right, top=(cell_bb.top + 2*metal2.min_width),
        )
        layouter.add_wire(net=net, wire=metal2, pin=metal2pin, shape=shape)

        # ngate
        net = nets.ngate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=ngatelu_ngate_m2pinbounds,
        )

        # pgate
        net = nets.pgate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=pgatelu_pgate_m2pinbounds,
        )

        # vss
        net = nets.vss
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_bb.left, right=cell_bb.right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)

        # vdd
        net = nets.vdd
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_bb.left, right=cell_bb.right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)

        # iovdd
        net = nets.iovdd
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_bb.left, right=cell_bb.right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)


class _GateDecode(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="GateDecode")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        stdcells = spec.stdcelllib.cells

        tie = stdcells.tie
        inv = stdcells.inv_x1
        nand = stdcells.nand2_x1
        nor = stdcells.nor2_x1
        levelup = fab.get_cell("LevelUp")

        ckt = self.new_circuit()

        tieinst = ckt.instantiate(tie, name="tieinst")
        eninv = ckt.instantiate(inv, name="en_inv")
        ngatenor = ckt.instantiate(nor, name="ngate_nor")
        ngatelu = ckt.instantiate(levelup, name="ngate_levelup")
        pgatenand = ckt.instantiate(nand, name="pgate_nand")
        pgatelu = ckt.instantiate(levelup, name="pgate_levelup")

        ckt.new_net(name="vdd", external=True, childports=(
            tieinst.ports.vdd, eninv.ports.vdd, ngatenor.ports.vdd, ngatelu.ports.vdd,
            pgatenand.ports.vdd, pgatelu.ports.vdd,
        ))
        ckt.new_net(name="vss", external=True, childports=(
            tieinst.ports.vss, eninv.ports.vss, ngatenor.ports.vss, ngatelu.ports.vss,
            pgatenand.ports.vss, pgatelu.ports.vss,
        ))
        ckt.new_net(name="iovdd", external=True, childports=(
            ngatelu.ports.iovdd, pgatelu.ports.iovdd,
        ))

        ckt.new_net(name="core", external=True, childports=(
            ngatenor.ports.i0, pgatenand.ports.i0,
        ))
        ckt.new_net(name="en", external=True, childports=(
            eninv.ports.i, pgatenand.ports.i1,
        ))
        ckt.new_net(name="en_n", external=False, childports=(
            eninv.ports.nq, ngatenor.ports.i1,
        ))
        ckt.new_net(name="ngate_core", external=False, childports=(
            ngatenor.ports.nq, ngatelu.ports.i,
        ))
        ckt.new_net(name="ngate", external=True, childports=(ngatelu.ports.o))
        ckt.new_net(name="pgate_core", external=False, childports=(
            pgatenand.ports.nq, pgatelu.ports.i,
        ))
        ckt.new_net(name="pgate", external=True, childports=(pgatelu.ports.o))

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        stdcells = spec.stdcelllib.cells
        comp = fab.computed

        insts = self.circuit.instances
        nets = self.circuit.nets

        tie = stdcells.tie
        assert tie.layout.boundary is not None
        levelup = fab.get_cell("LevelUp")
        assert levelup.layout.boundary is not None
        via1 = comp.vias[1]
        metal1 = comp.metal[1].prim
        metal1pin = metal1.pin
        metal2 = comp.metal[2].prim
        metal2pin = metal2.pin

        layouter = self.new_circuitlayouter()
        fab = layouter.fab
        layout = self.layout

        # Place the cells
        l_tie = layouter.place(insts.tieinst, x=0.0, y=0.0)
        assert l_tie.boundary is not None

        l_ngatenor = layouter.place(insts.ngate_nor, x=l_tie.boundary.right, y=0.0)
        assert l_ngatenor.boundary is not None
        ngatenor_d_m1pinbounds = l_ngatenor.bounds(mask=metal1pin.mask, net=nets.core)
        ngatenor_ngatecore_m1pinbounds = l_ngatenor.bounds(
            mask=metal1pin.mask, net=nets.ngate_core,
        )
        ngatenor_den_m1pinbounds = l_ngatenor.bounds(mask=metal1pin.mask, net=nets.en_n)
        l_pgatenand = layouter.place(
            insts.pgate_nand, x=l_ngatenor.boundary.right, y=0.0,
        )
        assert l_pgatenand.boundary is not None
        pgatenand_d_m1pinbounds = l_pgatenand.bounds(mask=metal1pin.mask, net=nets.core)
        pgatenand_pgatecore_m1pinbounds = l_pgatenand.bounds(
            mask=metal1pin.mask, net=nets.pgate_core,
        )
        pgatenand_de_m1pinbounds = l_pgatenand.bounds(mask=metal1pin.mask, net=nets.en)
        l_eninv = layouter.place(
            insts.en_inv, x=l_pgatenand.boundary.right, y=0.0,
        )
        assert l_eninv.boundary is not None
        eninv_de_m1pinbounds = l_eninv.bounds(mask=metal1pin.mask, net=nets.en)
        eninv_den_m1pinbounds = l_eninv.bounds(mask=metal1pin.mask, net=nets.en_n)

        y_lu = -levelup.layout.boundary.top - spec.levelup_core_space
        l_ngatelu = layouter.place(
            insts.ngate_levelup,
            x=tie.layout.boundary.right, y=y_lu,
        )
        ngatelu_ngatecore_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.ngate_core)
        ngatelu_ngate_m2pinbounds = l_ngatelu.bounds(mask=metal2pin.mask, net=nets.ngate)
        assert l_ngatelu.boundary is not None
        l_pgatelu = layouter.place(
            insts.pgate_levelup, x=l_ngatelu.boundary.right, y=y_lu
        )
        pgatelu_pgatecore_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.pgate_core)
        pgatelu_pgate_m2pinbounds = l_pgatelu.bounds(mask=metal2pin.mask, net=nets.pgate)
        assert l_pgatelu.boundary is not None

        # Set the boundary
        cell_left = 0.0
        cell_bottom = l_pgatelu.boundary.bottom
        cell_right = max(l_eninv.boundary.right, l_pgatelu.boundary.right)
        cell_top = l_eninv.boundary.top
        layout.boundary = _geo.Rect(
            left=cell_left, bottom=cell_bottom, right=cell_right, top=cell_top,
        )

        # Connect the nets
        # en
        net = nets.en
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        y = (
            min(pgatenand_de_m1pinbounds.top, eninv_de_m1pinbounds.top)
            - _m1bounds.top
        )
        l_via_pgatenand_de = layouter.place(
            object_=_l_via, x=pgatenand_de_m1pinbounds.center.x, y=y,
        )
        via_pgatenand_de_m2bounds = l_via_pgatenand_de.bounds(mask=metal2.mask)
        l_via_eninv_de = layouter.place(
            object_=_l_via, x=eninv_de_m1pinbounds.center.x, y=y,
        )
        via_eninv_de_m2bounds = l_via_eninv_de.bounds(mask=metal2.mask)

        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=via_pgatenand_de_m2bounds, right=via_eninv_de_m2bounds.right,
        ))
        shape = _geo.Rect(
            left=via_pgatenand_de_m2bounds.left,
            bottom=via_pgatenand_de_m2bounds.bottom,
            right=via_pgatenand_de_m2bounds.left + comp.metal[2].minwidth4ext_updown,
            top=l_eninv.boundary.top,
        )
        layouter.add_wire(net=net, wire=metal2, pin=metal2.pin, shape=shape)

        # core
        net = nets.core
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        _m2bounds = _l_via.bounds(mask=metal2.mask)
        y = (min(ngatenor_d_m1pinbounds.top, pgatenand_d_m1pinbounds.top) - _m1bounds.top)
        if pgatenand_d_m1pinbounds.center.x > pgatenand_de_m1pinbounds.center.x:
            y = min(
                y,
                (
                    min(via_pgatenand_de_m2bounds.bottom, via_eninv_de_m2bounds.bottom)
                    - metal2.min_space
                    - _m2bounds.top
                ),
            )
        l_via_ngatenor_d = layouter.place(
            object_=_l_via, x=ngatenor_d_m1pinbounds.center.x, y=y,
        )
        via_ngatenor_d_m2bounds = l_via_ngatenor_d.bounds(mask=metal2.mask)
        l_via_pgatenand_d = layouter.place(
            object_=_l_via, x=pgatenand_d_m1pinbounds.center.x, y=y,
        )
        via_pgatenand_d_m2bounds = l_via_pgatenand_d.bounds(mask=metal2.mask)

        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=via_ngatenor_d_m2bounds, right=via_pgatenand_d_m2bounds.right,
        ))
        shape = _geo.Rect(
            left=via_ngatenor_d_m2bounds.left,
            bottom=via_pgatenand_d_m2bounds.bottom,
            right=via_ngatenor_d_m2bounds.left + comp.metal[2].minwidth4ext_updown,
            top=l_eninv.boundary.top,
        )
        layouter.add_wire(net=net, wire=metal2, pin=metal2.pin, shape=shape)

        # en_n
        net = nets.en_n
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        _m2bounds = _l_via.bounds(mask=metal2.mask)
        y = min(
            (
                min(
                    via_ngatenor_d_m2bounds.bottom,
                    via_pgatenand_d_m2bounds.bottom,
                    via_pgatenand_de_m2bounds.bottom,
                )
                - metal2.min_space
                - _m2bounds.top
            ),
            (
                min(ngatenor_den_m1pinbounds.top, eninv_den_m1pinbounds.top)
                - _m1bounds.top
            ),
        )
        l_via_eninv_den = layouter.place(
            object_=_l_via, x=eninv_den_m1pinbounds.center.x, y=y,
        )
        via_eninv_den_m2bounds = l_via_eninv_den.bounds(mask=metal2.mask)
        if (y + _m1bounds.bottom + _geo.epsilon) > ngatenor_den_m1pinbounds.bottom:
            l_via_ngatenor_den = layouter.place(
                object_=_l_via, x=ngatenor_den_m1pinbounds.center.x, y=y,
            )
            via_ngatenor_den_m2bounds = l_via_ngatenor_den.bounds(mask=metal2.mask)

            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=via_ngatenor_den_m2bounds, right=via_eninv_den_m2bounds.right,
            ))
        else:
            y2 = ngatenor_den_m1pinbounds.bottom - _m1bounds.bottom

            l_via_ngatenor_den = layouter.place(
                object_=_l_via, x=ngatenor_den_m1pinbounds.center.x, y=y2,
            )
            via_ngatenor_den_m2bounds = l_via_ngatenor_den.bounds(mask=metal2.mask)

            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=via_ngatenor_den_m2bounds, bottom=via_eninv_den_m2bounds.bottom,
            ))
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=via_eninv_den_m2bounds, left=via_ngatenor_den_m2bounds.left,
            ))

        # ngate_core
        net = nets.ngate_core
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        _m2bounds = _l_via.bounds(mask=metal2.mask)
        x = ngatenor_ngatecore_m1pinbounds.left - _m1bounds.left
        y = ngatenor_ngatecore_m1pinbounds.bottom - _m1bounds.bottom
        l_via = layouter.place(object_=_l_via, x=x, y=y)
        m2bounds = l_via.bounds(mask=metal2.mask)
        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=ngatelu_ngatecore_m2pinbounds, top=m2bounds.top,
        ))
        if m2bounds.left < ngatelu_ngatecore_m2pinbounds.left:
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=m2bounds, right=ngatelu_ngatecore_m2pinbounds.right,
            ))
        else:
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=m2bounds, left=ngatelu_ngatecore_m2pinbounds.left,
            ))

        # pgate_core
        net = nets.pgate_core
        _l_via = layouter.wire_layout(
            net=net, wire=via1, bottom_enclosure="tall", top_enclosure="tall",
        )
        _m1bounds = _l_via.bounds(mask=metal1.mask)
        _m2bounds = _l_via.bounds(mask=metal2.mask)
        x = pgatenand_pgatecore_m1pinbounds.left - _m1bounds.left
        y = pgatenand_pgatecore_m1pinbounds.bottom - _m1bounds.bottom
        l_via = layouter.place(object_=_l_via, x=x, y=y)
        m2bounds = l_via.bounds(mask=metal2.mask)
        layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
            rect=pgatelu_pgatecore_m2pinbounds, top=m2bounds.top,
        ))
        if m2bounds.left < pgatelu_pgatecore_m2pinbounds.left:
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=m2bounds, right=pgatelu_pgatecore_m2pinbounds.right,
            ))
        else:
            layouter.add_wire(net=net, wire=metal2, shape=_geo.Rect.from_rect(
                rect=m2bounds, left=pgatelu_pgatecore_m2pinbounds.left,
            ))

        # ngate
        net = nets.ngate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=ngatelu_ngate_m2pinbounds,
        )

        # pgate
        net = nets.pgate
        layouter.add_wire(
            net=net, wire=metal2, pin=metal2pin, shape=pgatelu_pgate_m2pinbounds,
        )

        # vss
        net = nets.vss
        lum1pin_bounds = l_pgatelu.bounds(mask=metal1pin.mask, net=net)
        invm1pin_bounds = l_eninv.bounds(mask=metal1pin.mask, net=net)
        x = lum1pin_bounds.right - 0.5*comp.metal[1].minwidth4ext_up
        y = lum1pin_bounds.top
        l_via = layouter.add_wire(net=net, wire=via1, x=x, y=y)
        viam2_bounds1 = l_via.bounds(mask=metal2.mask)
        y = invm1pin_bounds.bottom + 0.5*comp.metal[1].minwidth4ext_up
        l_via = layouter.add_wire(net=net, wire=via1, x=x, y=y)
        viam2_bounds2 = l_via.bounds(mask=metal2.mask)
        shape = _geo.Rect.from_rect(rect=viam2_bounds1, top=viam2_bounds2.top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=invm1pin_bounds, left=cell_left, right=cell_right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)

        # vdd
        net = nets.vdd
        m1pin_bounds = l_eninv.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(
            rect=m1pin_bounds, left=cell_left, right=cell_right,
        )
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)
        x = cell_left + 0.5*comp.metal[1].minwidth4ext_up
        y = m1pin_bounds.bottom + 0.5*comp.metal[1].minwidth4ext_up
        l_via = layouter.add_wire(net=net, wire=via1, x=x, y=y)
        viam2_bounds1 = l_via.bounds(mask=metal2.mask)
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        y = m1pin_bounds.top - 0.5*comp.metal[1].minwidth4ext_up
        l_via = layouter.add_wire(net=net, wire=via1, x=x, y=y)
        viam2_bounds2 = l_via.bounds(mask=metal2.mask)
        viam1_bounds = l_via.bounds(mask=metal1.mask)
        shape = _geo.Rect.from_rect(rect=viam2_bounds1, bottom=viam2_bounds2.bottom)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(rect=m1pin_bounds, left=viam1_bounds.left)
        layouter.add_wire(net=net, wire=metal1, shape=shape)

        # iovdd
        net = nets.iovdd
        m1pin_bounds = l_ngatelu.bounds(net=net, mask=metal1pin.mask)
        shape = _geo.Rect.from_rect(rect=m1pin_bounds, left=cell_left, right=cell_right)
        layouter.add_wire(net=net, wire=metal1, pin=metal1pin, shape=shape)


class _PadOut(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="IOPadOut")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()

        frame.add_track_nets(ckt=ckt)
        frame.add_clamp_nets(ckt=ckt)

        c2p = ckt.new_net(name="c2p", external=True)
        pad = ckt.new_net(name="pad", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=spec.clampdrive, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=spec.clampdrive, pad=pad,
        )
        frame.add_trackconn_inst(ckt=ckt, width=spec.monocell_width, connect_up=True)

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        i_gatelu = ckt.instantiate(fab.get_cell("GateLevelUp"), name="gatelu")
        for name in ("vss", "vdd", "iovdd", "ngate", "pgate"):
            ckt.nets[name].childports += i_gatelu.ports[name]
        c2p.childports += i_gatelu.ports.core

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        frame = fab.frame
        comp = fab.computed

        metal = comp.metal
        metal2 = metal[2].prim
        metal2pin = metal2.pin

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.place_trackconn(layouter=layouter)

        # DC Diodes
        frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Gate levelup + interconnect
        _l_gatelu = layouter.inst_layout(inst=insts.gatelu)
        _gatelu_bb = _l_gatelu.boundary
        assert _gatelu_bb is not None
        dm2pin_bounds = _l_gatelu.bounds(net=nets.c2p, mask=metal2pin.mask)
        x = tech.on_grid(
            0.5*spec.monocell_width - 0.5*(dm2pin_bounds.left + dm2pin_bounds.right)
        )
        l_gatelu = layouter.place(
            _l_gatelu, x=x,
            y=(frame.cells_y - _gatelu_bb.bottom),
        )

        # c2p
        net = nets.c2p
        frame.promote_m2instpin_to_corepin(layouter=layouter, net=net, inst_layout=l_gatelu)

        # pgate
        net = nets.pgate
        m2pin_bounds1 = l_gatelu.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_pclamp.bounds(net=net, mask=metal2pin.mask)
        m2_width = comp.metal[2].minwidth4ext_updown
        bottom = cast(_geo._Rectangular, l_pclamp.boundary).top + 2*metal2.min_space
        y = bottom + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        top = bottom + m2_width
        shape = _geo.Rect(
            left=m2pin_bounds2.left, bottom=bottom,
            right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds2, bottom=m2pin_bounds2.top, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # ngate
        net = nets.ngate
        m2pin_bounds1 = l_gatelu.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_nclamp.bounds(net=net, mask=metal2pin.mask)
        y += m2_width + 2*metal2.min_space
        bottom = y - 0.5*m2_width
        top = y + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        left = 0.5*spec.metal_bigspace
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        right = left + m2_width
        bottom = m2pin_bounds2.top - m2_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds2.left, top=m2pin_bounds2.top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)


class _PadTriOut(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="IOPadTriOut")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()

        frame.add_track_nets(ckt=ckt)
        frame.add_clamp_nets(ckt=ckt)

        c2p = ckt.new_net(name="c2p", external=True)
        c2p_en = ckt.new_net(name="c2p_en", external=True)
        pad = ckt.new_net(name="pad", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=spec.clampdrive, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=spec.clampdrive, pad=pad,
        )
        frame.add_trackconn_inst(ckt=ckt, width=spec.monocell_width, connect_up=True)

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        i_gatedec = ckt.instantiate(fab.get_cell("GateDecode"), name="gatedec")
        for name in ("vss", "vdd", "iovdd", "ngate", "pgate"):
            ckt.nets[name].childports += i_gatedec.ports[name]
        c2p.childports += i_gatedec.ports.core
        c2p_en.childports += i_gatedec.ports.en

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        frame = fab.frame
        comp = fab.computed

        metal = comp.metal
        metal2 = metal[2].prim
        metal2pin = metal2.pin

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.place_trackconn(layouter=layouter)

        # DC Diodes
        frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Gate decoder + interconnect
        _l_gatedec = layouter.inst_layout(inst=insts.gatedec)
        dm2pin_bounds = _l_gatedec.bounds(net=nets.c2p, mask=metal2pin.mask)
        dem2pin_bounds = _l_gatedec.bounds(net=nets.c2p_en, mask=metal2pin.mask)
        x = tech.on_grid(
            0.5*spec.monocell_width - 0.5*(dm2pin_bounds.left + dem2pin_bounds.right)
        )
        l_gatedec = layouter.place(
            _l_gatedec, x=x,
            y=(frame.cells_y - cast(_geo._Rectangular, _l_gatedec.boundary).bottom),
        )

        # c2p & c2p_en
        # bring pins to top
        for name in ("c2p", "c2p_en"):
            frame.promote_m2instpin_to_corepin(layouter=layouter, net=nets[name], inst_layout=l_gatedec)

        # pgate
        net = nets.pgate
        m2pin_bounds1 = l_gatedec.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_pclamp.bounds(net=net, mask=metal2pin.mask)
        m2_width = comp.metal[2].minwidth4ext_updown
        bottom = cast(_geo._Rectangular, l_pclamp.boundary).top + 2*metal2.min_space
        y = bottom + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        top = bottom + m2_width
        shape = _geo.Rect(
            left=m2pin_bounds2.left, bottom=bottom,
            right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds2, bottom=m2pin_bounds2.top, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # ngate
        net = nets.ngate
        m2pin_bounds1 = l_gatedec.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_nclamp.bounds(net=net, mask=metal2pin.mask)
        y += m2_width + 2*metal2.min_space
        bottom = y - 0.5*m2_width
        top = y + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        left = 0.5*spec.metal_bigspace
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        right = left + m2_width
        bottom = m2pin_bounds2.top - m2_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds2.left, top=m2pin_bounds2.top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)


class _PadIn(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="IOPadIn")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()

        frame.add_track_nets(ckt=ckt)

        p2c = ckt.new_net(name="p2c", external=True)
        pad = ckt.new_net(name="pad", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=pad,
        )
        frame.add_trackconn_inst(ckt=ckt, width=spec.monocell_width, connect_up=True)

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        i_leveldown = ckt.instantiate(fab.get_cell("LevelDown"), name="leveldown")
        for name in ("vss", "vdd", "iovss", "iovdd", "pad"):
            ckt.nets[name].childports += i_leveldown.ports[name]
        p2c.childports += i_leveldown.ports.core

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame
        comp = fab.computed

        metal = comp.metal
        metal1 = metal[1].prim
        metal1pin = metal1.pin
        metal2 = metal[2].prim
        metal2pin = metal2.pin
        via1 = comp.vias[1]

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.place_trackconn(layouter=layouter)

        # DC Diodes
        frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # LevelDown + interconnect
        _l_ld = layouter.inst_layout(inst=insts.leveldown)

        # p2c
        net = nets.p2c
        _m1pin_bounds = _l_ld.bounds(net=net, mask=metal1pin.mask)
        x = 0.5*spec.monocell_width - 0.5*(_m1pin_bounds.left + _m1pin_bounds.right)
        l_ld = layouter.place(_l_ld, x=x, y=frame.cells_y)
        frame.promote_m1instpin_to_corepin(
            layouter=layouter, net=net, inst_layout=l_ld, align="left",
        )

        # pad
        net = nets.pad
        m2pin_bounds = l_ld.bounds(net=net, mask=metal2pin.mask)
        clamp_bounds = None
        for polygon in l_pclamp.filter_polygons(
            net=nets.pad, mask=metal2.mask, split=True,
        ):
            bounds = polygon.bounds
            if clamp_bounds is None:
                if bounds.left >= m2pin_bounds.left:
                    clamp_bounds = bounds
            else:
                if (
                    (bounds.left >= m2pin_bounds.left)
                    and (bounds.left < clamp_bounds.left)
                ):
                    clamp_bounds = bounds
        assert clamp_bounds is not None, "Internal error"
        m2_width = comp.metal[2].minwidth4ext_updown
        shape = _geo.Rect(
            left=m2pin_bounds.left, bottom=(m2pin_bounds.bottom - m2_width),
            right=(clamp_bounds.left + m2_width), top=m2pin_bounds.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=clamp_bounds, bottom=clamp_bounds.top, top=m2pin_bounds.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)


class _PadInOut(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="IOPadInOut")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()

        frame.add_track_nets(ckt=ckt)
        frame.add_clamp_nets(ckt=ckt)

        p2c = ckt.new_net(name="p2c", external=True)
        c2p = ckt.new_net(name="c2p", external=True)
        c2p_en = ckt.new_net(name="c2p_en", external=True)
        pad = ckt.new_net(name="pad", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=spec.clampdrive, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=spec.clampdrive, pad=pad,
        )
        frame.add_trackconn_inst(ckt=ckt, width=spec.monocell_width, connect_up=True)

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        i_gatedec = ckt.instantiate(fab.get_cell("GateDecode"), name="gatedec")
        for name in ("vss", "vdd", "iovdd", "ngate", "pgate"):
            ckt.nets[name].childports += i_gatedec.ports[name]
        c2p.childports += i_gatedec.ports.core
        c2p_en.childports += i_gatedec.ports.en

        i_leveldown = ckt.instantiate(fab.get_cell("LevelDown"), name="leveldown")
        for name in ("vss", "vdd", "iovss", "iovdd", "pad"):
            ckt.nets[name].childports += i_leveldown.ports[name]
        p2c.childports += i_leveldown.ports.core

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        frame = fab.frame
        comp = fab.computed

        metal = comp.metal
        metal1 = metal[1].prim
        metal1pin = metal1.pin
        metal2 = metal[2].prim
        metal2pin = metal2.pin
        via1 = comp.vias[1]

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.place_trackconn(layouter=layouter)

        # DC Diodes
        frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Gate decoder + interconnect
        _l_gatedec = layouter.inst_layout(inst=insts.gatedec)
        dm2pin_bounds = _l_gatedec.bounds(net=nets.c2p, mask=metal2pin.mask)
        dem2pin_bounds = _l_gatedec.bounds(net=nets.c2p_en, mask=metal2pin.mask)
        x = tech.on_grid(
            0.25*spec.monocell_width - 0.5*(dm2pin_bounds.left + dem2pin_bounds.right),
        )
        l_gatedec = layouter.place(
            _l_gatedec, x=x,
            y=(frame.cells_y - cast(_geo._Rectangular, _l_gatedec.boundary).bottom),
        )

        # c2p & c2p_en
        # bring pins to top
        for name in ("c2p", "c2p_en"):
            frame.promote_m2instpin_to_corepin(layouter=layouter, net=nets[name], inst_layout=l_gatedec)

        # pgate
        net = nets.pgate
        m2pin_bounds1 = l_gatedec.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_pclamp.bounds(net=net, mask=metal2pin.mask)
        m2_width = comp.metal[2].minwidth4ext_updown
        bottom = cast(_geo._Rectangular, l_pclamp.boundary).top + 2*metal2.min_space
        y = bottom + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        top = bottom + m2_width
        shape = _geo.Rect(
            left=m2pin_bounds2.left, bottom=bottom,
            right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds2, bottom=m2pin_bounds2.top, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # ngate
        net = nets.ngate
        m2pin_bounds1 = l_gatedec.bounds(net=net, mask=metal2pin.mask)
        m2pin_bounds2 = l_nclamp.bounds(net=net, mask=metal2pin.mask)
        y += m2_width + 2*metal2.min_space
        bottom = y - 0.5*m2_width
        top = y + 0.5*m2_width
        shape = _geo.Rect.from_rect(
            rect=m2pin_bounds1, bottom=bottom, top=m2pin_bounds1.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        left = 0.5*spec.metal_bigspace
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds1.right, top=top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        right = left + m2_width
        bottom = m2pin_bounds2.top - m2_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect(
            left=left, bottom=bottom, right=m2pin_bounds2.left, top=m2pin_bounds2.top,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)

        # LevelDown + interconnect
        _l_ld = layouter.inst_layout(inst=insts.leveldown)

        # p2c
        net = nets.p2c
        _m1pin_bounds = _l_ld.bounds(net=net, mask=metal1pin.mask)
        x = tech.on_grid(
            0.75*spec.monocell_width - 0.5*(_m1pin_bounds.left + _m1pin_bounds.right),
        )
        l_ld = layouter.place(_l_ld, x=x, y=frame.cells_y)
        frame.promote_m1instpin_to_corepin(
            layouter=layouter, net=net, inst_layout=l_ld, align="left",
        )

        # pad
        net = nets.pad
        m2pin_bounds = l_ld.bounds(net=net, mask=metal2pin.mask)
        clamp_bounds = None
        for polygon in l_pclamp.filter_polygons(
            net=nets.pad, mask=metal2.mask, split=True,
        ):
            bounds = polygon.bounds
            if clamp_bounds is None:
                if bounds.left >= m2pin_bounds.left:
                    clamp_bounds = bounds
            else:
                if (
                    (bounds.left >= m2pin_bounds.left)
                    and (bounds.left < clamp_bounds.left)
                ):
                    clamp_bounds = bounds
        assert clamp_bounds is not None, "Internal error"
        m2_width = comp.metal[2].minwidth4ext_updown
        shape = _geo.Rect(
            left=m2pin_bounds.left, bottom=(m2pin_bounds.bottom - m2_width),
            right=(clamp_bounds.left + m2_width), top=m2pin_bounds.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)
        shape = _geo.Rect.from_rect(
            rect=clamp_bounds, bottom=clamp_bounds.top, top=m2pin_bounds.bottom,
        )
        layouter.add_wire(net=net, wire=metal2, shape=shape)


class _PadAnalog(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="IOPadAnalog")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        iovss = nets.iovss
        iovdd = nets.iovdd

        pad = ckt.new_net(name="pad", external=True)
        padres = ckt.new_net(name="padres", external=True)

        frame.add_pad_inst(ckt=ckt, net=pad)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount_analog, n_drive=0, pad=pad,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount_analog, n_drive=0, pad=pad,
        )
        frame.add_trackconn_inst(ckt=ckt, width=spec.monocell_width, connect_up=True)

        frame.add_dcdiodes_inst(ckt=ckt, pad=pad)

        c_secondprot = fab.get_cell("SecondaryProtection")
        i_secondprot = ckt.instantiate(c_secondprot, name="secondprot")
        iovss.childports += i_secondprot.ports.iovss
        iovdd.childports += i_secondprot.ports.iovdd
        pad.childports += i_secondprot.ports.pad
        padres.childports += i_secondprot.ports.core

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        tech = fab.tech
        comp = fab.computed
        frame = fab.frame

        active = comp.active
        metal = comp.metal
        metal2 = metal[2].prim
        metal2pin = metal2.pin

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.pad)

        # Clamps
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.pad)
        l_pclamp = frame.place_pclamp(layouter=layouter, pad=nets.pad)

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.place_trackconn(layouter=layouter)

        # DC Diodes
        frame.place_dcdiodes(
            layouter=layouter, pad=nets["pad"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Place the secondary protection
        # Search for pad pin closest to the middle of the cell
        x_clamppin = None
        pinmask = metal2pin.mask
        clamppinm2_bounds: Optional[_geo.Rect] = None
        for polygon in l_pclamp.filter_polygons(net=nets.pad, mask=pinmask):
            for bounds in _iterate_polygonbounds(polygon=polygon):
                x_p = bounds.center.x
                if (x_clamppin is None) or (x_p > x_clamppin):
                    x_clamppin = x_p
                    assert isinstance(bounds, _geo.Rect)
                    clamppinm2_bounds = bounds
        assert x_clamppin is not None
        assert clamppinm2_bounds is not None
        _l_secondprot = layouter.inst_layout(inst=insts.secondprot)
        _actvdd_bounds = _l_secondprot.bounds(net=nets.iovdd, mask=active.mask)
        y = frame.cells_y - _actvdd_bounds.top + 0.5*comp.minwidth_activewithcontact
        _protpadpin_bounds = _l_secondprot.bounds(mask=pinmask, net=nets.pad)
        x_protpadpin = 0.5*(_protpadpin_bounds.left + _protpadpin_bounds.right)
        # Center pins
        x = tech.on_grid(x_clamppin - x_protpadpin)
        l_secondprot = layouter.place(_l_secondprot, x=x, y=y)
        protpadpin_bounds = l_secondprot.bounds(mask=pinmask, net=nets.pad)
        protpadrespin_bounds = l_secondprot.bounds(mask=pinmask, net=nets.padres)

        # Connect pins of secondary protection
        shape = _geo.Rect.from_rect(
            rect=protpadpin_bounds, bottom=clamppinm2_bounds.top,
        )
        layouter.add_wire(wire=metal2, net=nets.pad, shape=shape)

        shape = _geo.Rect.from_rect(
            rect=protpadrespin_bounds,
            left=(protpadrespin_bounds.right - comp.metal[2].minwidth4ext_updown),
        )
        frame.add_corepin(layouter=layouter, net=nets.padres, m2_shape=shape)

        # Connect pad pins
        left = spec.monocell_width
        right = 0.0
        for polygon in l_pclamp.filter_polygons(net=nets.pad, mask=pinmask):
            for bounds in _iterate_polygonbounds(polygon=polygon):
                if bounds.right < x_clamppin:
                    shape = _geo.Rect.from_rect(rect=bounds, top=frame.cell_height)
                    layouter.add_wire(net=nets.pad, wire=metal2, shape=shape)

                    left = min(left, bounds.left)
                    right = max(right, bounds.right)
        top = frame.cell_height
        bottom = top - 5*metal2.min_width
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        frame.add_corepin(layouter=layouter, net=nets.pad, m2_shape=shape)


class _PadIOVss(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="IOPadIOVss")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        iovss = nets.iovss

        frame.add_pad_inst(ckt=ckt, net=iovss)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=iovss,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=iovss,
        )
        frame.add_trackconn_inst(ckt=ckt, width=spec.monocell_width, connect_up=True)

        frame.add_dcdiodes_inst(ckt=ckt, pad=iovss)

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.circuit
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.iovss)

        # iovss & iovdd
        l_nclamp = frame.place_nclamp(
            layouter=layouter, pad=nets.iovss, connect_iovss=True,
        )
        l_pclamp = frame.place_pclamp(
            layouter=layouter, pad=nets.iovss, connect_iovsstap=True,
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.place_trackconn(layouter=layouter)

        # DC Diodes
        frame.place_dcdiodes(
            layouter=layouter, pad=nets["iovss"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )


class _PadIOVdd(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="IOPadIOVdd")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        iovss = nets.iovss
        iovdd = nets.iovdd

        frame.add_pad_inst(ckt=ckt, net=iovdd)

        if spec.invvdd_n_mosfet is None:
            # Just put a n&p clamp without drive
            frame.add_nclamp_inst(
                ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=iovdd,
            )
            frame.add_pclamp_inst(
                ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=iovdd,
            )
        else:
            frame.add_clamp_nets(ckt=ckt, add_p=False)
            frame.add_nclamp_inst(
                ckt=ckt, n_trans=spec.clampcount, n_drive=spec.clampcount, pad=iovdd,
            )
            ngate = nets.ngate

            # Add RC active clamp
            c_res = fab.get_cell("RCClampResistor")
            i_res = ckt.instantiate(c_res, name="rcres")
            iovdd.childports += i_res.ports.pin1

            c_inv = fab.get_cell("RCClampInverter")
            i_inv = ckt.instantiate(c_inv, name="rcinv")
            iovss.childports += i_inv.ports.ground
            iovdd.childports += i_inv.ports.supply
            ngate.childports += i_inv.ports.out

            ckt.new_net(name="iovdd_res", external=False, childports=(
                i_res.ports.pin2, i_inv.ports["in"],
            ))

        frame.add_trackconn_inst(ckt=ckt, width=spec.monocell_width, connect_up=True)

    def _create_layout(self):
        fab = self.fab
        tech = fab.tech
        spec = fab.spec
        comp = fab.computed
        frame = fab.frame
        framespec = frame.framespec

        metal = comp.metal
        metal1 = metal[1].prim
        metal1pin = metal1.pin
        metal2 = metal[2].prim
        metal2pin = metal2.pin
        via1 = comp.vias[1]
        via2 = comp.vias[2]

        iovss_trackspec = frame.track_specs["iovss"]
        iovdd_trackspec = frame.track_specs["iovdd"]

        ckt = self.circuit
        insts = ckt.instances
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(
            ckt=ckt, layouter=layouter,
            skip_top=() if frame.has_pad else ("iovss",),
        )
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.iovdd)
        padm2_bounds = frame.pad_bb(prim=metal2)

        # Place nclamp + connect to pad + pad guard ring
        l_nclamp = layouter.place(insts.nclamp, x=0.0, y=iovss_trackspec.bottom)
        for polygon in l_nclamp.filter_polygons(
            net=nets.iovdd, mask=metal2pin.mask, split=True,
        ):
            bb = polygon.bounds
            shape = _geo.Rect.from_rect(
                rect=bb,
                top=max(bb.top, padm2_bounds.bottom),
                bottom=min(bb.bottom, padm2_bounds.top),
            )
            layouter.add_wire(wire=metal2, net=nets.iovdd, shape=shape)

            y = bb.top
            layouter.add_wire(
                net=nets.iovdd, wire=via1, y=y,
                bottom_left=shape.left, bottom_right=shape.right, bottom_enclosure="tall",
                top_left=shape.left, top_right=shape.right, top_enclosure="tall",
            )

        # Draw guardring around pad and connect to iovdd track
        bottom = cast(_geo._Rectangular, l_nclamp.boundary).top
        top = iovdd_trackspec.bottom - comp.guardring_space
        _l = hlp.guardring(
            fab=fab, net=nets.iovss, type_="n",
            width=spec.monocell_width, height=(top - bottom),
        )
        l = layouter.place(_l, x=0.5*spec.monocell_width, y=0.5*(bottom + top))
        padguardring_m1bb = l.bounds(mask=metal1.mask)

        if spec.invvdd_n_mosfet is None:
            # Place pclamp + connect to iovdd track
            frame.place_pclamp(
                layouter=layouter, pad=nets.iovdd, connect_track="iovdd",
            )
        else:
            # Place the RC clamp subblocks
            l_rcinv = layouter.place(
                insts.rcinv, x=spec.monocell_width, y=iovdd_trackspec.bottom,
                rotation=_geo.Rotation.MY,
            )
            _l = layouter.inst_layout(inst=insts.rcres, rotation=_geo.Rotation.MX)
            _bb = _l.boundary
            assert _bb is not None
            if frame.has_pad:
                o = padm2_bounds.center - _bb.center
            else:
                # TODO: proper placement
                o = _geo.Point(
                    x=(0.5*frame.monocell_width - _bb.center.x),
                    y=(iovss_trackspec.top - _bb.top - 5.0),
                )
            l_rcres = layouter.place(_l, origin=o)

            # Connect supply of inv to iovdd track
            net = nets.iovdd
            m1pinbb = l_rcinv.bounds(mask=metal1pin.mask, net=net, depth=1)

            w = m1pinbb.width
            _l = layouter.wire_layout(
                net=net, wire=via1,
                bottom_width=w, bottom_enclosure="tall",
                top_width=w, top_enclosure="tall",
            )
            _m1bb = _l.bounds(mask=metal1.mask)
            x = m1pinbb.center.x
            y = m1pinbb.bottom - _m1bb.bottom
            layouter.place(_l, x=x, y=y)
            layouter.add_wire(
                net=net, wire=via2, x=x, y=y,
                bottom_width=w, bottom_enclosure="tall",
                top_width=w, top_enclosure="tall",
            )

            # Connect res output to inv input
            net = nets.iovdd_res
            res_m1pinbb = l_rcres.bounds(mask=metal1pin.mask, net=net, depth=1)
            inv_m2pinbb = l_rcinv.bounds(mask=metal2pin.mask, net=net, depth=1)

            w = inv_m2pinbb.right - res_m1pinbb.left
            _l = layouter.wire_layout(
                net=net, wire=via1,
                bottom_width=w, bottom_enclosure="tall",
                top_width=w, top_enclosure="tall",
            )
            _via1_m1bb = _l.bounds(mask=metal1.mask)
            x = res_m1pinbb.left - _via1_m1bb.left
            y = (
                padguardring_m1bb.top - comp.guardring_width - 2*metal1.min_space
                - _via1_m1bb.top
            )
            l = layouter.place(_l, x=x, y=y)
            via1_m1bb = l.bounds(mask=metal1.mask)
            via1_m2bb = l.bounds(mask=metal2.mask)
            shape = _geo.Rect.from_rect(rect=res_m1pinbb, top=via1_m1bb.top)
            layouter.add_wire(net=net, wire=metal1, shape=shape)
            shape = _geo.Rect.from_rect(
                rect=inv_m2pinbb,
                bottom=via1_m2bb.bottom, left=max(inv_m2pinbb.left, via1_m2bb.left),
            )
            layouter.add_wire(net=net, wire=metal2, shape=shape)

            # Connect inv output to gate of nclamp
            net = nets.ngate
            inv_m2pinbb = l_rcinv.bounds(mask=metal2pin.mask, net=net, depth=1)
            nclamp_m2pinbb = l_nclamp.bounds(mask=metal2pin.mask, net=net, depth=1)

            left = 2*metal2.min_space
            shape = _geo.Rect.from_rect(rect=inv_m2pinbb, left=left)
            layouter.add_wire(net=net, wire=metal2, shape=shape)
            shape = _geo.Rect.from_rect(rect=nclamp_m2pinbb, left=left)
            layouter.add_wire(net=net, wire=metal2, shape=shape)
            shape = _geo.Rect(
                left=left, bottom=nclamp_m2pinbb.bottom,
                right=(left + 2*metal2.min_width), top=inv_m2pinbb.top,
            )
            layouter.add_wire(net=net, wire=metal2, shape=shape)

            # Connect pin1 of rcres to pad
            m1pinbb = l_rcres.bounds(mask=metal1pin.mask, net=nets.iovdd, depth=1)

            _l = layouter.wire_layout(
                net=nets.iovdd, wire=via1, columns=2,
                bottom_enclosure="tall", top_enclosure="tall",
            )
            _m1bb = _l.bounds(mask=metal1.mask)
            x = m1pinbb.right - _m1bb.right
            y = m1pinbb.center.y
            l = layouter.place(_l, x=x, y=y)
            m2bb = l.bounds(mask=metal2.mask)
            if frame.has_pad:
                _l = layouter.wire_layout(
                    net=nets.iovdd, wire=via2, columns=2,
                    bottom_enclosure="tall", top_enclosure="tall",
                )
                _m2bb = _l.bounds(mask=metal2.mask)
                x = m2bb.right - _m2bb.right
                layouter.place(_l, x=x, y=y)
            else:
                w = m2bb.height
                x1 = m2bb.center.x
                y1 = m2bb.center.y
                x2 = nclamp_m2pinbb.right + metal2.min_space + w
                y2 = padm2_bounds.top
                shape = _geo.MultiPath(
                    _geo.Start(point=m2bb.center, width=w),
                    _geo.GoLeft(dist=(x1 - x2)),
                    _geo.GoDown(dist=(y1 - y2)),
                )
                layouter.add_wire(net=nets.iovdd, wire=metal2, shape=shape)

            # Connect pad to iovdd track
            net = nets.iovdd
            max_pitch = framespec.tracksegment_maxpitch
            fingers = floor((framespec.pad_width + _geo.epsilon)/max_pitch) + 1
            pitch = tech.on_grid(framespec.pad_width/fingers, mult=2, rounding="floor")
            track_top = iovdd_trackspec.top
            specs = comp.track_metalspecs
            for metal_spec in (specs if frame.has_pad else specs[-1:]):
                metal = metal_spec.prim
                space = metal_spec.tracksegment_space

                pad_bb = frame.pad_bb(prim=metal)
                width = pitch - space
                top = track_top - 0.5*space
                bottom = pad_bb.top
                for n in range(fingers):
                    if n < fingers - 1:
                        left = pad_bb.left + n*pitch + 0.5*space
                        right = left + width
                    else:
                        right = pad_bb.right - 0.5*space
                        left = right - width
                    shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
                    layouter.add_wire(net=net, wire=metal, shape=shape)

        # Bulk/well connection cell
        frame.place_trackconn(layouter=layouter)


class _PadVss(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="IOPadVss")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        vss = nets.vss

        frame.add_pad_inst(ckt=ckt, net=vss)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=vss,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=vss,
        )
        frame.add_trackconn_inst(ckt=ckt, width=spec.monocell_width, connect_up=True)

        frame.add_dcdiodes_inst(ckt=ckt, pad=vss)

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed
        frame = fab.frame

        metal = comp.metal
        metal2 = metal[2].prim

        ckt = self.circuit
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.vss)

        # iovss & iovdd
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.vss)
        l_pclamp = frame.place_pclamp(
            layouter=layouter, pad=nets.vss, connect_track="vss",
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.place_trackconn(layouter=layouter)

        # DC Diodes
        frame.place_dcdiodes(
            layouter=layouter, pad=nets["vss"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )



class _PadVdd(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="IOPadVdd")

    def _create_circuit(self):
        fab = self.fab
        spec = fab.spec
        frame = fab.frame

        ckt = self.new_circuit()
        nets = ckt.nets

        frame.add_track_nets(ckt=ckt)
        vdd = nets.vdd

        frame.add_pad_inst(ckt=ckt, net=vdd)
        frame.add_nclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=vdd,
        )
        frame.add_pclamp_inst(
            ckt=ckt, n_trans=spec.clampcount, n_drive=0, pad=vdd,
        )
        frame.add_trackconn_inst(ckt=ckt, width=spec.monocell_width, connect_up=True)

        frame.add_dcdiodes_inst(ckt=ckt, pad=vdd)

    def _create_layout(self):
        fab = self.fab
        spec = fab.spec
        comp = fab.computed
        frame = fab.frame

        metal = comp.metal
        metal2 = metal[2].prim

        ckt = self.circuit
        nets = ckt.nets

        layouter = self.new_circuitlayouter()
        layout = self.layout
        layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=spec.monocell_width, top=frame.cell_height,
        )

        frame.draw_tracks(ckt=ckt, layouter=layouter)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=spec.monocell_width,
            cells_only=True,
        )

        # PAD
        frame.place_pad(layouter=layouter, net=nets.vdd)

        # iovss & iovdd
        l_nclamp = frame.place_nclamp(layouter=layouter, pad=nets.vdd)
        l_pclamp = frame.place_pclamp(
            layouter=layouter, pad=nets.vdd, connect_track="vdd",
        )

        # Bulk/well connection clamps
        frame.connect_clamp_wells(
            ckt=ckt, layouter=layouter, nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )

        # Bulk/well connection cell
        frame.place_trackconn(layouter=layouter)

        # DC Diodes
        frame.place_dcdiodes(
            layouter=layouter, pad=nets["vdd"],
            nclamp_lay=l_nclamp, pclamp_lay=l_pclamp,
        )


class _Filler(_FactoryCell):
    def __init__(self, *,
        fab: "IOFactory", name: str, cell_width: float,
    ):
        super().__init__(fab=fab, name=name)

        frame = fab.frame

        ckt = self.new_circuit()
        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        frame.add_track_nets(ckt=ckt)

        frame.draw_tracks(ckt=ckt, layouter=layouter, cell_width=cell_width)
        frame.draw_lowertracks(
            ckt=ckt, layouter=layouter, cell_width=cell_width, cells_only=False,
        )

        # Boundary
        bb = _geo.Rect(
            left=0.0, bottom=0.0, right=cell_width, top=frame.cell_height,
        )
        layout.boundary = bb


class _Corner(_FactoryCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="Corner")

        frame = fab.frame
        spec = fab.spec

        ckt = self.new_circuit()
        layouter = self.new_circuitlayouter()
        layout = layouter.layout

        frame.add_track_nets(ckt=ckt)
        frame.draw_corner_tracks(ckt=ckt, layouter=layouter)

        # Boundary
        bb = _geo.Rect(
            left=-frame.cell_height, bottom=0.0, right=0.0, top=frame.cell_height,
        )
        layout.boundary = bb


class _Gallery(_FactoryOnDemandCell):
    def __init__(self, *, fab: "IOFactory"):
        super().__init__(fab=fab, name="Gallery")

    cells = (
        "Corner",
        "Filler200", "Filler400", "Filler1000", "Filler2000", "Filler4000", "Filler10000",
        "IOPadVss", "IOPadVdd", "IOPadIn", "IOPadOut", "IOPadTriOut", "IOPadInOut",
        "IOPadIOVss", "IOPadIOVdd", "IOPadAnalog",
    )
    cells_l = tuple(cell.lower() for cell in cells)

    def _create_circuit(self):
        fab = self.fab
        tech = self.tech
        ckt = self.new_circuit()
        insts = ckt.instances

        for cell_name in self.cells:
            if cell_name.startswith("Filler"):
                w = float(cell_name[6:])*tech.grid
                cell = fab.filler(cell_width=w)
            else:
                cell = fab.get_cell(cell_name)
            ckt.instantiate(cell, name=cell_name.lower())

        # Add second corner cell
        ckt.instantiate(fab.get_cell("Corner"), name="corner2")
        cells_l = (*self.cells_l, "corner2")

        # vss and iovss are connected by the substrate
        # make only vss in Gallery so it is LVS clean.
        for net in ("vdd", "vss", "iovdd"):
            ports = tuple(insts[cell].ports[net] for cell in cells_l)
            if net == "vss":
                ports += tuple(insts[cell].ports["iovss"] for cell in cells_l)
            ckt.new_net(name=net, external=True, childports=ports)

        ckt.new_net(name="in_p2c", external=True, childports=(
            insts.iopadin.ports.p2c,
        ))
        ckt.new_net(name="in_pad", external=True, childports=(
            insts.iopadin.ports.pad,
        ))
        ckt.new_net(name="out_c2p", external=True, childports=(
            insts.iopadout.ports.c2p,
        ))
        ckt.new_net(name="out_pad", external=True, childports=(
            insts.iopadout.ports.pad,
        ))
        ckt.new_net(name="triout_c2p", external=True, childports=(
            insts.iopadtriout.ports.c2p,
        ))
        ckt.new_net(name="triout_c2p_en", external=True, childports=(
            insts.iopadtriout.ports.c2p_en,
        ))
        ckt.new_net(name="triout_pad", external=True, childports=(
            insts.iopadtriout.ports.pad,
        ))
        ckt.new_net(name="io_p2c", external=True, childports=(
            insts.iopadinout.ports.p2c,
        ))
        ckt.new_net(name="io_c2p", external=True, childports=(
            insts.iopadinout.ports.c2p,
        ))
        ckt.new_net(name="io_c2p_en", external=True, childports=(
            insts.iopadinout.ports.c2p_en,
        ))
        ckt.new_net(name="io_pad", external=True, childports=(
            insts.iopadinout.ports.pad,
        ))
        ckt.new_net(name="ana_out", external=True, childports=(
            insts.iopadanalog.ports.pad,
        ))
        ckt.new_net(name="ana_outres", external=True, childports=(
            insts.iopadanalog.ports.padres,
        ))

    def _create_layout(self):
        fab = self.fab
        frame = fab.frame
        comp = fab.computed

        ckt = self.circuit
        nets = ckt.nets
        insts = ckt.instances
        layouter = self.new_circuitlayouter()

        padpin_metal = comp.track_metalspecs[-1].prim
        padpin_bb = frame.pad_bb(prim=padpin_metal)
        metal3 = comp.metal[3].prim

        x = 0.0
        y = 0.0

        pad_nets = {
            "iopadvss": nets["vss"],
            "iopadiovss": nets["vss"],
            "iopadvdd": nets["vdd"],
            "iopadiovdd": nets["iovdd"],
            "iopadin": nets["in_pad"],
            "iopadout": nets["out_pad"],
            "iopadtriout": nets["triout_pad"],
            "iopadinout": nets["io_pad"],
            "iopadanalog": nets["ana_out"],
        }
        core_nets = {
            "iopadin": (nets["in_p2c"],),
            "iopadout": (nets["out_c2p"],),
            "iopadtriout": (nets["triout_c2p"], nets["triout_c2p_en"]),
            "iopadinout": (nets["io_p2c"], nets["io_c2p"], nets["io_c2p_en"]),
            "iopadanalog": (nets["ana_out"], nets["ana_outres"]),
        }

        bnd: Optional[_geo._Rectangular] = None
        for cell in self.cells_l:
            inst = insts[cell]
            l = layouter.place(inst, x=x, y=y)

            net =  pad_nets.get(cell, None)
            if net is not None:
                layouter.add_wire(
                    net=net, wire=padpin_metal, pin=padpin_metal.pin,
                    shape=padpin_bb.moved(dxy=_geo.Point(x=x, y=y)),
                )
            for net in core_nets.get(cell, ()):
                for ms in l.filter_polygons(net=net, mask=metal3.pin.mask, split=True, depth=1):
                    shape = cast(_geo.RectangularT, ms.shape)
                    if shape.bottom > _geo.epsilon:
                        layouter.add_wire(net=net, wire=metal3, pin=metal3.pin, shape=shape)

            bnd = l.boundary
            assert bnd is not None
            x = bnd.right
        assert bnd is not None

        # Add second corner cell
        l = layouter.place(insts["corner2"], x=x, y=y, rotation=_geo.Rotation.MY)
        bnd = l.boundary
        assert bnd is not None

        self.layout.boundary = _geo.Rect(
            left=0.0, bottom=0.0, right=bnd.right, top=bnd.top,
        )


class IOFactory(_fab.CellFactory[_FactoryCell]):
    def __init__(self, *,
        lib: _lbry.Library, cktfab: _ckt.CircuitFactory, layoutfab: _lay.LayoutFactory,
        spec: IOSpecification, framespec:IOFrameSpecification,
    ):
        if lib.tech != spec.stdcelllib.tech:
            raise ValueError(
                f"Library technology '{lib.tech.name}' differs standard cell technology"
                f" '{spec.stdcelllib.name}'"
            )
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab, cell_class=_FactoryCell,
        )
        self.spec = spec

        self.computed = _ComputedSpecs(
            fab=self, framespec=framespec,
            nmos=spec.nmos, pmos=spec.pmos, ionmos=spec.ionmos, iopmos=spec.iopmos,
        )
        self.frame = _IOCellFrame(fab=self, framespec=framespec)

    def guardring(self, *,
        type_: str, width: float, height: float,
        fill_well: bool=False, fill_implant: bool=False,
    ):
        s = "GuardRing_{}{}W{}H{}{}".format(
            type_.upper(),
            round(width/self.tech.grid),
            round(height/self.tech.grid),
            "T" if fill_well else "F",
            "T" if fill_implant else "F",
        )

        try:
            return self.lib.cells[s]
        except KeyError:
            cell = _GuardRing(
                name=s, fab=self, type_=type_, width=width, height=height,
                fill_well=fill_well, fill_implant=fill_implant,
            )
            self.lib.cells += cell
            return cell

    def pad(self, *, width: float, height: float) -> _Pad:
        s = "Pad_{}W{}H".format(
            round(width/self.tech.grid),
            round(height/self.tech.grid),
        )

        try:
            return cast(_Pad, self.lib.cells[s])
        except KeyError:
            cell = _Pad(
                name=s, fab=self, width=width, height=height,
                start_via=2,
            )
            self.lib.cells += cell
            return cell

    def trackconn(self, *, width: float):
        s = f"TrackConn_{round(width/self.tech.grid)}W"

        try:
            return self.lib.cells[s]
        except KeyError:
            cell = _TrackConn(name=s, fab=self, cell_width=width)
            self.lib.cells += cell
            return cell

    def clamp(self, *, type_: str, n_trans: int, n_drive: int):
        s = "Clamp_{}{}N{}D".format(
            type_.upper(),
            n_trans,
            n_drive,
        )

        try:
            return self.lib.cells[s]
        except KeyError:
            cell = _Clamp(
                name=s, type_=type_, fab=self, n_trans=n_trans, n_drive=n_drive,
            )
            self.lib.cells += cell
            return cell

    def filler(self, *, cell_width: float):
        tech = self.tech
        s = f"Filler{round(cell_width/tech.grid)}"

        try:
            return self.lib.cells[s]
        except KeyError:
            cell = _Filler(name=s, fab=self, cell_width=cell_width)
            self.lib.cells += cell
            return cell

    def dcdiode(self, *, type_: str):
        if not self.spec.add_dcdiodes:
            raise TypeError("Can't generate DCDiode for Factory without DC diodes")

        if type_ not in ("n", "p"):
            raise ValueError(f"DCDiode type has to be 'n' or 'p' not '{type_}'")
        s = f"DC{type_.upper()}Diode"

        try:
            return self.lib.cells[s]
        except KeyError:
            cell = _DCDiode(name=s, fab=self, type_=type_)
            self.lib.cells += cell
            return cell

    def get_cell(self, name) -> _cell.Cell:
        try:
            return self.lib.cells[name]
        except KeyError:
            lookup = {
                "SecondaryProtection": _Secondary,
                "RCClampResistor": _RCClampResistor,
                "RCClampInverter": _RCClampInverter,
                "LevelUp": _LevelUp,
                "LevelDown": _LevelDown,
                "GateLevelUp": _GateLevelUp,
                "GateDecode": _GateDecode,
                "IOPadIn": _PadIn,
                "IOPadOut": _PadOut,
                "IOPadTriOut": _PadTriOut,
                "IOPadInOut": _PadInOut,
                "IOPadVdd": _PadVdd,
                "IOPadVss": _PadVss,
                "IOPadIOVdd": _PadIOVdd,
                "IOPadIOVss": _PadIOVss,
                "IOPadAnalog": _PadAnalog,
                "Corner": _Corner,
                "Gallery": _Gallery,
            }
            cell = lookup[name](fab=self)
            self.lib.cells += cell
            return cell
