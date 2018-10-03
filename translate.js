public static String TranslateGoogleString(String transalteContente,String fromLanguage,String toLanguage){
    StringBuilder url=new StringBuilder();
    try {
        url.append("https://translate.google.cn/translate_a/single?").append("client=t&sl=").append(fromLanguage)
        .append("&tl=").append(toLanguage).append("&hl=zh-CN").append("&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw")
        .append("&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=2&ssel=0&tsel=0&kc=1&tk=").append(googleToken(transalteContente)).append("&q=")
        .append(URLEncoder.encode(transalteContente, "utf-8"));
    } catch (UnsupportedEncodingException e1) {
        // TODO Auto-generated catch block
        e1.printStackTrace();
    }
    System.out.println(url);
    //获取请求连接
    Thread.sleep(1000);
    Connection con = Jsoup.connect(url.toString());
    //请求头设置，特别是cookie设置（这些参数在f12都可以kanda）
    con.header("Accept", "*/*"); 
    con.header("Content-Type", "application/json; charset=UTF-8");
    con.header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"); 
    con.header("Cookie", "");
    //解析请求结果
    Document doc;
    try {
        doc = con.ignoreContentType(true).get();
        String result = doc.body().text().split(",")[0].replace("[[[", "").replace("\"", "");
        
         //获取翻译后的内容
        System.out.println(result);
        //返回内容
        return Base64.encodeBase64String(result.getBytes());
    } catch (IOException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    } 
   return null;
}


private static String token(String text) {//获取tk参数的值
     String tk = "";
     ScriptEngine engine = new ScriptEngineManager().getEngineByName("js");
     try {
          FileReader reader = new FileReader(ConfigUtil.getString("GoogleJs"));
        /* FileReader reader = new FileReader("E:/codes/java2/psmedia-btcnews/src/main/webapp/gmphtml/js/Google.js");*/
         engine.eval(reader);

         if (engine instanceof Invocable) {
             Invocable invoke = (Invocable)engine;
             tk = String.valueOf(invoke.invokeFunction("token", text));
         }
     } catch (Exception e) {
         e.printStackTrace();
     }
     return tk;
 }


//  # google.js
function token(a) {
    var k = "";
    var b = 406644;
    var b1 = 3293161072;
 
    var jd = ".";
    var sb = "+-a^+6";
    var Zb = "+-3^+b+-f";
 
    for (var e = [], f = 0, g = 0; g < a.length; g++) {
        var m = a.charCodeAt(g);
        128 > m ? e[f++] = m: (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), e[f++] = m >> 18 | 240, e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, e[f++] = m >> 6 & 63 | 128), e[f++] = m & 63 | 128)
    }
    a = b;
    for (f = 0; f < e.length; f++) a += e[f],
    a = RL(a, sb);
    a = RL(a, Zb);
    a ^= b1 || 0;
    0 > a && (a = (a & 2147483647) + 2147483648);
    a %= 1E6;
    return a.toString() + jd + (a ^ b)
};
 
function RL(a, b) {
    var t = "a";
    var Yb = "+";
    for (var c = 0; c < b.length - 2; c += 3) {
        var d = b.charAt(c + 2),
        d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
        d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
    }
    return a
}