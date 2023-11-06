from random import randint
import re

def try_to_extract_xpath(response, response_xpath):
    result = ""
    try:
        result_raw = response.xpath(response_xpath).getall()
        result = '; '.join(result_raw)
    except:
        print("error xpath: ", response_xpath)
    return result

def extract_meta_data(response):
    string_volume = response.xpath('//*[@class="article__tocHeading"]').get() or ""
    regexp_volume = r'Vol. (\d+),'
    volume = re.search(regexp_volume, string_volume)

    authors_string = try_to_extract_xpath(response, '//*[@name="dc.Creator"]/@content')

    meta_data = {
        '202': response.xpath('//*[@name="dc.Title"]/@content').get() or None,
        '203': response.xpath('//*[@name="dc.Date"]/@content').get() or "",
        '233': response.xpath('//*[@name="dc.Identifier"]/@content').get() or "",
        '200': authors_string,
        '232': response.xpath('//*[@name="citation_journal_title"]/@content').get() or "",
        '176': volume or "",
        '235': response.xpath('//*[@name="dc.Publisher"]/@content').get() or "",
        '81': response.xpath('//*[@class="abstractSection abstractInFull"]/p').get() or response.xpath('//*[@class="abstractSection"]/p').get() or "",
        '201': response.xpath('//*[@name="keywords"]/@content').get() or "",
        '217': response.url,
        '239': response.xpath('//*[@name="dc.Type"]/@content').get() or "", #doctype
    }
    return meta_data
def extract_pdf_link(response):
    pdf_link = response.xpath('//*[@name="coolBar__ctrl coolBar__ctrl--pdf-epub-link"]/@href').get()
    if pdf_link:
        pdf_link = pdf_link.replace('epdf', 'pdf') + "?download=true"
    return pdf_link