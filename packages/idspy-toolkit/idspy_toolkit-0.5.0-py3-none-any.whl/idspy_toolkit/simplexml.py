from __future__ import annotations

import dataclasses
from typing import Any
import defusedxml.ElementTree as ET
from collections import defaultdict
import xml.etree.ElementTree as ETw

# Define a dict to map the Python type names to string
XML_TYPES = {list: 'list', int: 'int', float: 'float', dict: 'dict', bool: 'bool', complex: 'complex'}


def __parse_list(v):
    list_val = []
    for elem in v.get("item"):
        if elem.get("item") is not None:
            list_val.append(__parse_list(elem))
        else:
            list_val.append(_parse_xml(elem))
    return list_val


def clean_key(key: str) -> str:
    return key.strip().lstrip("#").lstrip("@")


def guess_from_val(value: str):
    if isinstance(value, dict):
        return value
    try:
        val = int(value)
    except ValueError:
        try:
            val = float(value)
        except ValueError:
            try:
                val = complex(value)
            except ValueError:
                if value.strip().lower() == "false":
                    val = False
                elif value.strip().lower() == "true":
                    val = True
                else:
                    val = value
    return val


@dataclasses.dataclass
class XmlAttrib:
    text: str | None = dataclasses.field(default="")
    type: str | None = dataclasses.field(default=None)
    value: Any = dataclasses.field(init=False)

    def __post_init__(self):
        self.value = None
        if self.type == "int":
            self.value = int(self.text)
        elif self.type == "float":
            self.value = float(self.text)
        elif self.type == "number":
            self.value = complex(self.text)
        elif self.type == "bool":
            if self.text.lower().strip().strip('.') == "true":
                self.value = True
            elif self.text.lower().strip().strip('.') == "false":
                self.value = False
        elif self.type in ("dict", "str"):
            self.value = self.text
        elif self.type == "list":
            self.value = [guess_from_val(x.strip(",").strip()) for x in self.text.split(",")]
        elif self.type == "null":
            self.value = None
        else:
            self.value = guess_from_val(self.text)


def _parse_xml(xmldict: str | dict, current_dict: dict | None = None) -> dict | Any:
    if not isinstance(xmldict, dict):
        return xmldict
    xmldict = dict(xmldict)
    if "@type" in xmldict.keys():
        if xmldict.get("@type", "").find("dict") == -1:
            return XmlAttrib(xmldict.get("#text", xmldict), xmldict.get("@type", None)).value
        else:
            xmldict.pop("@type")

    if current_dict is None:
        current_dict = {}
    tmp_dict = current_dict
    for k, v in xmldict.items():
        if isinstance(v, dict):
            if v.get("@type", "") == "dict":
                v.pop("@type")
                tmp_dict.update({k: _parse_xml(v)})
            elif v.get("@type", "") == "list":

                entry = __parse_list(v)
                tmp_dict.update({k: entry})
            else:
                entry = XmlAttrib(v.get("#text", v), v.get("@type", None)).value
                tmp_dict.update({k: _parse_xml(entry)})
        elif isinstance(v, list):
            entry = [_parse_xml(elem) for elem in v]
            tmp_dict.update({k: entry})
        else:
            entry = XmlAttrib(v).value
            tmp_dict.update({k: entry})
    return tmp_dict


def etree_to_dict(t):
    """Converts defusedxml.ElementTree to a dict."""

    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d.get("root", d)


def xml_to_dict(xmlstr):
    root = ET.fromstring(xmlstr)
    return _parse_xml(etree_to_dict(root))


def dict_to_xml(d: dict) -> str:

    if isinstance(d, dict) is False:
        raise ValueError(f"input parameter must be a dict and not a {type(d)}")

    def _to_etree(d, root):
        if not isinstance(d, (dict, list)):
            root.text = str(d)
            root.set('type', XML_TYPES.get(type(d), 'str'))
        elif isinstance(d, list):
            for i in d:
                item = ETw.SubElement(root, 'item', type=XML_TYPES.get(type(i), 'str'))
                _to_etree(i, item)
        else:  # Assuming dictionary type
            for kk, vv in d.items():
                child = ETw.SubElement(root, kk, type=XML_TYPES.get(type(vv), 'str'))
                _to_etree(vv, child)

    node = ETw.Element('root')  # Create a root tag

    for k, v in d.items():
        _to_etree(v, ETw.SubElement(node, k, type=XML_TYPES.get(type(v), 'str')))

    return ETw.tostring(node, encoding='unicode')
