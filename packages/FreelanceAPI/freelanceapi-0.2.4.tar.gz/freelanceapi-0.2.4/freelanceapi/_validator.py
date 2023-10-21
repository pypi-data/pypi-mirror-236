import re


class Identification:

    def __init__(self, value: str):
        self.id = value
        self.expected_type = [str]
        self._row_idents = [
            "[MSR:RECORD]", "[UID:ACCMSR]", "[PARA:PARADATA]", "[PB:NODE]", "[EAM:RECORD]", "[AREA]",
            "[EAM:RESOURCEASSOCIATION]", "[LAD:PARA_REF]", "[LAD:MSR_REF]", "[PBV:OBJPATH]", "[GWY:ACCEAM]",
            "[GWY:ACCMSR]", "[HW2_BLOB]", "[BEGIN_IODESCRIPTION]", "[HW2_NODE]", "[PATCHTABLE:RECORD]"
            ]

    def __get__(self, instance, cls):
        return instance.__dict__[self.id]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        elif value not in self._row_idents:
            raise ValueError(f'Row Identification is invalid! valid ->{self._row_idents}')
        else:
            instance.__dict__[self.id] = value


class ValueTrueOrFalse:

    def __init__(self, value: str | int):
        self.value = value
        self.expected_type = [str, int]
        self._nextelement_numbers = [0, 1]

    def __get__(self, instance, cls):
        return instance.__dict__[self.value]

    def __set__(self, instance, value: str | int):
        if not isinstance(value, str) and not isinstance(value, int):
            raise TypeError(f"{self.expected_type} value is expected")
        elif int(value) not in self._nextelement_numbers:
            raise ValueError(f'Value passed is not correct! Available values -> {self._nextelement_numbers}')
        else:
            instance.__dict__[self.value] = int(value)


class MeasuringPoint:

    def __init__(self, value: str):
        self.mp = value
        self.expected_type = [str]
        self._max_len: int = 17

    def __get__(self, instance, cls):
        return instance.__dict__[self.mp]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        elif re.search("""[!\"#$%&'()*+,./:;<=>?@[\]^`{|}~]""", value):
            raise ValueError('Value contains characters that are not allowed')
        elif len(value) > self._max_len:
            raise ValueError(f'Value ist to long max. len {self._max_len}')
        elif not re.search("^[a-zA-Z_]", value):
            raise ValueError('There is no character in the first place of the string')
        else:
            instance.__dict__[self.mp] = value


class VariabelName:

    def __init__(self, value: str):
        self.vn = value
        self.expected_type = [str]
        self._max_len: int = 17

    def __get__(self, instance, cls):
        return instance.__dict__[self.vn]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        elif re.search("""[!\"#$%&'()*+,./:;<=>?@[\]^`{|}~]""", value):
            raise ValueError('Value contains characters that are not allowed')
        elif len(value) > self._max_len:
            raise ValueError(f'Value ist to long max. len {self._max_len}')
        else:
            instance.__dict__[self.vn] = value


class Var:

    def __init__(self, value: str):
        self.vn = value
        self.expected_type = [str]
        self._max_len: int = 17

    def __get__(self, instance, cls):
        return instance.__dict__[self.vn]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        elif re.search("""[!\"#$%&'()*+,/:;<=>?@[\]^`{|}~]""", value):
            raise ValueError('Value contains characters that are not allowed')
        elif len(value) > self._max_len:
            raise ValueError(f'Value ist to long max. len {self._max_len}')
        else:
            instance.__dict__[self.vn] = value


class ModuleType:

    def __init__(self, value: str):
        self.mt = value
        self.expected_type = [str]
        #self._module_typs = ["M_BIN", "M_ANA", "C_CU", "IDF", "S800_AIW"]

    def __get__(self, instance, cls):
        return instance.__dict__[self.mt]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        # elif value not in self._module_typs:
        #     raise ValueError(f'Module type does not exist! Available modules -> {self._module_typs}')
        else:
            instance.__dict__[self.mt] = value


class Max12Chars:

    def __init__(self, value: str):
        self.value = value
        self.expected_type = [str]
        self._max_len: int = 12

    def __get__(self, instance, cls):
        return instance.__dict__[self.value]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        elif len(value) > self._max_len:
            raise ValueError(f'Value ist to long max. len {self._max_len}')
        else:
            instance.__dict__[self.value] = value


class Max16Chars:

    def __init__(self, value: str):
        self.value = value
        self.expected_type = [str]
        self._max_len: int = 16

    def __get__(self, instance, cls):
        return instance.__dict__[self.value]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        elif len(value) > self._max_len:
            raise ValueError(f'Value ist to long max. len {self._max_len}')
        else:
            instance.__dict__[self.value] = value


class Max30Chars:

    def __init__(self, value: str):
        self.value = value
        self.expected_type = [str]
        self._max_len: int = 30

    def __get__(self, instance, cls):
        return instance.__dict__[self.value]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        if len(value) > self._max_len:
            raise ValueError(f'Value ist to long max. len {self._max_len}')
        else:
            instance.__dict__[self.value] = value


class AreaDefinition:

    def __init__(self, value: str | int):
        self.ad = value
        self.expected_type = [str, int]
        self._area_numbers = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]

    def __get__(self, instance, cls):
        return instance.__dict__[self.ad]

    def __set__(self, instance, value: str):
        if not isinstance(value, str) and not isinstance(value, int):
            raise TypeError(f"{self.expected_type} value is expected")
        elif int(value) not in self._area_numbers:
            raise ValueError(f'Area Number is invalid! valid ->{self._area_numbers}')
        else:
            instance.__dict__[self.ad] = value


