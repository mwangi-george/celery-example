import io
import time
from openpyxl import Workbook


def generate_excel_workbook(title: str, rows: list[list[str]]) -> bytes:
    time.sleep(90)

    # Initialize workbook
    wb = Workbook()
    ws = wb.active
    ws.title = title

    # write rows to Excel sheet
    for row in rows:
        ws.append(row)

    # save workbook to an in-memory bytes buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    # return the generate workbook in bytes
    return buffer.getvalue()



