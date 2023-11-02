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
        'title': response.xpath('//*[@name="citation_title"]/@content').get() or response.xpath('//title/text()').get() or None,
        'date': response.xpath('//*[@name="citation_publication_date"]/@content').get() or "",
        'mf_doi': response.xpath('//*[@name="citation_doi"]/@content').get() or "",
        'author': authors_string,
        'mf_journal': response.xpath('//*[@name="citation_journal_title"]/@content').get() or "",
        'volume_info': response.xpath('//*[@name="citation_volume"]/@content').get() or "",
        'issue_info': response.xpath('//*[@name="citation_issue"]/@content').get() or "",
        'mf_issn': response.xpath('//*[@name="prism.issn"]/@content').get() or "",
        'mf_eissn': response.xpath('//*[@name="prism.eIssn"]/@content').get() or "",
        'mf_publisher': response.xpath('//*[@name="citation_publisher"]/@content').get() or "",
        'abstract': response.xpath('//*[@align="LEFT"]/text()').get() or response.xpath('//*[@name="citation_abstract"]/@content').get() or "",
        'keywords': formatted_keywords,
        'mf_url': response.url,
        'first_page': response.xpath('//*[@name="prism.startingPage"]/@content').get() or "",
        'last_page': response.xpath('//*[@name="prism.endingPage"]/@content').get() or "",
        'content-language': response.xpath('//*[@name="citation_language"]/@content').get() or "",
        'affiliation': formatted_affilations,

    }
    return meta_data
def extract_pdf_link(response):
    pdf_link = response.xpath('//*[@name="citation_pdf_url"]/@content').get()
    if not pdf_link:
        pdf_link = response.xpath('//div[@class="article_doc"]/ul/li[2]/a/@href').get()
    return pdf_link