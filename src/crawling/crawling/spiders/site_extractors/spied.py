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
    formatted_keywords = try_to_extract_xpath(response, '//*[@name="keywords"]/@content')
    formatted_affilations = try_to_extract_xpath(response, '//*[@name="citation_author_institution"]/@content')

    meta_data = {
        '202': response.xpath('//*[@name="citation_title"]/@content').get() or response.xpath('//title/text()').get() or None, #TITLE
        '203': response.xpath('//*[@name="citation_publication_date"]/@content').get() or "", #DATE
        '233': response.xpath('//*[@name="citation_doi"]/@content').get() or "", #DOI
        '200': authors_string, #AUTHORS
        '232': response.xpath('//*[@name="citation_journal_title"]/@content').get() or "", #JOURNAL TITLE
        '176': response.xpath('//*[@name="citation_volume"]/@content').get() or "", #VOLUME
        '208': response.xpath('//*[@name="citation_issue"]/@content').get() or "", #ISSUE
        '184': response.xpath('//*[@name="citation_issn"][1]/@content').get() or "", #ISSN
        '185': response.xpath('//*[@name="citation_issn"][2]/@content').get() or "", #EISSN
        '235': response.xpath('//*[@name="citation_publisher"]/@content').get() or "", #PUBLISHER
        '81': response.xpath('//*[@class="ArticleContentText"]/p/text()').get() or response.xpath('//*[@name="description"]/@content').get() or "", #ABSTRACT
        '201': formatted_keywords, #KEYWORDS
        '217': response.url, #MF_URL
        '197': response.xpath('//*[@name="citation_firstpage"]/@content').get() or "", #FIRST PAGE
        #'198': response.xpath('//*[@name="prism.endingPage"]/@content').get() or "", #LAST PAGE
        '205': response.xpath('//*[@name="citation_language"]/@content').get() or "", #LANGUAGE
        '144': formatted_affilations, #AFFILATION
        '239': response.xpath('//*[@name="citation_article_type"]/@content').get() or "", #DOC TYPE

    }
    return meta_data
def extract_pdf_link(response):
    pdf_link = response.xpath('//*[@name="citation_pdf_url"]/@content').get()
    # if not pdf_link:
    #     pdf_link = response.xpath('//*[@class="ui-button  DownloadSaveButton1 DownloadSaveButtonText"]/@href').get()
    return pdf_link