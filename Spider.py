#!/usr/bin/env python

from zapv2 import ZAPv2

#The URL of the application to be test
#타겟의 URL를 입력.
target = 'http://localhost:5000'

#Change to match the API key set in ZAP, or use None if the API key is disabled
#apiKey값을 입력.
apiKey = 'f1dphhnjuopd8lqqmrhaf5hvs4'
zap = ZAPv2(apikey=apiKey)

"""
#test.txt파일에 저장되어 있는 url을 제외시키는 코드
print("제외 url List")
f = open("test.txt", "r")
for line in f.readlines():
   zap.spider.exclude_from_scan(line.replace("\n",""))
   print(line.replace("\n",""))
"""

#Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8080
#OWASP ZAP AIP에서 기본적으로 주어지는 포트값이 8080이므로 프록시의 포트값에 8080을 입력.
#현재 api 포트를 9000으로 수정.
zap = ZAPv2(apikey = apiKey, proxies={'http': 'http://localhost:9000','https':'https://localhost:9000'})
print('Spidering target {}'.format(target))

#The scan returns a scan id to support concurrent scanning
scanID = zap.spider.scan(target)        #Spider 수행
while int(zap.spider.status(scanID)) < 100:
    # Poll the status until it completes
    print('Spider progress %: {}'.format(zap.spider.status(scanID)))
    time.sleep(1)

print('Spider has completed!')
#Prints the URLs the spider has crawled
print('\n'.join(map(str, zap.spider.results(scanID))))
#If requred post prosess the spider results

f.close

