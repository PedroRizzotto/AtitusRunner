from enum import IntFlag

import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 as __wrapper_module__
from comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 import (
    OLE_HANDLE, FONTUNDERSCORE, OLE_XPOS_CONTAINER, Font, StdFont,
    OLE_XSIZE_HIMETRIC, Picture, IFontEventsDisp, OLE_OPTEXCLUSIVE,
    IEnumVARIANT, OLE_YPOS_PIXELS, CoClass, VgaColor, FONTITALIC,
    FONTBOLD, Gray, IPictureDisp, _lcid, IFont, Default, BSTR,
    IFontDisp, OLE_XPOS_HIMETRIC, VARIANT_BOOL, Color, Checked,
    HRESULT, OLE_YPOS_HIMETRIC, dispid, DISPPARAMS,
    OLE_YSIZE_CONTAINER, OLE_YSIZE_PIXELS, OLE_ENABLEDEFAULTBOOL,
    StdPicture, OLE_XPOS_PIXELS, FONTSTRIKETHROUGH,
    OLE_YPOS_CONTAINER, FONTSIZE, FontEvents, OLE_XSIZE_PIXELS,
    COMMETHOD, Library, DISPPROPERTY, IDispatch, IUnknown,
    OLE_YSIZE_HIMETRIC, _check_version, IPicture, OLE_CANCELBOOL,
    OLE_COLOR, Monochrome, OLE_XSIZE_CONTAINER, typelib_path,
    FONTNAME, EXCEPINFO, DISPMETHOD, Unchecked, GUID
)


class OLE_TRISTATE(IntFlag):
    Unchecked = 0
    Checked = 1
    Gray = 2


class LoadPictureConstants(IntFlag):
    Default = 0
    Monochrome = 1
    VgaColor = 2
    Color = 4


__all__ = [
    'OLE_HANDLE', 'OLE_YSIZE_CONTAINER', 'FONTUNDERSCORE',
    'OLE_YSIZE_PIXELS', 'OLE_ENABLEDEFAULTBOOL', 'OLE_XPOS_CONTAINER',
    'Font', 'StdPicture', 'OLE_XPOS_PIXELS', 'StdFont',
    'LoadPictureConstants', 'OLE_XSIZE_HIMETRIC', 'FONTSIZE',
    'Picture', 'FONTSTRIKETHROUGH', 'OLE_YPOS_CONTAINER',
    'IFontEventsDisp', 'FontEvents', 'OLE_OPTEXCLUSIVE',
    'OLE_XSIZE_PIXELS', 'OLE_YPOS_PIXELS', 'Library', 'VgaColor',
    'FONTITALIC', 'OLE_TRISTATE', 'FONTBOLD', 'Gray', 'IPictureDisp',
    'OLE_YSIZE_HIMETRIC', 'IFont', 'IPicture', 'OLE_CANCELBOOL',
    'OLE_COLOR', 'Default', 'Monochrome', 'IFontDisp',
    'OLE_XPOS_HIMETRIC', 'OLE_XSIZE_CONTAINER', 'typelib_path',
    'FONTNAME', 'Color', 'Checked', 'OLE_YPOS_HIMETRIC', 'Unchecked'
]

