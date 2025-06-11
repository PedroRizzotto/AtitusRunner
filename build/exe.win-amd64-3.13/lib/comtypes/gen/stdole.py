from enum import IntFlag

import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 as __wrapper_module__
from comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 import (
    CoClass, IPictureDisp, VgaColor, IEnumVARIANT, typelib_path,
    _check_version, OLE_YSIZE_PIXELS, IDispatch, OLE_YPOS_CONTAINER,
    IFont, OLE_XPOS_PIXELS, StdFont, GUID, FONTSIZE, Font,
    OLE_XPOS_CONTAINER, EXCEPINFO, Color, OLE_XSIZE_PIXELS, BSTR,
    VARIANT_BOOL, FONTITALIC, OLE_HANDLE, OLE_XSIZE_HIMETRIC,
    OLE_YPOS_HIMETRIC, Picture, OLE_YSIZE_CONTAINER, DISPMETHOD,
    StdPicture, Checked, OLE_YSIZE_HIMETRIC, FONTSTRIKETHROUGH,
    Unchecked, OLE_CANCELBOOL, OLE_XSIZE_CONTAINER, Gray,
    OLE_ENABLEDEFAULTBOOL, IUnknown, HRESULT, IPicture,
    OLE_YPOS_PIXELS, dispid, DISPPARAMS, FONTBOLD, OLE_COLOR,
    FontEvents, _lcid, OLE_OPTEXCLUSIVE, DISPPROPERTY, FONTUNDERSCORE,
    IFontDisp, OLE_XPOS_HIMETRIC, Default, FONTNAME, IFontEventsDisp,
    Library, Monochrome, COMMETHOD
)


class LoadPictureConstants(IntFlag):
    Default = 0
    Monochrome = 1
    VgaColor = 2
    Color = 4


class OLE_TRISTATE(IntFlag):
    Unchecked = 0
    Checked = 1
    Gray = 2


__all__ = [
    'OLE_XSIZE_HIMETRIC', 'OLE_YPOS_HIMETRIC', 'Picture',
    'OLE_YSIZE_CONTAINER', 'IPictureDisp', 'VgaColor', 'StdPicture',
    'Checked', 'OLE_YSIZE_HIMETRIC', 'typelib_path',
    'FONTSTRIKETHROUGH', 'Unchecked', 'OLE_CANCELBOOL',
    'OLE_YSIZE_PIXELS', 'OLE_XSIZE_CONTAINER', 'Gray',
    'OLE_ENABLEDEFAULTBOOL', 'IPicture', 'OLE_YPOS_CONTAINER',
    'IFont', 'OLE_XPOS_PIXELS', 'OLE_YPOS_PIXELS', 'OLE_TRISTATE',
    'FONTBOLD', 'StdFont', 'OLE_COLOR', 'FontEvents', 'FONTSIZE',
    'Font', 'OLE_XPOS_CONTAINER', 'FONTUNDERSCORE',
    'OLE_OPTEXCLUSIVE', 'IFontDisp', 'OLE_XPOS_HIMETRIC', 'Default',
    'Color', 'FONTNAME', 'IFontEventsDisp', 'Library',
    'OLE_XSIZE_PIXELS', 'Monochrome', 'FONTITALIC',
    'LoadPictureConstants', 'OLE_HANDLE'
]

