# -*- coding: utf-8 -*-
"""
将 CV 文件夹中的 Word 简历（.docx）转换为 PDF。
转换顺序：LibreOffice -> Word COM (docx2pdf) -> Word COM (pywin32)
"""
import os
import sys
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def find_docx():
    files = [f for f in glob.glob(os.path.join(BASE_DIR, "*.docx"))
             if not os.path.basename(f).startswith("~$")]
    if not files:
        sys.exit("未在 CV 文件夹中找到 .docx 文件")
    return files


def convert_by_libreoffice(docx_path, pdf_path):
    soffice = r"C:\Program Files\LibreOffice\program\soffice.exe"
    if not os.path.exists(soffice):
        raise RuntimeError("LibreOffice 未安装")
    import subprocess
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf",
         "--outdir", BASE_DIR, docx_path],
        check=True, timeout=120,
    )
    out = os.path.splitext(docx_path)[0] + ".pdf"
    if pdf_path != out and os.path.exists(out):
        os.replace(out, pdf_path)
    if not os.path.exists(pdf_path):
        raise RuntimeError("LibreOffice 转换后未生成 PDF")


def convert_by_docx2pdf(docx_path, pdf_path):
    from docx2pdf import convert
    convert(docx_path, pdf_path)
    if not os.path.exists(pdf_path):
        raise RuntimeError("docx2pdf 转换后未生成 PDF")


def convert_by_win32com(docx_path, pdf_path):
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(docx_path, ReadOnly=True)
        # FileFormat=17 即 wdFormatPDF
        doc.SaveAs(pdf_path, FileFormat=17)
        doc.Close(False)
    finally:
        word.Quit()
    if not os.path.exists(pdf_path):
        raise RuntimeError("Word COM 转换后未生成 PDF")


def main():
    for docx_path in find_docx():
        pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
        if os.path.exists(pdf_path):
            print(f"已存在，跳过: {pdf_path}")
            continue
        for method in (convert_by_libreoffice, convert_by_docx2pdf,
                       convert_by_win32com):
            try:
                method(docx_path, pdf_path)
                print(f"转换成功 [{method.__name__}]: {docx_path} -> {pdf_path}")
                break
            except Exception as exc:
                print(f"[{method.__name__}] 失败: {exc}")
        else:
            print(f"所有方法均失败: {docx_path}")


if __name__ == "__main__":
    main()
