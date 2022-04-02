import requests
from bs4 import BeautifulSoup

class Administrative(object):
    def __init__(self):
        #写入文件
        self.f = open("area_info_tab_2021.txt","a",encoding="utf-8")
        self.flag = True
        self.i = 1
        self.f.write("id,code,pcode,name,flevel\n")
        while self.flag:
            try :
                self.main()
            except :
                print("出错了")

    def main(self):
        base_url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/'
        trs=self.get_response(base_url,'provincetr')
        #已完成省市区编码,出错时,可根据编码快速跳过已插入省市区
        self.f2 = open("exist.txt","r+",encoding="utf-8")
        exist = self.f2.read()
        #已插入省市区编码,出错时,可根据编码跳过已插入数据
        self.f3 = open("exist2.txt","r+",encoding="utf-8")
        exist2 = self.f3.read()
        if  exist.find("650000000000")!=-1:
            self.flag = False
            return
        for tr in trs:#循环每一行
            for td in tr:#循环每个省
                province_code = td.a.get('href')[0:2]+"0000000000"
                province_name=td.a.get_text()
                if exist.find(province_code)!=-1:
                    continue
                if exist2.find(province_code)==-1:
                    self.f.write(str(self.i)+","+province_code+","+"000000000000"+","+province_name+","+"1\n")
                self.f3.write(province_code+",")
                self.i = int(self.i) + 1
                province_url=base_url+td.a.get('href')
                print(province_url)
                trs=self.get_response(province_url,None)
                for tr in trs[1:]:#循环每个市
                    city_code=tr.find_all('td')[0].string
                    city_name=tr.find_all('td')[1].string
                    if exist.find(city_code)!=-1:
                        continue
                    if exist2.find(city_code)==-1:
                        self.f.write(str(self.i)+","+city_code+","+province_code+","+city_name+","+"2\n")
                    self.f3.write(city_code+",")
                    self.i = int(self.i) + 1
                    if tr.find_all('td')[1].a==None:
                        continue
                    href = tr.find_all('td')[1].a.get('href')
                    province_bm = href.split("/")[0]+"/"
                    city_url=base_url+href
                    print(city_url)
                    trs=self.get_response(city_url,None)
                    for tr in trs[1:]:#循环每个区
                        area_code=tr.find_all('td')[0].string
                        area_name=tr.find_all('td')[1].string
                        if exist.find(area_code)!=-1:
                            continue
                        if exist2.find(area_code)==-1:
                            self.f.write(str(self.i)+","+area_code+","+city_code+","+area_name+","+"3\n")
                        self.f3.write(area_code+",")
                        self.i = int(self.i) + 1
                        if tr.find_all('td')[1].a==None:
                            continue
                        href = tr.find_all('td')[1].a.get('href')
                        city_bm = href.split("/")[0]+"/"
                        area_url=base_url+province_bm+href
                        print(area_url)
                        trs=self.get_response(area_url,None)
                        for tr in trs[1:]:#循环每个县
                            street_code=tr.find_all('td')[0].string
                            street_name=tr.find_all('td')[1].string
                            if exist.find(street_code)!=-1:
                                continue
                            if exist2.find(street_code)==-1:
                                self.f.write(str(self.i)+","+street_code+","+area_code+","+street_name+","+"4\n")
                            self.f3.write(street_code+",")
                            self.i = int(self.i) + 1
                            if tr.find_all('td')[1].a==None:
                                continue
                            street_url=base_url+province_bm+city_bm+tr.find_all('td')[1].a.get('href')
                            print(street_url)
                            trs=self.get_response(street_url,None)
                            for tr in trs[1:]:#循环每个镇
                                community_code=tr.find_all('td')[0].string
                                community_name=tr.find_all('td')[2].string
                                if exist.find(community_code)!=-1:
                                    continue
                                if exist2.find(community_code)==-1:
                                    self.f.write(str(self.i)+","+community_code+","+street_code+","+community_name+","+"5\n")
                                self.f3.write(community_code+",")
                                self.i = int(self.i) + 1
                                data=[province_code,province_name,city_code,city_name,area_code,area_name,street_code,street_name,community_code,community_name]
                                print(data)
                                self.f2.write(community_code+",")
                            self.f2.write(street_code+",")
                        self.f2.write(area_code+",")
                    self.f2.write(city_code+",")
                self.f2.write(province_code+",")
    def get_response(self,url,attr):
        response=self.gethtml(url)
        response.encoding='utf-8'#编码转换
        soup=BeautifulSoup(response.text,'lxml')
        table=soup.find_all('tbody')[1].tbody.tbody.table
        if attr:
            trs=table.find_all('tr',attrs={'class':attr})
        else:
            trs=table.find_all('tr')
        return trs
    def gethtml(self,url):
        i = 0
        while i < 30:
            try:
                response = requests.get(url, timeout=5)
                return response
            except :
                i += 1
if __name__=='__main__':
    Administrative()
