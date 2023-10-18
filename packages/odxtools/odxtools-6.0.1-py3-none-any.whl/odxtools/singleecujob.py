# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, cast
from xml.etree import ElementTree

from .admindata import AdminData
from .audience import Audience
from .createsdgs import create_sdgs_from_et
from .element import IdentifiableElement
from .exceptions import DecodeError, EncodeError, odxraise, odxrequire
from .functionalclass import FunctionalClass
from .globals import logger
from .inputparam import InputParam
from .message import Message
from .nameditemlist import NamedItemList
from .negoutputparam import NegOutputParam
from .odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId, OdxLinkRef
from .odxtypes import ParameterValue, odxstr_to_bool
from .outputparam import OutputParam
from .progcode import ProgCode
from .specialdatagroup import SpecialDataGroup
from .utils import dataclass_fields_asdict

if TYPE_CHECKING:
    from .diaglayer import DiagLayer


class DiagClassType(Enum):
    STARTCOMM = "STARTCOMM"
    STOPCOMM = "STOPCOMM"
    VARIANTIDENTIFICATION = "VARIANTIDENTIFICATION"
    READ_DYN_DEFINED_MESSAGE = "READ-DYN-DEFINED-MESSAGE"
    DYN_DEF_MESSAGE = "DYN-DEF-MESSAGE"
    CLEAR_DYN_DEF_MESSAGE = "CLEAR-DYN-DEF-MESSAGE"


