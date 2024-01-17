#pip install transformers
#pip install scrapy
#pip install scrapeops-scrapy
#pip install scrapy-user-agents

import scrapy
from scrapy.crawler import CrawlerProcess
# import openpyxl
# from transformers import pipeline

class Prodcrawler3Spider(scrapy.Spider):
    name = "prodcrawler3"
    allowed_domains = ["www.amazon.com","www.amazon.in"]
    # start_urls = [r"https://www.amazon.in/dp/B09WQYFLRX/ref=s9_acsd_al_bw_c2_x_2_t?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-2&pf_rd_r=V90K4GX2KV2CRK1H0TMM&pf_rd_t=101&pf_rd_p=dd55f421-4048-4cb6-98e4-c55c8eb200cb&pf_rd_i=68424881031"]
    user_url = input("\n\nPlease paste the url of your amazon product\n\n")
    start_urls = [fr'{user_url}']
    custom_settings = {
    'EXTENSIONS': {
        'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500
    },
    'ROBOTSTXT_OBEY' : False,
    'SCRAPEOPS_API_KEY' : 'YOUR KEY HERE',
    'DOWNLOADER_MIDDLEWARES' : {
        'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    },
    # 'CONCURRENT_REQUESTS': 1,
    # 'AUTOTHROTTLE_ENABLED': True,
    # 'AUTOTHROTTLE_START_DELAY': 5,
    }

    def parse(self, response):
        global prod_info_list
        prod_info_list = []
        # prod_title = response.css('#productTitle::text').get().strip()
        # print(f"\n\nProduct Title: {prod_title}")

        fp = open('bot_input', 'w')
        fp.close()

        desc_list = response.css('#feature-bullets ul li span::text')
        prod_desc_list = []
        for i in desc_list:
            desc_bullet = i.get()
            prod_desc_list.append(desc_bullet)
        prod_desc_str = ''
        prod_desc_str = prod_desc_str.join(prod_desc_list)
        print(f"\n\nProduct Description:\n{prod_desc_str}")

        # prod_rating = response.css('#acrPopover span a span::text').get().strip()
        # print(f"\n\nProduct Rating: {prod_rating}\n\n")

        # top_reviews = str(response.selector.xpath('//*[@id="cm-cr-dp-review-list"]').css('div div div div span div div span::text').extract())
        # print(f"\n\nReviews: {top_reviews}\n\n")

        top_review = str(response.css('div.a-row.a-spacing-small.review-data')[0].css('span div div span::text').extract())
        print(f"\n\nTop review:\n{top_review}")
        
        summarizer_input = prod_desc_str + top_review 

        # summarizer = pipeline("summarization")
        # desc = prod_desc_str
        # sum_prod_desc = summarizer(desc, max_length=130, min_length=30, do_sample=False)
        # prod_info_list.extend([prod_title,prod_desc_str,  sum_prod_desc, prod_rating])

        # prod_info_list.extend([prod_title,prod_desc_str,prod_rating,top_reviews])
        # prod_info_list.extend([prod_title,prod_desc_str,prod_rating,top_review, summarizer_input])


        with open('bot_input', 'w') as f:
            f.write(summarizer_input)

        # prod_info_tuple = tuple(prod_info_list)
        # wb = openpyxl.load_workbook('scraped_prods.xlsx')
        # ws = wb.active
        # ws.append(prod_info_tuple)
        # wb.save('scraped_prods.xlsx')

        # prod_info_list.clear()
        # prod_info_tuple = ()

        print("DONE")

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    }
)        

process.crawl(Prodcrawler3Spider)
process.start()

def qna():
    from transformers import TFAutoModelForQuestionAnswering, AutoTokenizer, pipeline

    model_name = "deepset/electra-base-squad2"

    model = TFAutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    with open('bot_input') as f:
        context = str(f.readlines())

    # print(type(context))

    # Getting predictions
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

    #Enter Question here:
    ques = input('How can I help you?:)\n')

    QA_input = {
        'question': ques,
        'context': context
    }

    res = nlp(QA_input)
    print(f"Question: {ques}")
    print(f"Answer: {res['answer']}")
# res


qna() 
