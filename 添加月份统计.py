#!/usr/bin/env python
# coding: utf-8

# In[228]:


import json
import matplotlib.pyplot as plt
import requests
import platform
from datetime import datetime
import pandas as pd
import numpy
import warnings
warnings.filterwarnings('ignore')

# 传入cookie所需参数
account = ""
hallticket = ""
ASP_NET_SessionId = ""
all_data = dict()
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'JWTUser=%7B%22account%22%3A%222100013357%22%2C%22id%22%3A539511%2C%22tenant_id%22%3A1%7D; login_cmc_id=c3f94d04680602391c8f51533f0de9b6; login_cmc_tid=f6dead83f9a639f4adf9ab3d674f0709; group_code=1350000018; login_cmc_url=https%3A%2F%2Fyjloginse.pku.edu.cn%2Flogin1350000018.html; login_cmc_type=2; cmc_version=v3; _token=767fb816ede9e69f6a6348ac5fd0c26fa2933048a87b51f185704fc5accd57dea%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22_token%22%3Bi%3A1%3Bs%3A733%3A%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50IjoiMjEwMDAxMzM1NyIsImNtY0dyb3VwQ29kZSI6IjEzNTAwMDAwMTgiLCJjbWNHcm91cElkIjoiZDQzOGNhZmI0YzM0YjNiNDliM2E1MjNiYmVmNTAyMDMiLCJleHAiOjE3MzQ5NzAwODEsImxvZ2luVHlwZSI6ImRlZmF1bHQiLCJtcm9sZXMiOlt7ImNtY19yb2xlIjoiMTViZDI2NzE1NDc4YjE5ZDAxYjkzYjk3ODNkZmVlNmQiLCJjb2RlIjoic3R1ZGVudCIsImNyZWF0ZWRfYXQiOiIyMDIyLTAxLTE0IDE1OjI3OjQzIiwiZGVzY3JpcHRpb24iOiLlrabnlJ_mi6XmnInigJzmoJblrabigJ3mmbrmhafkupLliqjlnKjnur_mlZnlrablubPlj7DliY3lj7DlrabkuaDor77nqIvlkozkuIrkvKDkvZzlk4Hmn6XnnIvmiJDnu6nnrqHnkIbkuKrkurrotYTmupDmnYPpmZAiLCJkaXNwbGF5X25hbWUiOiLlrabnlJ8iLCJpZCI6NDgyLCJpc2RlZmF1bHQiOiIxIn1dLCJyZWFsbmFtZSI6IuiRo-S4gOadrSIsInN1YiI6NTM5NTExLCJ0ZW5hbnRfaWQiOjF9.bpXwiHAe1nRNjwxwXg6t38_6cLQMNSuNKri2leWotUg%22%3B%7D; ASP.NET_SessionId=dapala3hruunqk5hzebmymse; hallticket=A1FA34EE568D427FB507C057D0FD0950',
    'Origin': 'https://card.pku.edu.cn',
    'Referer': 'https://card.pku.edu.cn/Page/Page',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


# In[ ]:


