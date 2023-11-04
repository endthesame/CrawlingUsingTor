from random import randint

def try_to_extract_xpath(response, response_xpath):
    result = ""
    try:
        result_raw = response.xpath(response_xpath).getall()
        result = '; '.join(result_raw)
    except:
        print("error xpath: ", response_xpath)
    return result

def extract_meta_data(response):

    authors_string = try_to_extract_xpath(response, '//*[@name="citation_author"]/@content')
    formatted_keywords = try_to_extract_xpath(response, '//*[@name="citation_keyword"]/@content')
    formatted_affilations = try_to_extract_xpath(response, '//*[@name="citation_author_institution"]/@content')

    meta_data = {
        '202': response.xpath('//*[@name="citation_title"]/@content').get() or response.xpath('//title/text()').get() or None,
        '203': response.xpath('//*[@name="citation_publication_date"]/@content').get() or "",
        '233': response.xpath('//*[@name="citation_doi"]/@content').get() or "",
        '200': authors_string,
        '232': response.xpath('//*[@name="citation_journal_title"]/@content').get() or "",
        '176': response.xpath('//*[@name="citation_volume"]/@content').get() or "",
        '208': response.xpath('//*[@name="citation_issue"]/@content').get() or "",
        '184': response.xpath('//*[@name="prism.issn"]/@content').get() or "",
        '185': response.xpath('//*[@name="prism.eIssn"]/@content').get() or "",
        '235': response.xpath('//*[@name="citation_publisher"]/@content').get() or "",
        '81': response.xpath('//*[@align="LEFT"]/text()').get() or response.xpath('//*[@name="citation_abstract"]/@content').get() or "",
        '201': formatted_keywords,
        '217': response.url,
        '197': response.xpath('//*[@name="prism.startingPage"]/@content').get() or "",
        '198': response.xpath('//*[@name="prism.endingPage"]/@content').get() or "",
        '205': response.xpath('//*[@name="citation_language"]/@content').get() or "",
        '144': formatted_affilations,

    }
    return meta_data
def extract_pdf_link(response):
    pdf_link = response.xpath('//*[@name="citation_pdf_url"]/@content').get()
    if not pdf_link:
        pdf_link = response.xpath('//div[@class="article_doc"]/ul/li[2]/a/@href').get()
    return pdf_link