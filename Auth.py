#!/usr/bin/env python

import time
import urllib.parse
from zapv2 import ZAPv2


context_id = 1
apikey = 'f1dphhnjuopd8lqqmrhaf5hvs4'    #가지고 있는 OWASP-ZAP의 APIKey값
context_name = 'Default Context'
target_url = 'http://13.124.115.58:4900'        #타겟 URL

#By default ZAP API client will connect to port
zap = ZAPv2(apikey = apikey)

#Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8080
#OWASP ZAP AIP에서 기본적으로 주어지는 포트값이 8080이므로 프록시의 포트값에 8080을 입력.
#8081로 되어 있으므로 수정했으나 9000으로 수정 부탁드려요.
#[tool] -> [options] -> [Local Servers/Proxies] -> 포트에 8081을 9000으로 수정.
zap = ZAPv2(apikey = apikey, proxies={'http': 'http://localhost:8888','https':'https://localhost:8888'})

#점검 시작 시간 출력
t = time.strftime('%X')
print('startTime: ' + t)

def set_include_in_context():       # 취약점 진단 대상 선정
    exclude_url = ''
    include_url = 'http://localhost:4900.*' ##전체가 대상. target변경시 수정 필요
    zap.context.include_in_context(context_name, include_url)
    zap.context.exclude_from_context(context_name, exclude_url)
    print('Configured include and exclude regex(s) in context')

def set_logged_in_indicator():      #로그인 지시자 선정
    logged_in_regex = '\Q<div id = "main_menu" > \E'
    zap.authentication.set_logged_in_indicator(context_id, logged_in_regex)
    print('Configured logged in indicator regex: ')

def set_form_based_auth():      #로그인 폼 설정
    login_url = 'http://localhost:4900/login' ##로그인 화면 php로 바꾸어주어야함. 그외에도 타겟 변경시 수정 필요.
    login_request_data = 'username={%username%}&password={%password%}&Login=Login&user_token={%csrf_token%}'
    form_based_config = 'LoginUrl=' + urllib.parse.quote(login_url) + '&loginRequestData=' + urllib.parse.quote(login_request_data)
    zap.authentication.set_authentication_method(context_id, 'formBasedAuthentication', form_based_config)
    print('Configured form based authentication')

def set_user_auth_config():     #로그인 계정 정보 설정
    user = 'admin'
    username = 'admin'
    password = 'password'

    user_id = zap.users.new_user(context_id, user)
    user_auth_config = 'username=' + urllib.parse.quote(username) + '&password=' + urllib.parse.quote(password)
    zap.users.set_authentication_credentials(context_id, user_id, user_auth_config)
    zap.users.set_user_enabled(context_id, user_id, 'true')
    zap.forcedUser.set_forced_user(context_id, user_id)
    zap.forcedUser.set_forced_user_mode_enabled('true')
    print('User Auth Configured')
    return user_id

set_include_in_context()
set_form_based_auth()
set_logged_in_indicator()
user_id_response = set_user_auth_config()
    
