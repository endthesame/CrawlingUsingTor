def extract_meta_data(response):
    authors = response.xpath('//*[@name="citation_author"]/@content').getall()
    authors_string = '; '.join(authors)

    keywords = response.xpath('//*[@name="citation_keyword"]/@content').getall()
    formatted_keywords = '; '.join(keywords).strip()

    affiliations = response.xpath('//*[@name="citation_author_institution"]/@content').getall()
    formatted_affilations = '; '.join(affiliations).strip()

    meta_data = {
        'title': response.xpath('//*[@name="citation_title"]/@content').get(),
        'date': response.xpath('//*[@name="citation_publication_date"]/@content').get(),
        'mf_doi': response.xpath('//*[@name="citation_doi"]/@content').get(),
        'author': authors_string,
        'mf_journal': response.xpath('//*[@name="citation_journal_title"]/@content').get(),
        'volume_info': response.xpath('//*[@name="citation_volume"]/@content').get(),
        'issue_info': response.xpath('//*[@name="citation_issue"]/@content').get(),
        'mf_issn': response.xpath('//*[@name="prism.issn"]/@content').get(),
        'mf_eissn': response.xpath('//*[@name="prism.eIssn"]/@content').get(),
        'mf_publisher': response.xpath('//*[@name="citation_publisher"]/@content').get(),
        'abstract': response.xpath('//*[@align="LEFT"]/text()').get(),
        'keywords': formatted_keywords,
        'mf_url': response.url,
        'first_page': response.xpath('//*[@name="prism.startingPage"]/@content').get(),
        'last_page': response.xpath('//*[@name="prism.endingPage"]/@content').get(),
        'content-language': response.xpath('//*[@name="citation_language"]/@content').get(),
        'affiliation': formatted_affilations,

    }
    return meta_data
def extract_pdf_link(response):
    pdf_link = response.xpath('//*[@name="citation_pdf_url"]/@content').get()
    return pdf_link