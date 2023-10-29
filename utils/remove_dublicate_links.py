# Открываем файл для чтения
with open('assets/sites_to_crawl/sites.txt', 'r') as file:
    links = file.readlines()

# Удаляем дубликаты
unique_links = list(set(links))

# Сортируем ссылки (если нужно сохранить исходный порядок, этот шаг можно пропустить)
unique_links.sort()

# Записываем обратно в файл
with open('assets/sites_to_crawl/sites.txt', 'w') as file:
    file.writelines(unique_links)
