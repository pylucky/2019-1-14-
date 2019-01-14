
"""
难题
从首页 get方式没问题，
直接看AJAX数据 POST提交方式
总提示({"status":false,"msg":"您操作太频繁,请稍后再访问","clientIp":"106.121.72.102","state":2402})

"""

import requests
from lxml import etree
import  re
import time

from mysqlhelper import  MysqlHelper

##首页》列表页
def getpage(queue):
    try:
        url="https://www.lagou.com/"

        headers={
        'Cookie': '_ga=GA1.2.1074690271.1547378664; LGUID=20190113192423-c7104e93-1725-11e9-ad39-525400f775ce; user_trace_token=20190113192423-9221e81cfccb4727b51f484d217cf4b8; _gid=GA1.2.1720614924.1547378664; index_location_city=%E5%8C%97%E4%BA%AC; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221684a4dbbd937-0dc7a458921612-b781636-1049088-1684a4dbbda5f2%22%2C%22%24device_id%22%3A%221684a4dbbd937-0dc7a458921612-b781636-1049088-1684a4dbbda5f2%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=bc09fcf82697afb620b4a7e9fb559d4cc2e146afa7109f37375acf744f94da67; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=427; JSESSIONID=ABAAABAAAGFABEF0DF4BBF115D77C8F84F5A959888E3EC4; _putrc=EBAE0462AA6AE5FE123F89F2B170EADC; login=true; unick=%E5%BE%90%E9%9B%AA%E4%B8%9C; X_MIDDLE_TOKEN=62a3a8f75ec8b1d8fd6fee884c6d263f; PRE_UTM=; gate_login_token=20b7cf69a65412647c9bd033863575a6b6778352bc29e9030c10b9cc97334338; _gat=1; TG-TRACK-CODE=index_navigation; SEARCH_ID=023d711407c94954bf63a791d44556d7; LGSID=20190114153350-bc4432b6-17ce-11e9-af12-525400f775ce; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0NALcLttamj7gw7OeZf0Mc5064WotJAakhEp81FVYfG%26wd%3D%26eqid%3Dd3cc9b4400003344000000035c3c3b59; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20190114153350-bc44340e-17ce-11e9-af12-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1547378663,1547433175,1547440196,1547451230; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1547451230',
        'Host': 'www.lagou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }


        response=requests.get(url,headers=headers)

        # with open('index.html','wb')as f:
        #     f.write(response.content)

        ##技术

        hmtl_ele=etree.HTML(response.text)

        jishu=hmtl_ele.xpath('//div[@class="mainNavs"]/div[1]/div[2]//text()')
        # 获取所有的分类
        for i in jishu:
            i=i.strip('\n').strip()
            # print(i)
        # 获取所有的href

        href=hmtl_ele.xpath('//div[@class="mainNavs"]/div[1]/div[2]//@href')

        for h in  href:
            ##获取页面最大页面数
            response=requests.get(h)
            html_res=etree.HTML(response.text)
            if html_res!="":
                max_num = html_res.xpath('//div[@class="pager_container"]/a/@href')[-2]
                max_page=re.findall(r".*/(\d+)/",max_num)
                if max_page!=[]:
                    result=int("".join(max_page))

                    for num in range(1,result+1):
                        ### 拼接所有下一页
                        list_url=h+str(num)+'/?filterOption='+str(result)


                        ##获取所有的详细页url
                        response=requests.get(list_url)
                        html_ele=etree.HTML(response.text)
                        next_href=html_ele.xpath('//ul[@class="item_con_list"]/li//@href')

                        queue.put(next_href)


    except Exception as e:
        print(e)

## return详情页所有的url

def getInfopage(next_href):
    try:
        for i in next_href:
            list_url=i
            # print(list_url)
            headers={
            'Cookie': '_ga=GA1.2.1074690271.1547378664; LGUID=20190113192423-c7104e93-1725-11e9-ad39-525400f775ce; user_trace_token=20190113192423-9221e81cfccb4727b51f484d217cf4b8; _gid=GA1.2.1720614924.1547378664; index_location_city=%E5%8C%97%E4%BA%AC; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221684a4dbbd937-0dc7a458921612-b781636-1049088-1684a4dbbda5f2%22%2C%22%24device_id%22%3A%221684a4dbbd937-0dc7a458921612-b781636-1049088-1684a4dbbda5f2%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=bc09fcf82697afb620b4a7e9fb559d4cc2e146afa7109f37375acf744f94da67; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=427; JSESSIONID=ABAAABAAAGFABEF0DF4BBF115D77C8F84F5A959888E3EC4; _putrc=EBAE0462AA6AE5FE123F89F2B170EADC; login=true; unick=%E5%BE%90%E9%9B%AA%E4%B8%9C; X_MIDDLE_TOKEN=62a3a8f75ec8b1d8fd6fee884c6d263f; gate_login_token=20b7cf69a65412647c9bd033863575a6b6778352bc29e9030c10b9cc97334338; LGSID=20190114153350-bc4432b6-17ce-11e9-af12-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1547378663,1547433175,1547440196,1547451230; TG-TRACK-CODE=index_navigation; SEARCH_ID=9659609750684ea2aa8fbea99afde64b; _gat=1; LGRID=20190114163223-ea6e8a8f-17d6-11e9-b64c-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1547454744',
            'Host': 'www.lagou.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            }
            response=requests.get(list_url,headers=headers)
            # print(response.text)
            ##详情页所有信息

            time.sleep(0.2)
            ##### 公司详情
            hmtl_ele=etree.HTML(response.text)
            ##公司名称
            time.sleep(0.2)
            name_gs=hmtl_ele.xpath('//h2[@class="fl"]//text()')
            name_gs="".join(name_gs).replace("拉勾认证企业","").replace("拉勾未认证企业","").strip("\n").strip()
            # print(name_gs)
            ##公司地址
            time.sleep(0.1)
            location_gs=hmtl_ele.xpath('//div[@class="work_addr"]/text()')
            location_gs = "".join(location_gs).strip("\n").strip()
            # print(location_gs)
            ##公司行业
            time.sleep(0.1)
            type_gs=hmtl_ele.xpath('//ul[@class="c_feature"]/li[1]/text()')
            type_gs = "".join(type_gs).strip("\n").strip()
            ##公司人数

            num_gs=hmtl_ele.xpath('//ul[@class="c_feature"]/li[3]/text()')
            num_gs = "".join( num_gs).strip("\n").strip()
            print(num_gs)
            ##公司网站
            url_gs=hmtl_ele.xpath('//ul[@class="c_feature"]/li[4]/@href')

            ### 招聘详情
            ##招聘标题
            title=hmtl_ele.xpath('//div[@class="job-name"]/span/text()')
            title="".join(title).strip()
            ##招聘薪资
            salary=hmtl_ele.xpath('//span[@class="salary"]/text()')
            salary="".join(salary).strip()
            ##招聘经验
            time.sleep(0.2)
            jinyan=hmtl_ele.xpath('//dd[@class="job_request"]/p/span[3]/text()')
            jinyan="".join(jinyan).strip('/').strip()
            ##招聘学历
            xueli=hmtl_ele.xpath('//dd[@class="job_request"]/p/span[4]/text()')
            ##招聘时间
            time.sleep(0.3)
            times=hmtl_ele.xpath('//p[@class="publish_time"]/text()')
            new_time=[]
            for t in times:
                if not t.startswith("2019") and  t!=[]:
                    t=t.replace("发布于拉勾网","")
                    localtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                    day_time=str(localtime)+"---"+t
                    # print(day_time)
                    new_time.append(day_time)
                else:
                    t=t.replace("发布于拉勾网","")
                    new_time.append(t)
            for s in new_time:
                if s!=[]:
                    zhao_time=s

                    time.sleep(0.3)
                    ##岗位要求详情
                    content=hmtl_ele.xpath('//div[@class="job-detail"]/p//text()')
                    content="".join(content).strip()

                    uid="拉勾网"
                    ##存储
                    s1 = name_gs
                    s2 = location_gs
                    s3 = type_gs
                    s4 =num_gs
                    s5 = title
                    s6 = salary
                    s7 = jinyan
                    s8 = xueli
                    s9 = zhao_time
                    s10 = content
                    s11 = uid

                    # # # ##mysql存贮
                    #
                    # sql = 'insert into lagou(name_gs,location_gs,type_gs,num_gs,title,salary,jinyan,xueli,zhao_time,content,uid)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    # data = (s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11)
                    # myhelper = MysqlHelper()
                    # myhelper.execute_modify_sql(sql, data)
                    #
                    # print('Mysql连接成功')

    except Exception as e:
        print(e)




if __name__ =="__main__":
    import multiprocessing

    # 创建一个消息队列 用于存放列表页url
    queue = multiprocessing.Queue()

    print('消息队列创建成功')
    # 创建一个进程获取所有的的url
    p = multiprocessing.Process(target=getpage, args=(queue,))
    # 进程的开启
    p.start()
    print('进程开启了' * 10)
    # 创建下载图片的进程池 指定同时开启5个进程  进程池中的进程只有5个进程是循环利用的
    pool = multiprocessing.Pool(30)
    print('进程池创建成功')
    while True:
        # 从消息队列中获取url  如果获得了就执行  获取不到会处于阻塞状态
        manages_url = queue.get()
        # 打印获取到的信息
        print(manages_url, '==' * 50)
        pool.apply_async(getInfopage,(manages_url,))
    # 进程池的关闭
    pool.close()
    # 进程池的等待
    pool.join()
    # 所有执行完毕之后
    p.join()

    print('结束'*10)










