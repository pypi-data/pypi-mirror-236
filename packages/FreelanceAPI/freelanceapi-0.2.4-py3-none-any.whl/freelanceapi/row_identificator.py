from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional, Tuple, Union

from ._validator import (
    AreaChar, AreaDefinition, AreaLength, DataTyp, Identification, Length, Libary, Max12Chars, Max16Chars, Max30Chars,
    MeasuringPoint, ModuleType, NoIdear, ParaForGwy, ParaForParaData, ParaForUidAcc, ParaLength, ProcessStation,
    ValueTrueOrFalse, Var, VariabelName
    )
from .sections.area_dict import AreaDict
from .sections.eam_dict import EamRecordDict
from .sections.gwy_dict import GwyEamDict, GwyMsrDict
from .sections.hd_dict import MsrRefDict, ParaRefDict
from .sections.hw2_dict import BeginIODescriptionDict, Hw2BlobDict, Hw2NodeDict
from .sections.msr_dict import MsrRecordDict, UidAccDict
from .sections.node_dict import PbNodeDict
from .sections.para_dict import ParaDataDict
from .sections.patchtable_dict import PatchtableDict
from .sections.pbaum_dict import PbvObjpathDict
from .sections.resourcen_dict import EamResourceDict
from .utils import (
    Create, create_ascii_hex, create_string_from_dict_with_list_of_dicts, create_string_from_dict_with_string
    )


def ValidatorAssignment(**kwargs):

    def Assignment(cls):
        for parameter, expected_validator in kwargs.items():
            setattr(cls, parameter, expected_validator(parameter))
        return cls

    return Assignment


@ValidatorAssignment(ID=Identification)
class RowIdentification(ABC):

    def __init__(self, **kwargs) -> None:
        self.ID = kwargs["ID"]

    def _get_string_from_dict_with_string(self, dict_of_strings: Dict) -> str:
        created_string = Create(dict_of_strings)
        return created_string.execute(create_string_from_dict_with_string(sep=";"))

    def _get_string_from_dict_with_dict(self, dict_with_list_of_dicts: Dict) -> str:
        created_string = Create(dict_with_list_of_dicts)
        return created_string.execute(create_string_from_dict_with_list_of_dicts(sep=";"))

    def _get_string_ascii_hex(self, ascii_list: List[str]) -> str:
        created_string = Create(ascii_list)
        return created_string.execute(create_ascii_hex())

    @abstractmethod
    def string(self) -> str:
        pass

    def dict(self, exclude: list = None):
        if exclude is not None:
            return {k: self.__dict__[k] for k in self.__dict__.keys() - exclude}
        return self.__dict__


@ValidatorAssignment(
    NA=ValueTrueOrFalse,
    MP=MeasuringPoint,
    MT=ModuleType,
    ST=Max12Chars,
    LT=Max30Chars,
    NI1=NoIdear,
    AD=AreaDefinition,
    SB=ValueTrueOrFalse,
    NI2=NoIdear,
    NI3=NoIdear,
    NI4=NoIdear,
    NI5=NoIdear,
    )