if __name__ == "__main__":
    # 读入账户信息
    try:
        with open("config.json", "r", encoding='utf-8') as f:
            config = json.load(f)
            account = config["account"]
            hallticket = config["hallticket"]
            ASP_NET_SessionId = config['ASP.NET_SessionId']
        
    except Exception as e:
        print("账户信息读取失败，请重新输入")
        account = input("请输入account: ")
        hallticket = input("请输入hallticket: ")
        ASP_NET_SessionId = input("请输入ASP.NET_SessionId: ")
        with open("config.json", "w", encoding='utf-8') as f:
            json.dump({"account": account, "hallticket": hallticket,'ASP.NET_SessionId': ASP_NET_SessionId}, f, indent=4)

    # 默认日期
    default_sdate = "2024-01-01"
    default_edate = "2024-12-31"

    def is_valid_date(date_str):
        """检查日期是否符合YYYY-MM-DD格式且为有效日期"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    def format_date(date_str):
        """确保日期始终以两位数显示月份和日期"""
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%Y-%m-%d")  # 格式化为YYYY-MM-DD

    
    
    ### 日期处理###
    
    # 获取用户输入的开始日期
    sdate = input("请输入开始日期(YYYY-MM-DD，默认2024-01-01): ").strip()
    if not is_valid_date(sdate):
        print(f"输入的开始日期无效，使用默认值: {default_sdate}")
        sdate = default_sdate
    else:
        sdate = format_date(sdate)

    # 获取用户输入的结束日期
    edate = input("请输入结束日期(YYYY-MM-DD，默认2024-12-31): ").strip()
    if not is_valid_date(edate):
        print(f"输入的结束日期无效，使用默认值: {default_edate}")
        edate = default_edate
    else:
        edate = format_date(edate)

    print(f"开始日期: {sdate}, 结束日期: {edate}")
    
    
    
    # 发送请求，得到加密后的字符串
    
    url = f"https://card.pku.edu.cn/Report/GetPersonTrjn"
    cookie = {
        'ASP.NET_SessionId': ASP_NET_SessionId,
        'hallticket': hallticket,
    }
    post_data = {
        "sdate": sdate,
        "edate": edate,
        "account": account,
        "page": "1",
        "rows": "9000",
    }
    test = requests.session()
    response = test.post(url, cookies=cookie, data=post_data,headers = headers)
#     response = requests.post(url, cookies=cookie, data=post_data,headers = headers)
    
    data = json.loads(response.text)["rows"]


# In[230]:


# 接收包含数据的dataframe , 用于分类的变量var ，选择是否按照消费排序sort_bool
# 输出统计图片
def draw_graph(pre_data , var, sort_bool):
    all_data = pre_data.groupby(var).agg(
            TRANAMT=('TRANAMT', 'sum'),
        ).reset_index()

    #判断是档口统计还是月份统计
    if sort_bool:
        all_data = all_data.sort_values(by='TRANAMT', ascending=True)
        description = f"今年你猛猛吃了：{len(all_data)}个档口\n总消费次数：{len(data)}\n总消费金额：￥{round(sum(all_data['TRANAMT']), 1)}"
    else:
        description = f"今年你在学校进食了：{len(all_data)}个月\n最饿月份：{all_data.loc[all_data['TRANAMT'].idxmax(), 'OCCTIME']}\n最饿月份你总共吃了：￥{all_data['TRANAMT'].max()}"
    
    #设置字体
    if platform.system() == "Darwin":
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    elif platform.system() == "Linux":
        plt.rcParams['font.family'] = ['Droid Sans Fallback', 'DejaVu Sans']
    else:
        plt.rcParams['font.sans-serif'] = ['SimHei']
    
    #绘图
    plt.figure(figsize=(12, len(all_data) / 66 * 18))
    plt.barh(all_data[var],all_data['TRANAMT'], align='center')
    for index, value in enumerate(all_data['TRANAMT']):
        plt.text(value + 0.01 * all_data['TRANAMT'].max(),
                index,
                str(value),
                va='center')

    plt.xlim(0, 1.2 * max(all_data['TRANAMT']))
    plt.title(f"白鲸大学食堂消费情况\n({post_data['sdate']} 至 {post_data['edate']})")
    plt.xlabel("消费金额（元）")
    
    #判断是档口统计还是月份统计
    plt.text(0.9, 0.1, description, ha='center', va='center', transform=plt.gca().transAxes)
        
    plt.savefig("result.png",bbox_inches='tight')
    plt.show()


# ## 这个小档口才是我永远的家）

# In[232]:


# all_data = dict()
pre_data = pd.DataFrame(data)
pre_data = pre_data[pre_data['TRANAMT']<0].reset_index(drop =True)
pre_data['TRANAMT'] = abs(pre_data['TRANAMT'])
pre_data['MERCNAME'] = pre_data['MERCNAME'].str.strip()

draw_graph(pre_data ,'MERCNAME',True)


# # 最饿的月

# In[233]:


monthdata = pre_data[['OCCTIME','MERCNAME','TRANAMT']]
monthdata['OCCTIME'] = pd.to_datetime(pre_data['OCCTIME']).dt.strftime('%Y-%m')
monthdata = monthdata.sort_values(by='OCCTIME', ascending=True)
monthdata['OCCDAYS'] = pd.to_datetime(pre_data['OCCTIME']).dt.strftime('%Y-%m-%d')
daysdata = monthdata.sort_values(by='OCCDAYS', ascending=True)
draw_graph(monthdata ,'OCCTIME',False)


# In[ ]:




