# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : sdk.py
# Time       ：2023/7/26 17:24
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
import json

import requests
from retrying import retry

from AppleSearchAdsSDK.api.ad_group import AdGroup
from AppleSearchAdsSDK.api.ad_group_negative_keywords import AdGroupNegativeKeywords
from AppleSearchAdsSDK.api.ad_rejection_reasons import AdRejectionReasons
from AppleSearchAdsSDK.api.ads import Ads
from AppleSearchAdsSDK.api.budget_order import BudgetOrder
from AppleSearchAdsSDK.api.campaign import Campaign
from AppleSearchAdsSDK.api.campaign_negative_keywords import CampaignNegativeKeywords
from AppleSearchAdsSDK.api.creatives import Creatives
from AppleSearchAdsSDK.api.custom_product_pages import CustomProductPages
from AppleSearchAdsSDK.api.impression_share_reports import ImpressionShareReports
from AppleSearchAdsSDK.api.reports import Reports
from AppleSearchAdsSDK.api.search_app import SearchApps
from AppleSearchAdsSDK.api.search_geolocations import SearchGeolocations
from AppleSearchAdsSDK.api.targeting_keywords import TargetingKeywords
from AppleSearchAdsSDK.api.user_acl import UserAcl
from AppleSearchAdsSDK.exceptions import APIError
from AppleSearchAdsSDK.settings import API_PATH

api_dict = {
    "AdGroup": AdGroup,
    "AdGroupNegativeKeywords": AdGroupNegativeKeywords,
    "AdRejectionReasons": AdRejectionReasons,
    "Ads": Ads,
    "BudgetOrder": BudgetOrder,
    "Campaign": Campaign,
    "CampaignNegativeKeywords": CampaignNegativeKeywords,
    "Creatives": Creatives,
    "CustomProductPages": CustomProductPages,
    "ImpressionShareReports": ImpressionShareReports,
    "Reports": Reports,
    "SearchApps": SearchApps,
    "SearchGeolocations": SearchGeolocations,
    "TargetingKeywords": TargetingKeywords,
    "UserAcl": UserAcl
}


class AppleSearchAdsSDK:
    def __init__(self, access_token, version="v4", org_id=None):
        self.access_token = access_token
        self.api_base_url = f"{API_PATH}/{version}"
        self.org_id = org_id
        self.headers = None
        self.api_dict = api_dict

    def set_authorization(self, headers):
        self.headers = headers or {}
        if self.org_id:
            self.headers['X-AP-Context'] = f"orgId={self.org_id}"
        self.headers['Authorization'] = f"{self.access_token.get('token_type')} {self.access_token.get('access_token')}"
        self.headers['Content-Type'] = "application/json"

    @retry(retry_on_exception=lambda ex: isinstance(ex, APIError), stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def make_request(self, method, end_point, headers=None, params=None, data=None, timeout=180):
        self.set_authorization(headers)
        url = f"{self.api_base_url}/{end_point}"
        response = requests.request(method, url, headers=self.headers, params=params, data=json.dumps(data), timeout=timeout)
        return response

    def send(self, payload):
        api = self.api_dict[payload['api_type']](self, payload)  # 根据 api_type 从api_dict中获取对应的API实例
        return api.send()