class DataTyp:

    def __init__(self, value: str):
        self.dt = value
        self.expected_type = [str]
        self._data_typs = [
            "BOOL", "INT", "DINT", "UINT", "UDINT", "REAL", "TIME", "DT", "BYTE", "WORD", "DWORD", "STR8", "STR16",
            "STR32", "STR64", "STR128", "STR256"
            ]

    def __get__(self, instance, cls):
        return instance.__dict__[self.dt]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        elif value not in self._data_typs:
            raise ValueError(f'Datatyp is invalid! valid ->{self._data_typs}')
        else:
            instance.__dict__[self.dt] = value


class NoIdear:

    def __init__(self, value: str):
        self.NI = value
        self.expected_type = [str]

    def __get__(self, instance, cls):
        return instance.__dict__[self.NI]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        else:
            instance.__dict__[self.NI] = value


class AreaChar:

    def __init__(self, value: str):
        self.AC = value
        self.expected_type = [str]
        self._area_chars = ["!", "-", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]

    def __get__(self, instance, cls):
        return instance.__dict__[self.AC]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        elif len(value) > 1:
            raise TypeError("Area Charakter is to long max len = 1")
        elif value not in self._area_chars:
            raise ValueError(f'Area Charakter is invalid! valid ->{self._area_chars}')
        else:
            instance.__dict__[self.AC] = value


class AreaLength:

    def __init__(self, value: str | int):
        self.value = value
        self.expected_type = [str, int]

    def __get__(self, instance, cls):
        return instance.__dict__[self.value]

    def __set__(self, instance, value: str | int):
        if isinstance(value, str):
            instance.__dict__[self.value] = len(value)
        elif isinstance(value, int):
            instance.__dict__[self.value] = value
        else:
            raise TypeError(f"{self.expected_type} value is expected")


class ParaLength:

    def __init__(self, value: list | int):
        self.value = value
        self.expected_type = [list, int]

    def __get__(self, instance, cls):
        return instance.__dict__[self.value]

    def __set__(self, instance, value: list | int):
        if isinstance(value, list):
            instance.__dict__[self.value] = len(value)
        elif isinstance(value, int):
            instance.__dict__[self.value] = value
        else:
            raise TypeError(f"{self.expected_type} value is expected")


class ProcessStation:

    def __init__(self, value: str):
        self.PS = value
        self.expected_type = [str]

    def __get__(self, instance, cls):
        return instance.__dict__[self.PS]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        else:
            instance.__dict__[self.PS] = value


class Libary:

    # Libary Avabile-> DIGBLT

    def __init__(self, value: str):
        self.LB = value
        self.expected_type = [str]

    def __get__(self, instance, cls):
        return instance.__dict__[self.LB]

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(f"{self.expected_type} value is expected")
        else:
            instance.__dict__[self.LB] = value


class ParaForParaData:

    def __init__(self, value: list):
        self.para = value
        self.expected_type = [list]

    def __get__(self, instance, cls):
        return instance.__dict__[self.para]

    def __set__(self, instance, value: list):
        if not isinstance(value, list):
            raise TypeError(f"{self.expected_type} value is expected")
        self._check_dict(value)
        instance.__dict__[self.para] = value

    def _check_dict(self, value: list):
        for dictionary in value:
            if int(dictionary["L1"]) != len(dictionary["K1"]):
                raise ValueError(f"legnth of {dictionary['L1']} is not matching with Value {dictionary['K1']}")
            if int(dictionary["L2"]) != len(dictionary["K2"]):
                raise ValueError(f"length of {dictionary['L2']} is not matching with Value {dictionary['K2']}")


class Length:

    def __init__(self, value: int | str | list):
        self.len = value
        self.expected_type = [int | str | list]

    def __get__(self, instance, cls):
        return instance.__dict__[self.len]

    def __set__(self, instance, value: int | str | list):
        if isinstance(value, str):
            instance.__dict__[self.len] = int(value)
        elif isinstance(value, int):
            instance.__dict__[self.len] = value
        elif isinstance(value, list):
            instance.__dict__[self.len] = len(value)
        else:
            raise TypeError(f"{self.expected_type} value is expected")


class ParaForUidAcc:

    def __init__(self, value: list):
        self.para = value
        self.expected_type = [list]

    def __get__(self, instance, cls):
        return instance.__dict__[self.para]

    def __set__(self, instance, value: list):
        if not isinstance(value, list):
            raise TypeError(f"{self.expected_type} value is expected")
        self._check_dict(value)
        instance.__dict__[self.para] = value

    def _check_dict(self, value: list):
        valid_uid = [0, 1, 3]
        for dictionary in value:
            if int(dictionary["ACC"]) not in valid_uid:
                raise ValueError(f"{dictionary['ACC']} Access number is not valid. Valid Values -> {valid_uid}")


class ParaForGwy:

    def __init__(self, value: list):
        self.para = value
        self.expected_type = [list]

    def __get__(self, instance, cls):
        return instance.__dict__[self.para]

    def __set__(self, instance, value: list):
        if not isinstance(value, list):
            raise TypeError(f"{self.expected_type} value is expected")
        self._check_dict(value)
        instance.__dict__[self.para] = value

    def _check_dict(self, value: list):
        valid_uid = [0, 1, 3]
        for dictionary in value:
            if int(dictionary["G1"]) not in valid_uid:
                raise ValueError(f"{dictionary['G1']} Access number is not valid. Valid Values -> {valid_uid}")
            if int(dictionary["G2"]) not in valid_uid:
                raise ValueError(f"{dictionary['G1']} Access number is not valid. Valid Values -> {valid_uid}")
