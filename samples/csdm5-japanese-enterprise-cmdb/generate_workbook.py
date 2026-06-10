#!/usr/bin/env python3
"""Generate an Excel workbook for the CSDM 5 Japanese enterprise CMDB sample.

The repository intentionally avoids adding Python package dependencies, so this
script writes the small XLSX Open Packaging Convention files directly with the
standard library.
"""

from __future__ import annotations

import csv
import html
import re
import zipfile
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "csdm5_japanese_enterprise_cmdb_sample.xlsx"
CSV_FILES = [
    "01_foundation_core.csv",
    "02_business_capabilities.csv",
    "03_business_applications.csv",
    "04_business_services.csv",
    "05_technical_services.csv",
    "06_service_offerings.csv",
    "07_service_instances.csv",
    "08_infrastructure_cis.csv",
    "09_cmdb_rel_ci.csv",
    "10_svc_ci_assoc.csv",
]
SHEET_NAMES = {
    "01_foundation_core.csv": "01 Foundation",
    "02_business_capabilities.csv": "02 Capabilities",
    "03_business_applications.csv": "03 Business Apps",
    "04_business_services.csv": "04 Business Services",
    "05_technical_services.csv": "05 Technical Services",
    "06_service_offerings.csv": "06 Offerings",
    "07_service_instances.csv": "07 Service Instances",
    "08_infrastructure_cis.csv": "08 Infrastructure CIs",
    "09_cmdb_rel_ci.csv": "09 Relationships",
    "10_svc_ci_assoc.csv": "10 Service CI Assoc",
}

_FIXED_ZIP_TIMESTAMP = (2026, 6, 10, 0, 0, 0)
_INVALID_XML_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def clean_text(value: object) -> str:
    return _INVALID_XML_CHARS.sub("", "" if value is None else str(value))


def xml_escape(value: object) -> str:
    return html.escape(clean_text(value), quote=True)


def column_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def read_csv(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise ValueError(f"{path} is empty")
    width = len(rows[0])
    for row_number, row in enumerate(rows, start=1):
        if len(row) != width:
            raise ValueError(
                f"{path}:{row_number} has {len(row)} columns; expected {width}"
            )
    return rows


def worksheet_xml(rows: list[list[str]]) -> str:
    row_count = len(rows)
    column_count = len(rows[0]) if rows else 1
    last_cell = f"{column_name(column_count)}{row_count}"

    max_widths = [0] * column_count
    for row in rows:
        for index, value in enumerate(row):
            max_widths[index] = max(max_widths[index], min(len(clean_text(value)) + 2, 60))

    cols_xml = "".join(
        f'<col min="{index}" max="{index}" width="{max(width, 10)}" customWidth="1"/>'
        for index, width in enumerate(max_widths, start=1)
    )

    sheet_rows = []
    for row_index, row in enumerate(rows, start=1):
        cells = []
        style = ' s="1"' if row_index == 1 else ""
        for column_index, value in enumerate(row, start=1):
            ref = f"{column_name(column_index)}{row_index}"
            cells.append(
                f'<c r="{ref}" t="inlineStr"{style}><is><t>{xml_escape(value)}</t></is></c>'
            )
        sheet_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <dimension ref="A1:{last_cell}"/>
  <sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>
  <sheetFormatPr defaultRowHeight="15"/>
  <cols>{cols_xml}</cols>
  <sheetData>{''.join(sheet_rows)}</sheetData>
  <autoFilter ref="A1:{last_cell}"/>
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
</worksheet>
'''


def workbook_xml(sheet_names: Iterable[str]) -> str:
    sheets = "".join(
        f'<sheet name="{xml_escape(name)}" sheetId="{index}" r:id="rId{index}"/>'
        for index, name in enumerate(sheet_names, start=1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <workbookPr date1904="false"/>
  <sheets>{sheets}</sheets>
</workbook>
'''


def workbook_rels_xml(sheet_count: int) -> str:
    worksheet_rels = "".join(
        f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{index}.xml"/>'
        for index in range(1, sheet_count + 1)
    )
    styles_id = sheet_count + 1
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {worksheet_rels}
  <Relationship Id="rId{styles_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
'''


def content_types_xml(sheet_count: int) -> str:
    sheet_overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for index in range(1, sheet_count + 1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  {sheet_overrides}
</Types>
'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="11"/><name val="Calibri"/></font>
  </fonts>
  <fills count="2">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
  </fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="2">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>
'''


def root_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
'''


def write_zip_entry(archive: zipfile.ZipFile, name: str, content: str | bytes) -> None:
    info = zipfile.ZipInfo(name, _FIXED_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    data = content.encode("utf-8") if isinstance(content, str) else content
    archive.writestr(info, data)


def main() -> None:
    worksheets = []
    for csv_name in CSV_FILES:
        rows = read_csv(BASE_DIR / csv_name)
        worksheets.append((SHEET_NAMES[csv_name], rows))

    with zipfile.ZipFile(OUTPUT, "w") as archive:
        write_zip_entry(archive, "[Content_Types].xml", content_types_xml(len(worksheets)))
        write_zip_entry(archive, "_rels/.rels", root_rels_xml())
        write_zip_entry(archive, "xl/workbook.xml", workbook_xml(name for name, _ in worksheets))
        write_zip_entry(archive, "xl/_rels/workbook.xml.rels", workbook_rels_xml(len(worksheets)))
        write_zip_entry(archive, "xl/styles.xml", styles_xml())
        for index, (_, rows) in enumerate(worksheets, start=1):
            write_zip_entry(archive, f"xl/worksheets/sheet{index}.xml", worksheet_xml(rows))

    print(f"Wrote {OUTPUT.relative_to(BASE_DIR.parent.parent)}")


if __name__ == "__main__":
    main()
