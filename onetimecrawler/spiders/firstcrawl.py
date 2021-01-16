import scrapy


class FirstcrawlSpider(scrapy.Spider):
    name = 'firstcrawl'
    allowed_domains = ['85tube.net']
    start_urls = ['https://85tube.net/latest-updates/%s/' % page for page in range(100)]

    def parse(self, response):
        wrapper = response.xpath('//div[@id="list_videos_latest_videos_list"]')
        for wrapperindex in wrapper:
            videos = wrapperindex.xpath('//div[@class="item  "]')
            for video in videos:
                videospage = wrapperindex.xpath('.//div[@class="pagination-holder"]//li[@class="page-current"]/span/text()').get()
                link = video.xpath('.//a/@href').get()
                yield response.follow(url=link, callback=self.parse_video, cb_kwargs=dict(current_page=videospage))
          
                        
    def parse_video(self, response, current_page):        
        video_id = response.xpath('//div[@class="button-group"]/input[2]/@value').get()
        txt = 'https://85tube.net/embed/{}/'
        
        yield {
            'VideoID': response.xpath('//div[@class="button-group"]/input[2]/@value').get(),
            'ChineseName': response.xpath('//h1/text()').get(),
            'Duration': response.xpath('//span[contains(text(),"時間: ")][1]/em/text()').get(),
            'Tags': response.xpath('//div[contains(text(),"標簽:") or contains(text(),"分類:")]/a/text()').getall(),
            'ImgURL': response.xpath('//div[@class="block-screenshots"]/a[1]/@href').get(),
            'EmbedURL': txt.format(video_id),
            'videoPage': current_page
            }
