import scrapy
import re

class EtherscanSpider(scrapy.Spider):
    name = "etherscan"

    def start_requests(self):
        urls = []
        for i in range(43,85):
            urls.append ('https://etherscan.io/blocks_forked?ps=100&p=%s' % i )

        #urls = [
        #    'https://etherscan.io/blocks_forked?ps=100&p=32',
        #]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        blocks  =  response.xpath('//a[contains(@href, "/block/")]/@href').getall()
        
        filename = 'reorgedblocks.log'
        with open(filename, 'a') as f:
            for block in blocks:
                f.write(block[7:-2])
                f.write('\n')
        
        self.log('Saved file %s' % filename)


        # our last  7680081    (44 ok  769..)    our first   7479620    do 83

      
