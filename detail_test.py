import json
import execjs
import requests
import asyncio

cookies = {
    'shshshfpa': 'a9cdb98a-c1df-7d6c-f75d-b8575a025224-1670230558',
    'shshshfpx': 'a9cdb98a-c1df-7d6c-f75d-b8575a025224-1670230558',
    'jcap_dvzw_fp': 'jkI-zx35PbaR8MXM0KK2dDl-6fK-xG71WFPVq1ndgJedA-bg8HSB5JsWheKjQXjSXZA6FQ==',
    'whwswswws': '',
    '__jdu': '1691395301872157302158',
    'mba_muid': '1691395301872157302158',
    'pinId': 'Hyk7Kc0yxw9W7VgxTgOJpw',
    'pin': '57633058-715238',
    'unick': 'nice%E8%82%A5%E7%89%9B',
    '_tp': 'KAp7HTNrb7gSh44VH3TmBw%3D%3D',
    '_pst': '57633058-715238',
    'wxa_level': '1',
    'cid': '9',
    'jxsid': '17021280266729410142',
    'appCode': 'ms0ca95114',
    'webp': '1',
    'visitkey': '32844653123653423',
    'equipmentId': 'YMR7276LJ5HX2IGR2EFJGTCXDH55D6VTDT32LM6FX2MHQVHXIBI7W6PH37HOKXSYJLRRWOAMSNYW7JHOL752MMJVYE',
    'deviceName': 'Chrome',
    'sc_width': '1920',
    'retina': '1',
    'deviceVersion': '116.0.0.0',
    'deviceOS': 'android',
    'deviceOSVersion': '13',
    'fingerprint': '63cbcee5323a872673ae5bffe7336ef6',
    'warehistory': '"10058118597717,10058118597717,10058118597717,10058118597717,"',
    'wqmnx1': 'MDEyNjM4NHMubXQxLm1scm9jTkNSYnJwYWFzbnBkc21nMXRDMzU0bExuMzhsLyhsa20uaXI2ZmEtS1JPRik%3D',
    'mba_sid': '17021280271022543788860037814.4',
    'cd_eid': 'jdd03YMR7276LJ5HX2IGR2EFJGTCXDH55D6VTDT32LM6FX2MHQVHXIBI7W6PH37HOKXSYJLRRWOAMSNYW7JHOL752MMJVYEAAAAMMJ3GW3NAAAAAAC6THEMXISZ2SMIX',
    '__wga': '1702129138129.1702128027669.1702128027669.1702128027669.4.1',
    '__jdv': '122270672%7Candroidapp%7Ct_335139774%7Cappshare%7CCopyURL%7C1702129138132',
    'PPRD_P': 'UUID.1691395301872157302158-LOGID.1702129138135.351935434',
    '__jd_ref_cls': 'MProductdetail_ServiceFloorExpo',
    '3AB9D23F7A4B3CSS': 'jdd03YMR7276LJ5HX2IGR2EFJGTCXDH55D6VTDT32LM6FX2MHQVHXIBI7W6PH37HOKXSYJLRRWOAMSNYW7JHOL752MMJVYEAAAAMMJ3JAEHYAAAAAC57TD4ILXHFBLIX',
    '_gia_d': '1',
    'jsavif': '1',
    'areaId': '4',
    'wlfstk_smdl': '1xixbcusfhabdhw16rta1m3fi1yqwx0y',
    '3AB9D23F7A4B3C9B': 'YMR7276LJ5HX2IGR2EFJGTCXDH55D6VTDT32LM6FX2MHQVHXIBI7W6PH37HOKXSYJLRRWOAMSNYW7JHOL752MMJVYE',
    'TrackID': '1fReYKxQpbahsMtmMOPQ-ssfH6juvtQbWLdxosmLAocuS6jbw8-MhbGNDRAE-qFOhRIFiLn2cR1RmTW80edegxpfcOVecdG_L8JPO8sl0Xrk',
    'thor': '0ED339B8DDCA1AEEE3961DA2F2AB70F8FF5315F8AAC2D08B36080554A4CA07A4C51A7FDFBB4463C792BA2507DC6411A028BDF6821787C9DC1576D2952FA1579E9E51182D6B38E86C5BE4E0DFC1EDF35378E2C92C22334882B7E918A8951A4782265EF42D78C3BF144B66894A3D5B3E94093D0F33CBAF1465BCED843BF26E62CAFDB5392D6D656B92BC4AB7937FF5106D47A058023C29A4C40B1445A3D6994E11',
    'flash': '2_0KJxE6MqShc8JBqLexNNESPrGtCydFNYy-Zb1tMvI66Yr-ciP-GKBSJXTvNA8Ucf-B4X76VoA4BzJKFpDYfII1yN9Ls-D7b9LgbPB8AR5yp*',
    'ceshi3.com': '201',
    'token': '47a92010b619e5daad135e40a752ca25,3,945627',
    '__tk': '93d5ba9f596a276a05b085761c96f4db,3,945627',
    '__jda': '181111935.1691395301872157302158.1691395301.1700918026.1702128026.5',
    '__jdc': '181111935',
    'ipLoc-djd': '4-115-9940-0',
    'shshshsID': '4e9a2a44f7f52965882e27ec3f2be18f_5_1702129466470',
    '__jdb': '181111935.16.1691395301872157302158|5.1702128026',
    'shshshfpb': 'AAgeM0k6MEs25isHffWz3XbhXWgJSJBZwIwVYUwAAAAA',
}
#
headers = {
    'authority': 'api.m.jd.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://item.jd.com',
    'pragma': 'no-cache',
    'referer': 'https://item.jd.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-referer-page': 'https://item.jd.com/10058118597717.html',
    'x-rp-client': 'h5_1.0.0',
}
#
params = {
    'appid': 'pc-item-soa',
    'functionId': 'pc_detailpage_wareBusiness',
    'client': 'pc',
    'clientVersion': '1.0.0',
    't': '1702129466819',
    'body': '{"skuId":10058118597717,"cat":"16750,16753,16783","area":"4_115_9940_0","shopId":"598847","venderId":603837,"paramJson":"{\\"platform2\\":\\"1\\",\\"colType\\":1,\\"specialAttrStr\\":\\"p0pppppppppppppppppppppppp\\",\\"skuMarkStr\\":\\"00\\"}","num":1,"bbTraffic":""}',
    'h5st': '20231209214426965;p93agwptttp9mmd8;fb5df;tk03wd9781ca618nbPaRxuRjnzVSLku9rPKbS_DB3Pg0Xvy_Jew4jIAfLhtMJQo__JUgmVbSBRAb-BpWZbPoq0W2j69P;c320850dd5a3c8180dd4858425f3a6f3fc703545711c2dea410d2e71491046d2;4.2;1702129466965;0aeefaf52c5a7fa31a1ad5e06c8551fda85ad5f4536e7e4aa639c27c742cb035bc404e042da71a6faa85368294121c991aaa072574333c3beb282fd4c183dca9c259bce08682cfcdb935c7ff0ccd36d9cdc077e07d3823c543097e5856688c99a300e9d9dabed9f68f98bd83eb2357783dd5fc2de624630f8785dbf0347c2ac330169879bf4c1f19935a3573838a68c83267757b6afe1ba171e00d171a17431ac01d57dd24db576fff467316ecef3c7ef1778a417005459a7e7297416ed8e7b0fed5be3b87831e5902a638345d531e295261468dbf9718bdba3e73457078fd4da360da4fa6f7edeecfde7c57b0b1335ac9412eb46eb32e8bb5022a2db63fbf4dbf24cab5f7ca0aae7e7ad4330db3938e1c1926273eb9d5314166d9f027535b890846e9a383a2bc93fcbcec8492fa2bed',
    # 'x-api-eid-token': 'jdd03YMR7276LJ5HX2IGR2EFJGTCXDH55D6VTDT32LM6FX2MHQVHXIBI7W6PH37HOKXSYJLRRWOAMSNYW7JHOL752MMJVYEAAAAMMJ3JAEHYAAAAAC57TD4ILXHFBLIX',
    # 'loginType': '3',
    # 'uuid': '181111935.1691395301872157302158.1691395301.1700918026.1702128026.5',
}


#

def main():
    print(json.loads(params['body']))

    with open('get_sign.js', 'r', encoding='utf-8') as f:
        _js = f.read()
    exc = execjs.compile(_js)
    rr = exc.call('get_sign', headers['user-agent'], json.loads(params['body']), cookies['unick'])
    # result = await exc.call('get_sign', headers['user-agent'], json.loads(params['body']), cookies['unick'])

    print('rr: ', rr)


if __name__ == '__main__':
    # main()

    response = requests.get(
        'https://api.m.jd.com/' + '?functionId=pc_detailpage_wareBusiness&body=%7B%22skuId%22%3A10058118597717%2C%22cat%22%3A%2216750%2C16753%2C16783%22%2C%22area%22%3A%224_115_9940_0%22%2C%22shopId%22%3A%22598847%22%2C%22venderId%22%3A603837%2C%22paramJson%22%3A%22%7B%5C%22platform2%5C%22%3A%5C%221%5C%22%2C%5C%22colType%5C%22%3A1%2C%5C%22specialAttrStr%5C%22%3A%5C%22p0pppppppppppppppppppppppp%5C%22%2C%5C%22skuMarkStr%5C%22%3A%5C%2200%5C%22%7D%22%2C%22num%22%3A1%2C%22bbTraffic%22%3A%22%22%7D&appid=pc-item-soa&client=pc&clientVersion=1.0.0&h5st=20231211142803526%3Bmgn6iz93993zz3u9%3Bfb5df%3Btk02wa02d1b7618nqyYAdBDsWZHuonVfMFXZC4zfQ03nBBRXLihX%2BzT%2B9sXk5MF2uiK16nQI%2BkJVc46tRJyU76HNivDq%3Bc5235f2f9640a557b68026749148f0a6%3B4.1%3B1702276083526%3Bee3cf7f6b94dc20e9265d83066bb9ceece4bb89e2b7e8bf5afb1bfd928788174bfa06c210ddd4437d8a2e234330c3a392aaa8efbc1a09940d67fba97ff2626f1a84d0a87bb9191da582410905e9313163862d7b22de7bcdd566ae34b2d1f5644cae0ffa811cdfea50f6d9775cfb18efadc38badbebf4db224cb2c1aa74d533b2e99cc72a7ee3b1b6457b89cd1c553389f7d0a702beecd0dbdb67f593f0a17ec8a8e14a1a8c022cc1bb37bd0f35e1f910&t=1702276083526',
        # params=params,
        cookies=cookies, headers=headers)
    print(response.text)

#
# // )geth5st('{"appid":"item-v3","functionId":"pctradesoa_getprice","client":"pc","clientVersion":"1.0.0","t":1693203742832,"body":"{\\"area\\":\\"17_1381_0_0\\",\\"pin\\":\\"\\",\\"fields\\":\\"11100000\\",\\"skuIds\\":\\"100058005881,100021318954,100038837202,100020913402\\",\\"source\\":\\"pc-item\\"}"}'

# resp = requests.post('http://127.0.0.1:8911/h5st', data=params)
# print(resp.text)
    print(response.request.url)
