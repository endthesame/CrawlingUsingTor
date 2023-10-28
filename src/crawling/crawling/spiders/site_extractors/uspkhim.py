from random import randint

def convert_date(date_string):
    # Словарь для преобразования названия месяца в число
    month_mapping = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }

    day, month, year = date_string.split()
    new_date = f"{day}.{month_mapping[month]}.{year}"

    return new_date

def extract_meta_data(response):
    authors_elements = response.css('a.SLink > b')
    authors = []

    for author_element in authors_elements:
        initials = "".join(author_element.css('::text').re(r'[А-Я]\.'))
        surname = author_element.css('::text').re(r'[А-Я][а-я]+')[0]  # Предполагается, что фамилия состоит из заглавной буквы и следующих за ней строчных букв
        authors.append(f"{initials} {surname}")

    authors_string = '; '.join(authors)

    date = response.xpath('//b[contains(text(), "Опубликовано:")]/following-sibling::nobr/text()').get() or ""
    date = convert_date(date)

    other_meta = response.xpath("//body[@text='#000000']/i[2]").get() or ""
    parts = other_meta.split(", ")
    mf_journal = parts[0].replace("<i>", "")
    volume = parts[2].split(" (")
    volume_info = volume[0].replace("<b>", "").replace("</b>", "")
    issue_info = volume[1].replace(")", "")
    pages = parts[3].split("–")
    first_page = pages[0]
    last_page = pages[1].replace("</i>", "")

    meta_data = {
        'title': response.xpath('//div[@style="padding: 5px 5px 5px 0px"]/following-sibling::font/text()').get() or f"Успехи химии {randint(1,100000000000)}",
        'date': date or "",
        'mf_doi': response.xpath('//div[@style="padding: 5px 5px 5px 0px"]/b/a[@class="SLink"]/@href').get() or "",
        'author': authors_string or "",
        'mf_journal': mf_journal or "",
        'volume_info': volume_info or "",
        'issue_info': issue_info or "",
        'first_page': first_page or "",
        'last_page': last_page or "",
        'mf_url': response.url

    }
    return meta_data
def extract_pdf_link(response):
    pdf_link = response.xpath('//a[contains(@href, "getFT")]/@href').get()
    return pdf_link