import os

# Пути к папкам с json и pdf файлами
resource = "edp"
json_folder = f"assets/output/{resource}/jsons"
pdf_folder = f"assets/output/{resource}/pdfs"

# Получаем списки файлов
json_files = [f for f in os.listdir(json_folder) if f.endswith(".json")]
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Создаем txt файл
with open("utils/output.txt", "w") as out_file:
    for json_file in json_files:
        # Убираем расширение из названия json файла и добавляем расширение .pdf
        corresponding_pdf = json_file[:-5] + ".pdf"
        
        if corresponding_pdf in pdf_files:
            out_file.write(f"{json_file},{corresponding_pdf}\n")
        else:
            out_file.write(f"{json_file},-\n")