class MsrRec(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NA = kwargs["NA"]
        self.MP = kwargs["MP"]
        self.LB = kwargs["LB"]
        self.MT = kwargs["MT"]
        self.ST = kwargs["ST"]
        self.LT = kwargs["LT"]
        self.NI1 = kwargs["NI1"]
        self.AD = kwargs["AD"]
        self.SB = kwargs["SB"]
        self.NI2 = kwargs["NI2"]
        self.NI3 = kwargs["NI3"]
        self.NI4 = kwargs["NI4"]
        self.NI5 = kwargs["NI5"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


@ValidatorAssignment(LEN=Length, PARA=ParaForUidAcc)
class UidAcc(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LEN: int = kwargs["LEN"]
        self.PARA: list = kwargs["PARA"]

    def string(self) -> str:
        uid_string = self._get_string_from_dict_with_dict(self.PARA)
        return f"{self.ID};{self.LEN};{uid_string}"


@ValidatorAssignment(LEN=Length, PARA=ParaForParaData)
class ParaData(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LEN: int = kwargs["LEN"]
        self.PARA: list = kwargs["PARA"]

    def string(self) -> str:
        para_string = self._get_string_from_dict_with_dict(self.PARA)
        return f"{self.ID};{self.LEN};{para_string}"


@ValidatorAssignment(
    NA=ValueTrueOrFalse,
    LB=Libary,
    FN=MeasuringPoint,
    )
class PBNode(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NA: int = kwargs["NA"]
        self.LB: str = kwargs["MT"]
        self.FN: str = kwargs["FN"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


@ValidatorAssignment(
    NA=ValueTrueOrFalse,
    VN=VariabelName,
    NI1=NoIdear,
    DT=DataTyp,
    VT=Max30Chars,
    PI=ValueTrueOrFalse,
    EX=ValueTrueOrFalse
    )
class EamRecord(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NA: int = kwargs["NA"]
        self.VN: str = kwargs["VN"]
        self.NI1: int = kwargs["NI1"]
        self.DT: str = kwargs["DT"]
        self.VT: str = kwargs["VT"]
        self.PI: int = kwargs["PI"]
        self.EX: int = kwargs["EX"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


@ValidatorAssignment(NA=ValueTrueOrFalse, AC=AreaChar, AL=AreaLength, AN=Max16Chars)
class Area(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NA: int = kwargs["NA"]
        self.AC: str = kwargs["AC"]
        self.LA: int = kwargs["LA"]
        self.AN: str = kwargs["AN"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


@ValidatorAssignment(NA=ValueTrueOrFalse, VN=VariabelName, PS=ProcessStation)
class EamResourceassocation(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NA: int = kwargs["NA"]
        self.VN: str = kwargs["VN"]
        self.PS: str = kwargs["PS"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


@ValidatorAssignment(VAR=Var, DT=DataTyp, NI1=NoIdear, PI=ValueTrueOrFalse, VC=ValueTrueOrFalse)
class ParaRef(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.VAR: str = kwargs["VAR"]
        self.DT: str = kwargs["DT"]
        self.NI1: int = kwargs["NI1"]
        self.PI: int = kwargs["PI"]
        self.VC: int = kwargs["VC"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


@ValidatorAssignment(MP=MeasuringPoint)
class MsrRef(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.MP: str = kwargs["MP"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


@ValidatorAssignment(NA=ValueTrueOrFalse, LB=Libary, FN=MeasuringPoint)
class PbvOpjpath(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NA: int = kwargs["NA"]
        self.LB: str = kwargs["LB"]
        self.FN: str = kwargs["FN"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


@ValidatorAssignment(VN=VariabelName, LEN=Length, PARA=ParaForGwy, NA=ValueTrueOrFalse)
class GwyAccEam(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.VN: str = kwargs["VN"]
        self.LEN: int = kwargs["LEN"]
        self.PARA: list = kwargs["PARA"]
        self.NA: int = kwargs["NA"]

    def string(self) -> str:
        gwy_string = self._get_string_from_dict_with_dict(self.PARA)
        if self.PARA == []:
            return f"{self.ID};{self.VN};{self.LEN};{self.NA}"
        return f"{self.ID};{self.VN};{self.LEN};{gwy_string};{self.NA}"


@ValidatorAssignment(MP=MeasuringPoint, LEN=Length, PARA=ParaForGwy, NA=ValueTrueOrFalse)
class GwyAccMsr(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.MP: str = kwargs["MP"]
        self.LEN: int = kwargs["LEN"]
        self.PARA: list = kwargs["PARA"]
        self.NA: int = kwargs["NA"]

    def string(self) -> str:
        gwy_string = self._get_string_from_dict_with_dict(self.PARA)
        if self.PARA == []:
            return f"{self.ID};{self.MP};{self.LEN};{self.NA}"
        return f"{self.ID};{self.MP};{self.LEN};{gwy_string};{self.NA}"


class Hw2Blob(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DTMN: int = kwargs["DTMN"]
        self.QC: int = kwargs["QC"]
        self.DTMC: tuple = kwargs["DTMC"]

    def string(self) -> str:
        hex_string = self._get_string_ascii_hex(self.DTMC)
        return f"{self.ID};{self.DTMN};{self.QC};{hex_string}"


class IoDescription(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.CN: str = kwargs["CN"]
        self.IO: int = kwargs["IO"]
        self.DT: int = kwargs["DT"]
        self.UB: int = kwargs["UB"]
        self.B: int = kwargs["B"]
        self.BL: int = kwargs["BL"]
        self.VN: str = kwargs["VN"]
        self.C: str = kwargs["C"]
        self.NI1: int = kwargs["NI1"]
        self.NI2: int = kwargs["NI2"]
        self.NI3: int = kwargs["NI3"]
        self.NI4: int = kwargs["NI4"]
        self.NI5: int = kwargs["NI5"]
        self.NI6: int = kwargs["NI6"]
        self.NI7: int = kwargs["NI7"]
        self.NI8: int = kwargs["NI8"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


class Hw2Node(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.RID: str = kwargs["RID"]
        self.NI1: str = kwargs["NI1"]
        self.NI2: str = kwargs["NI2"]
        self.NI3: str = kwargs["NI3"]
        self.NI4: str = kwargs["NI4"]
        self.MT: str = kwargs["MT"]
        self.LB: str = kwargs["LB"]
        self.NI5: str = kwargs["NI5"]
        self.NI6: str = kwargs["NI6"]
        self.NI7: str = kwargs["NI7"]
        self.NI8: str = kwargs["NI8"]
        self.NI9: str = kwargs["NI9"]
        self.NI10: str = kwargs["NI10"]
        self.NI11: str = kwargs["NI11"]
        self.NI12: str = kwargs["NI12"]
        self.NI13: str = kwargs["NI13"]
        self.NI14: str = kwargs["NI14"]
        self.NI15: str = kwargs["NI15"]
        self.MP: str = kwargs["MP"]
        self.PS: str = kwargs["PS"]
        self.NA: int = kwargs["NA"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


class PatchtableRecord(RowIdentification):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NA: int = kwargs["NA"]
        self.MT: str = kwargs["MT"]
        self.LB: str = kwargs["LB"]
        self.NI1: int = kwargs["NI1"]
        self.NI2: int = kwargs["NI2"]
        self.NI3: int = kwargs["NI3"]
        self.NI4: int = kwargs["NI4"]
        self.PO: int = kwargs["PO"]
        self.NI5: int = kwargs["NI5"]
        self.NI6: int = kwargs["NI6"]
        self.NI7: int = kwargs["NI7"]
        self.NI8: int = kwargs["NI8"]
        self.NI9: str = kwargs["NI9"]
        self.NI10: int = kwargs["NI10"]
        self.NI11: int = kwargs["NI11"]
        self.NI12: int = kwargs["NI12"]
        self.NI13: str = kwargs["NI13"]
        self.NI14: int = kwargs["NI14"]
        self.NI15: int = kwargs["NI15"]
        self.NI16: int = kwargs["NI16"]
        self.NI17: str = kwargs["NI17"]
        self.NI18: str = kwargs["NI18"]

    def string(self) -> str:
        return self._get_string_from_dict_with_string(self.dict())


__FREELANCE_IDENTIFICATION = {
    "[MSR:RECORD]": (MsrRec, MsrRecordDict),
    "[UID:ACCMSR]": (UidAcc, UidAccDict),
    "[PARA:PARADATA]": (ParaData, ParaDataDict),
    "[PB:NODE]": (PBNode, PbNodeDict),
    "[EAM:RECORD]": (EamRecord, EamRecordDict),
    "[AREA]": (Area, AreaDict),
    "[EAM:RESOURCEASSOCIATION]": (EamResourceassocation, EamResourceDict),
    "[LAD:PARA_REF]": (ParaRef, ParaRefDict),
    "[LAD:MSR_REF]": (MsrRef, MsrRefDict),
    "[PBV:OBJPATH]": (PbvOpjpath, PbvObjpathDict),
    "[GWY:ACCEAM]": (GwyAccEam, GwyEamDict),
    "[GWY:ACCMSR]": (GwyAccMsr, GwyMsrDict),
    "[HW2_BLOB]": (Hw2Blob, Hw2BlobDict),
    "[BEGIN_IODESCRIPTION]": (IoDescription, BeginIODescriptionDict),
    "[HW2_NODE]": (Hw2Node, Hw2NodeDict),
    "[PATCHTABLE:RECORD]": (PatchtableRecord, PatchtableDict)
    }


def row_identificator(row: tuple[str]) -> RowIdentification:
    if row[0] not in __FREELANCE_IDENTIFICATION.keys():
        raise AttributeError('cant find identificator!')
    (id, CreateDict) = __FREELANCE_IDENTIFICATION[row[0]]
    row_dict = CreateDict().merge_dict(row)
    return id(**row_dict)
