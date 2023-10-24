def extract_meta_data(response):
    authors = response.css('.linked-name::text').getall()
    authors_string = ', '.join(authors)

    abstract_texts = response.css('section.abstract p::text').getall()
    full_abstract = ' '.join(abstract_texts).strip()

    keywords = response.css('.kwd-group .kwd-part::text').getall()
    formatted_keywords = ', '.join(keywords).strip()

    meta_data = {
        'title': response.xpath('//*[@name="citation_title"]/@content').get(),
        'date': response.xpath('//*[@name="citation_publication_date"]/@content').get(),
        'mf_doi': response.xpath('//*[@name="citation_doi"]/@content').get(),
        'author': authors_string,
        'mf_journal': response.xpath('//*[@name="citation_journal_title"]/@content').get(),
        'volume_info': response.xpath('//*[@name="citation_volume"]/@content').get(),
        'issue_info': response.xpath('//*[@name="citation_issue"]/@content').get(),
        'mf_issn': response.xpath('//*[@name="citation_issn"]/@content').get(),
        'mf_publisher': response.xpath('//*[@name="citation_publisher"]/@content').get(),
        'abstract': full_abstract,
        'keywords': formatted_keywords,
        'mf_url': response.url

    }
    return meta_data
def extract_pdf_link(response):
    pdf_link = response.xpath('//a[contains(@href, "article-pdf")]/@href').get()
    return pdf_link