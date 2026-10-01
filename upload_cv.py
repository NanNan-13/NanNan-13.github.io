# -*- coding: utf-8 -*-
"""
一键流程：CV 文件夹中的 .docx 简历 -> 转 PDF -> git add -> 手敲 commit 信息提交 -> 推送。

用法：
    python upload_cv.py

commit 信息会在运行时提示输入（直接回车则取消提交）。
配置见同目录 cv_upload.json。
"""
import glob
import json
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "cv_upload.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run(cmd, **kw):
    print("  $", " ".join(cmd))
    return subprocess.run(cmd, cwd=BASE_DIR, text=True,
                          capture_output=True, **kw)


def convert_docx_to_pdf(docx_path):
    """调用本机 Word 将 docx 转为同名 pdf，返回 pdf 路径。"""
    pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(docx_path, ReadOnly=True)
        doc.SaveAs(pdf_path, FileFormat=17)  # 17 = wdFormatPDF
        doc.Close(False)
    finally:
        word.Quit()
    if not os.path.exists(pdf_path):
        raise RuntimeError("转换后未找到 PDF 文件")
    return pdf_path


def main():
    cfg = load_config()
    cv_dir = os.path.join(BASE_DIR, cfg["cv_dir"])

    # 1. 转换 docx -> pdf
    docx_files = [p for p in glob.glob(os.path.join(cv_dir, cfg["docx_pattern"]))
                  if not os.path.basename(p).startswith(cfg["skip_prefix"])]
    if not docx_files:
        sys.exit(f"未在 {cv_dir} 中找到 docx 文件")

    staged = []
    for docx_path in docx_files:
        pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
        if os.path.exists(pdf_path):
            print(f"PDF 已存在，跳过转换: {os.path.basename(pdf_path)}")
        else:
            print(f"转换中: {os.path.basename(docx_path)}")
            convert_docx_to_pdf(docx_path)
            print(f"  -> {os.path.basename(pdf_path)}")
        staged.append(docx_path)
        staged.append(pdf_path)

    for extra in cfg.get("extra_add_paths", []):
        p = os.path.join(BASE_DIR, extra)
        if os.path.exists(p):
            staged.append(p)

    # 2. git add
    rel = [os.path.relpath(p, BASE_DIR) for p in staged]
    result = run(["git", "add", "--"] + rel)
    if result.returncode != 0:
        sys.exit(f"git add 失败:\n{result.stderr}")

    status = run(["git", "status", "--short"])
    print("\n待提交的变更：")
    print(status.stdout or "（无变更）")
    if not status.stdout.strip():
        print("没有需要提交的修改。")
        return

    # 3. 运行时手敲 commit 信息
    try:
        message = input("\n请输入 commit 信息（回车取消提交）: ").strip()
    except EOFError:
        message = ""
    if not message:
        print("已取消提交（文件仍保留在暂存区）。")
        return

    result = run(["git", "commit", "-m", message])
    print(result.stdout or result.stderr)
    if result.returncode != 0:
        sys.exit("git commit 失败")

    # 4. 推送
    if cfg.get("push_after_commit", True):
        result = run(["git", "push", "origin", cfg.get("branch", "main")])
        print(result.stdout or result.stderr)
        if result.returncode != 0:
            sys.exit("git push 失败")
    print("\n完成 ✅")


if __name__ == "__main__":
    main()
