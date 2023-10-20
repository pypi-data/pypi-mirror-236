## 简介

AppleSearchAdsSDK是一个用于与Apple Search Ads Campaign Management API进行交互的软件开发工具包（SDK）。它提供了一组功能丰富的工具和方法，用于简化与Apple Search Ads广告系列进行交互的过程。
以下是 Apple Search Ads SDK 的主要功能和用途：
* 广告活动管理: 开发者可以使用 SDK 创建、修改和管理其 Apple Search Ads 广告活动。这包括创建新广告系列、设定广告组和关键字的出价等。
* 拉取广告报告数据: SDK 可以帮助开发者生成广告活动报告，以便进行数据分析和决策制定。这些报告可以用于了解广告活动的整体表现和趋势，以及评估广告投资的回报。

## 特性
- Oauth2 授权Token管理
- 封装API功能，简化API交互
- 持续更新，及时根据Apple Search Ads Campaign Management API 新特性

## API文档

[Apple Search Ads Campaign Management API文档地址](https://developer.apple.com/documentation/apple_search_ads)

## 准备

- [Python3.9+](https://www.python.org/) 和 [git](https://git-scm.com/) -项目开发环境


## 安装

- 获取项目代码

```bash
git clone git@github.com:wangjiabiao/AppleSearchAdsSDK.git
```

- 安装

```bash
pip install AppleSearchAdsSDK
```
## 使用
### 完成OAuth 2身份验证
* 1、在Apple Search Ads 广告系列管理 API V4版本中，使用OAuth 2进行身份验证。 
  在正式开始前请先阅读：[Implementing OAuth for the Apple Search Ads API](https://developer.apple.com/documentation/apple_search_ads/implementing_oauth_for_the_apple_search_ads_api) .
  在本项目中auth.py模块帮助实现了以下功能：
    - 生成私钥
      ``` python
       auth.create_private_key(private_key_out)
       ```
    - 提取公钥
      ``` python
       auth.create_public_key(private_key,public_key_out)
       ```
    - 创建客户端密码
       ``` python
       auth.create_client_secret(private_key_path, client_secret_out)
       ```
    - 获取access_token
        ``` python
       auth.get_access_token(client_secret)
       ```
### 使用 sdk 管理 Apple Search Ads
AppleSearchAdsSDK类用于与苹果的Search Ads API进行交互.
先来看一个例子：
```python
from AppleSearchAdsSDK.sdk import AppleSearchAdsSDK #导入 AppleSearchAdsSDK 类
#access_token 字典包含了访问令牌的相关信息，可以通过本SDK auth.get_access_token方法获取。由于access_token有效期为1个小时，建议统一管理您的access_token。
access_token = {'access_token': '****', 'token_type': 'Bearer', 'expires_in': 3600} 
sdk = AppleSearchAdsSDK(access_token, org_id=123456)  # org_id为账户的organization id
#构建一个 payload 字典，其中包含了要发送的信息，包括 API 类型 (api_type) 和 API 名称 (api_name) API请求参数（data）
payload = {
    "api_type": "Campaign",
    "api_name": "find_campaigns",
    "data": {
        "pagination": {"offset": 0, "limit": 5000},
        "orderBy": [{"field": "id", "sortOrder": "ASCENDING"}],
        "conditions": [
            {"field": "deleted", "operator": "IN", "values": [True, False]},
        ]
    }
}
response = sdk.send(payload) #使用 sdk.send(payload) 方法发送 API 请求，返回的response是一个requests.models.Response 对象
print(response.status_code)
print(response.json())
```
在这个例子中 payload 包含了Search Ads API 的 API 类型：api_type；API 名称：api_name； 请求参数： data；
其中api_type 是此SDK api包中各个模块中类的名称，如：campaign.py模块 Campaign类；
api_name是api包中各个模块中类的方法，如：campaign.py模块 Campaign类的find_campaigns方法。
* payload 说明

|  字段   | 类型  | 说明 |
|  ----  | ----  | ----  |
| api_type  | str | api包中各个模块中类的名称，如：campaign.py模块 Campaign类 |
| api_name  | str | api包中各个模块中类的方法，如：campaign.py模块 Campaign类的find_campaigns方法 |
| path_params  | dict | uri中要求的参数 如：https://developer.apple.com/documentation/apple_search_ads/get_an_ad_group API 中 GET https://api.searchads.apple.com/api/v4/campaigns/{campaignId}/adgroups/{adgroupId} 中的 {campaignId} 和 {adgroupId} 可以定义为:{'campaign_id': 123456, 'adgroup_id': 123456}|
| query_params  | dict | uri中可以添加的参数，返回指定字段 如：https://developer.apple.com/documentation/apple_search_ads/get_an_ad_group 指定返回id,name 可以将query_params定义为{'fields': "id,name"}，最终API为:https://api.searchads.apple.com/api/v4/campaigns/{campaignId}/adgroups/{adgroupId}?fields=id,name |
| data  | dict | data的格式可以参考苹果官方API。 |

```python
from AppleSearchAdsSDK.api import ApiBase
class Campaign(ApiBase):

    def create_a_campaign(self):
        """
        Creates a campaign to promote an app.
        https://developer.apple.com/documentation/apple_search_ads/create_a_campaign
        :return:
        """
        return self.sdk.make_request("POST", "campaigns")

    def find_campaigns(self):
        """
        Fetches campaigns with selector operators.
        https://developer.apple.com/documentation/apple_search_ads/find_campaigns
        :return:
        """
        query_params = self.payload.get("query_params")
        return self.sdk.make_request("POST", "campaigns/find", params=query_params)
```


## 维护者
[@wangjiabiao](https://github.com/wangjiabiao)

