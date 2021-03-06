import requests
import execjs
import re
import json


def get_js_result(tcontent, token = "token"):
    htmlstr = ""
    with open("app/google.js", "r", encoding="UTF-8") as f:
        line = f.readline()
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
    return execjs.compile(htmlstr).call(token, tcontent)


def translate(tcontent, fromLanguage, toLanguage):
    url = "https://translate.google.cn/translate_a/single?client=t&sl={}&tl={}&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=0&tsel=0&kc=0&tk={}&q={}".format(fromLanguage, toLanguage, get_js_result(tcontent), tcontent)
    response = requests.get(url, headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36", 
                                            "cookie": "_ga=GA1.3.941415922.1536839914; _gid=GA1.3.560171090.1538451750; 1P_JAR=2018-10-3-12; NID=140=vQcXHsvblL5DAoF2ndZZZmOoxOQpm0LbdHWv5F7mHlj8ChcfFFfP122L4h4gcCaVqv5Fl2HGaVBrLowpAsA1yim13PgjzvG4HLserRHZEjhC0vKJDJmJ0AiX-vsXAxuXPoRC3fP891jSRTj2HQ", 
                                            "content-type": "application/json; charset=UTF-8", "accept": "*/*"})

    if response.status_code != 200:
        return _('Error: the translation service failed.')

    trans_Result = ""
    navice_transText = json.loads(response.text)            # this is the original content return by request.get()    
    listof_transText = navice_transText[:1][0]        # I extract the list that contain the text which had transalted.

    # Moveover, I extract the finally translations one by one!
    for one_transText in listof_transText:
        if one_transText[0] is not None:
            trans_Result += one_transText[0]
    return trans_Result


if __name__ == "__main__":
    print(translate("黄花鱼胶。迟呢买点煲鸡。或回家买。", "zh-CN", "en"))