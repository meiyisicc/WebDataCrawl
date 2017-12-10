import os
import csv
import lxml.html
from downloader import downloader
import urllib.parse
import traceback

SEED_URL = r'https://cs.lianjia.com/ershoufang/'

def write_csv_file(file_name):
    fileobj = open(file_name, 'w', newline='')
    csv_writer = csv.writer(fileobj)
    return csv_writer


def lxml_filter(html, field_lst):
    tree = lxml.html.fromstring(html)
    result = []
    for field in field_lst:
        result.append(tree.cssselect(field)[0].text_content())
    return result


def lianjia_ershoufang(html, fw):
    try:
        tree = lxml.html.fromstring(html)
        house_list = tree.cssselect('ul.sellListContent > li.clear')

        title = 'div.title > a'
        house_info = 'div.address > div.houseInfo'
        price_info = 'div.priceInfo > div.totalPrice > span'
        uinit_price = 'div.priceInfo > div.unitPrice > span'
        #result = {}

        for house in house_list:
            l1 = house.cssselect(title)[0].text_content()
            l2 = house.cssselect(house_info)[0].text_content()
            l3 = house.cssselect(price_info)[0].text_content()
            l4 = house.cssselect(uinit_price)[0].text_content()
            #result[l1] = [l2,l3]
            fw.writerow([l1,l2, l3, l4])
    except:
        print('error, continue')

    #return result



def do():
    with open('my_house_info.csv', 'w', newline='') as fileobj:
        fw = csv.writer(fileobj)
        fw.writerow(['title', 'house_info', 'price_info(wan)', 'uint_price'])
        for i in range(1, 101):
            url = SEED_URL + '/pg%s'%i
            d = Downloader()
            html = d(url)

            lianjia_ershoufang(html, fw)
            #print(p)
            #fw.
        #fw.close();

def get_plane_ticket():
    url = 'https://sjipiao.alitrip.com/flight_search_result.htm?searchBy=1277&tripType=0&depCityName=%B3%C9%B6%BC&depCity=&depDate=2017-07-03&arrCityName=%B3%A4%C9%B3&arrCity=CSX&arrDate='
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'

    d = Downloader(user_agent = head['User-Agent'])
    html = d(url)

    try:
        tree = lxml.html.fromstring(html)
        flight_list = tree.cssselect('div.flight-list-item clearfix J_FlightItem')

        title = 'span.J_line J_TestFlight'
        price_info = 'span.J_FlightListPrice'
        uinit_price = 'span.discount'
        #result = {}

        for flight in flight_list:
            l1 = flight.cssselect(title)[0].text_content()
            l3 = flight.cssselect(price_info)[0].text_content()
            l4 = flight.cssselect(uinit_price)[0].text_content()
            #result[l1] = [l2,l3]
            print(str([l1,l3,l4]))
    except:
        print(traceback.format_exc())

def get_jingdong_item():
    url = 'https://search.jd.com/search?keyword=%E7%94%B5%E8%A7%86%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%94%B5%E8%A7%86%E6%9C%BA&stock=1&ev=244_1486%40&uc=0#J_searchWrap'
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'

    d = Downloader(user_agent = head['User-Agent'])
    html = d(url)

    try:
        tree = lxml.html.fromstring(html)
        good_list = tree.cssselect('li.gl-item > div.gl-i-wrap > div.p-img > a')

        fw = write_csv_file('dianshi_jingdong_info.csv')
        for good in good_list:
            herf = good.get('href')

            goodprice = good.cssselect('i')[0].text_content() + good.cssselect('em')[0].text_content()
            print(goodprice)

            new_url = urllib.parse.urljoin(url, herf)
            good_html = d(new_url)

            try:
                good_tree = lxml.html.fromstring(good_html)

                good_brand = good_tree.cssselect('ul#parameter-brand.p-parameter-list > li > a')[0].text_content()
                good_price = good_tree.cssselect('span.p-price > span.price.J-p-4609652')[0].text_content() + good_tree.cssselect('span.p-price > span')[0].text_content()
                pingjiacishu = good_tree.cssselect('div#comment-count.comment-count.item.fl > a')[0].text_content()
                goumailv = good_tree.cssselect('div#buy-rate.buy-rate.item.fl.hide > a')[0].text_content()

                para_list = good_tree.cssselect('div.p-parameter > ul.parameter2.p-parameter-list > li')
                fenbianlv = para_list[5].get('title')
                biaoqian = para_list[6].get('title')
                nengxiao = para_list[7].get('title')
                chicun = para_list[8].get('title')

                fw.writerow([good_brand, good_price, pingjiacishu, goumailv, fenbianlv, biaoqian, nengxiao, chicun])

                print(good_brand)
            except:
                print(traceback.format_exc())

            """l1 = flight.cssselect(title)[0].text_content()
            l3 = flight.cssselect(price_info)[0].text_content()
            l4 = flight.cssselect(uinit_price)[0].text_content()
            #result[l1] = [l2,l3]
            print(str([l1,l3,l4]))"""
    except:
        print(traceback.format_exc())



if __name__ == '__main__':
    get_jingdong_item()
