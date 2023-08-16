# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import logging

from django.conf import settings
from django.contrib import auth, messages
from django.core.cache import caches
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from blueapps.account.components.bk_token.forms import AuthenticationForm
from blueapps.account.conf import ConfFixture
from blueapps.account.handlers.response import ResponseHandler
from blueapps.account.models import User

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

logger = logging.getLogger("component")
cache = caches["login_db"]


class LocalLoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        #验证当前的url
        current_page_url = request.get_full_path()
        #验证当前用户是否登录
        current_user = request.user
        if current_user.is_staff is False:
            if 'admin' not in current_page_url:
                return HttpResponseRedirect(reverse('admin:index'))

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(request,username=username,password=password)
            if user is not None:
                auth.login(request,user)

        return None

    def process_response(self, request, response):
        return response


def get_addr_by_request(request):
    """根据请求获取IP对应的所在地址"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get("REMOTE_ADDR")  # 这里获得代理ip
    setattr(request, "current_ip", ip)
