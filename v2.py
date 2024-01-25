import os
from pypdf import PdfReader, PdfWriter

def split_pdf_by_size(file_path, max_file_size_mb):
    # PDFファイルを読み込む
    reader = PdfReader(file_path)
    total_pages = len(reader.pages)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    start_page = 0
    while start_page < total_pages:
        end_page = start_page
        writer = PdfWriter()

        # 各ページを追加し、ファイルサイズを確認する
        while end_page < total_pages:
            writer.add_page(reader.pages[end_page])
            end_page += 1

            # 現在の状態を一時ファイルに保存してサイズをチェック
            temp_filename = f"{base_name}_temp.pdf"
            with open(temp_filename, "wb") as f:
                writer.write(f)

            # 一時ファイルのサイズをMB単位で取得
            temp_file_size_mb = os.path.getsize(temp_filename) / (1024 * 1024)
            if temp_file_size_mb > max_file_size_mb:
                # ファイルサイズが大きすぎる場合は、最後に追加したページを破棄
                end_page -= 1
                break

        # 分割されたファイルを保存（少なくとも1ページ以上含む場合）
        if end_page > start_page:
            split_filename = f"{base_name}_{start_page + 1}_{end_page}.pdf"
            with open(split_filename, "wb") as f:
                writer = PdfWriter()
                for page in range(start_page, end_page):
                    writer.add_page(reader.pages[page])
                writer.write(f)
            print(f"作成されたファイル: {split_filename}")

        # 次の分割のために開始ページを更新
        start_page = end_page
        # 一時ファイルを削除
        os.remove(temp_filename)

# 使用例
# "20220706 「試行錯誤を許容するおもしろ環境のつくりかた」  (登 大遊, 2022).pdf"を指定のファイルパスに置き換えてください
split_pdf_by_size("example.pdf", 10)