@dataclass
class SingleEcuJob(IdentifiableElement):
    """A single ECU job is a diagnostic communication primitive.

    A single ECU job is more complex than a diagnostic service and is not provided natively by the ECU.
    In particular, the job is defined in external programs which are referenced by the attribute `.prog_codes`.

    In contrast to "multiple ECU jobs", a single ECU job only does service calls to a single ECU.

    Single ECU jobs are defined in section 7.3.5.7 of the ASAM MCD-2 standard.

    TODO: The following xml attributes are not internalized yet:
          PROTOCOL-SNREFS, RELATED-DIAG-COMM-REFS, PRE-CONDITION-STATE-REFS, STATE-TRANSITION-REFS
    """

    prog_codes: List[ProgCode]
    # optional xsd:elements inherited from DIAG-COMM (and thus shared with DIAG-SERVICE)
    oid: Optional[str]
    admin_data: Optional[AdminData]
    functional_class_refs: List[OdxLinkRef]
    audience: Optional[Audience]
    # optional xsd:elements specific to SINGLE-ECU-JOB
    # cast(...) just tells the type checker to pretend it's a list...
    input_params: Union[NamedItemList[InputParam], List[InputParam]]
    output_params: Union[NamedItemList[OutputParam], List[OutputParam]]
    neg_output_params: Union[NamedItemList[NegOutputParam], List[NegOutputParam]]
    # xsd:attributes inherited from DIAG-COMM (and thus shared with DIAG-SERVICE)
    semantic: Optional[str]
    diagnostic_class: Optional[DiagClassType]
    is_mandatory_raw: Optional[bool]
    is_executable_raw: Optional[bool]
    is_final_raw: Optional[bool]
    sdgs: List[SpecialDataGroup]

    @property
    def is_mandatory(self) -> bool:
        return self.is_mandatory_raw is True

    @property
    def is_executable(self) -> bool:
        return self.is_executable_raw in (None, True)

    @property
    def is_final(self) -> bool:
        return self.is_final_raw is True

    def __post_init__(self) -> None:
        if not self.functional_class_refs:
            self.functional_class_refs = []
        self._functional_classes: NamedItemList[FunctionalClass]

        # Replace None attributes by empty lists
        if not self.input_params:
            self.input_params = NamedItemList()
        if not self.output_params:
            self.output_params = NamedItemList()
        if not self.neg_output_params:
            self.neg_output_params = NamedItemList()

    @staticmethod
    def from_et(et_element: ElementTree.Element, doc_frags: List[OdxDocFragment]) -> "SingleEcuJob":

        logger.info(f"Parsing service based on ET DiagService element: {et_element}")
        kwargs = dataclass_fields_asdict(IdentifiableElement.from_et(et_element, doc_frags))
        admin_data = AdminData.from_et(et_element.find("ADMIN-DATA"), doc_frags)
        semantic = et_element.get("SEMANTIC")

        functional_class_refs = [
            odxrequire(OdxLinkRef.from_et(el, doc_frags))
            for el in et_element.iterfind("FUNCT-CLASS-REFS/FUNCT-CLASS-REF")
        ]

        prog_codes = [
            ProgCode.from_et(pc_elem, doc_frags)
            for pc_elem in et_element.iterfind("PROG-CODES/PROG-CODE")
        ]

        if (audience_elem := et_element.find("AUDIENCE")) is not None:
            audience = Audience.from_et(audience_elem, doc_frags)
        else:
            audience = None

        input_params = [
            InputParam.from_et(el, doc_frags)
            for el in et_element.iterfind("INPUT-PARAMS/INPUT-PARAM")
        ]
        output_params = [
            OutputParam.from_et(el, doc_frags)
            for el in et_element.iterfind("OUTPUT-PARAMS/OUTPUT-PARAM")
        ]
        neg_output_params = [
            NegOutputParam.from_et(el, doc_frags)
            for el in et_element.iterfind("NEG-OUTPUT-PARAMS/NEG-OUTPUT-PARAM")
        ]

        sdgs = create_sdgs_from_et(et_element.find("SDGS"), doc_frags)

        # Read boolean flags. Note that the "else" clause contains the default value.
        is_mandatory_raw = odxstr_to_bool(et_element.get("IS-MANDATORY"))
        is_executable_raw = odxstr_to_bool(et_element.get("IS-MANDATORY"))
        is_final_raw = odxstr_to_bool(et_element.get("IS-FINAL"))

        diag_class: Optional[DiagClassType] = None
        if (diag_class_str := et_element.get("DIAGNOSTIC-CLASS")) is not None:
            try:
                diag_class = DiagClassType(diag_class_str)
            except ValueError:
                diag_class = cast(DiagClassType, None)
                odxraise(f"Encountered unknown diagnostic class type '{diag_class_str}'")

        return SingleEcuJob(
            oid=None,
            admin_data=admin_data,
            prog_codes=prog_codes,
            semantic=semantic,
            audience=audience,
            functional_class_refs=functional_class_refs,
            diagnostic_class=diag_class,
            input_params=input_params,
            output_params=output_params,
            neg_output_params=neg_output_params,
            is_mandatory_raw=is_mandatory_raw,
            is_executable_raw=is_executable_raw,
            is_final_raw=is_final_raw,
            sdgs=sdgs,
            **kwargs)

    @property
    def functional_classes(self) -> NamedItemList[FunctionalClass]:
        """The functional classes referenced by this job.
        This is None iff the references were not resolved.
        """
        return self._functional_classes

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        result = {self.odx_id: self}

        for prog_code in self.prog_codes:
            result.update(prog_code._build_odxlinks())
        for input_param in self.input_params:
            result.update(input_param._build_odxlinks())
        for output_param in self.output_params:
            result.update(output_param._build_odxlinks())
        for neg_output_param in self.neg_output_params:
            result.update(neg_output_param._build_odxlinks())
        for sdg in self.sdgs:
            result.update(sdg._build_odxlinks())

        if self.admin_data:
            result.update(self.admin_data._build_odxlinks())

        if self.audience:
            result.update(self.audience._build_odxlinks())

        return result

    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:
        for code in self.prog_codes:
            code._resolve_odxlinks(odxlinks)

        # Resolve references to functional classes
        self._functional_classes = NamedItemList[FunctionalClass]([])
        for fc_ref in self.functional_class_refs:
            fc = odxlinks.resolve(fc_ref)
            if isinstance(fc, FunctionalClass):
                self._functional_classes.append(fc)
            else:
                logger.warning(f"Functional class ID {fc_ref!r} resolved to {fc!r}.")

        for prog_code in self.prog_codes:
            prog_code._resolve_odxlinks(odxlinks)
        for input_param in self.input_params:
            input_param._resolve_odxlinks(odxlinks)
        for output_param in self.output_params:
            output_param._resolve_odxlinks(odxlinks)
        for neg_output_param in self.neg_output_params:
            neg_output_param._resolve_odxlinks(odxlinks)
        for sdg in self.sdgs:
            sdg._resolve_odxlinks(odxlinks)

        # Resolve references of admin data
        if self.admin_data:
            self.admin_data._resolve_odxlinks(odxlinks)

        # Resolve references of audience
        if self.audience:
            self.audience._resolve_odxlinks(odxlinks)

    def _resolve_snrefs(self, diag_layer: "DiagLayer") -> None:
        for prog_code in self.prog_codes:
            prog_code._resolve_snrefs(diag_layer)
        for input_param in self.input_params:
            input_param._resolve_snrefs(diag_layer)
        for output_param in self.output_params:
            output_param._resolve_snrefs(diag_layer)
        for neg_output_param in self.neg_output_params:
            neg_output_param._resolve_snrefs(diag_layer)
        for sdg in self.sdgs:
            sdg._resolve_snrefs(diag_layer)

        # Resolve references of admin data
        if self.admin_data:
            self.admin_data._resolve_snrefs(diag_layer)

        # Resolve references of audience
        if self.audience:
            self.audience._resolve_snrefs(diag_layer)

    def decode_message(self, message: bytes) -> Message:
        """This function's signature matches `DiagService.decode_message`
        and only raises an informative error.
        """
        raise DecodeError(
            f"Single ECU jobs are completely executed on the tester and thus cannot be decoded."
            f" You tried to decode a response for the job {self.odx_id}.")

    def encode_request(self, **params: ParameterValue) -> bytes:
        """This function's signature matches `DiagService.encode_request`
        and only raises an informative error.
        """
        raise EncodeError(
            f"Single ECU jobs are completely executed on the tester and thus cannot be encoded."
            f" You tried to encode a request for the job {self.odx_id}.")

    def encode_positive_response(self,
                                 coded_request: bytes,
                                 response_index: int = 0,
                                 **params: ParameterValue) -> bytes:
        """This function's signature matches `DiagService.encode_positive_response`
        and only raises an informative error.
        """
        raise EncodeError(
            f"Single ECU jobs are completely executed on the tester and thus cannot be encoded."
            f" You tried to encode a response for the job {self.odx_id}.")

    def encode_negative_response(self,
                                 coded_request: bytes,
                                 response_index: int = 0,
                                 **params: ParameterValue) -> bytes:
        """This function's signature matches `DiagService.encode_negative_response`
        and only raises an informative error.
        """
        raise EncodeError(
            f"Single ECU jobs are completely executed on the tester and thus cannot be encoded."
            f" You tried to encode the job {self.odx_id}.")

    def __call__(self, **params: ParameterValue) -> bytes:
        raise EncodeError(
            f"Single ECU jobs are completely executed on the tester and thus cannot be encoded."
            f" You tried to call the job {self.odx_id}.")

    def __hash__(self) -> int:
        return hash(self.odx_id)
