import os, json, re
from partials import head, foot
from content import HE, AR, SLUGS, GMAPS_LISTING
BASE="https://a-l-service.com"
MAPQ="%D7%90-%D7%A8%D7%91%D7%90%D7%98+1+%D7%9B%D7%A4%D7%A8+%D7%A7%D7%90%D7%A1%D7%9D"
WAZE="https://waze.com/ul?q=%D7%90.%D7%9C+%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99+%D7%AA%D7%A2%D7%91%D7%95%D7%A8%D7%94&navigate=yes"
def alt(path,L): return "/ar"+path if L["code"]=="he" else (path[3:] or "/")
def write(fn,L,path,title,desc,body,extra="",scripts=""):
    os.makedirs(os.path.dirname(fn) or ".",exist_ok=True)
    html=head(L,title,desc,BASE,path,alt(path,L),extra)+'<main id="main">'+body+'</main>'+foot(L,scripts)
    # make site-internal links relative so it works at a subpath (github.io/al-site/) and at a root domain
    pre="../"*fn.count("/") or "./"
    html=re.sub(r'(href|src)="/(?!/)',lambda m:f'{m.group(1)}="{pre}',html)
    open(fn,"w").write(html)
def ld(L,extra_type=None,name=None):
    d={"@context":"https://schema.org","@type":"AutoRepair","name":L["name"],"alternateName":"א.ל שירותי תעבורה 2017 בע\"מ","description":L["desc"],"telephone":"+972-3-9379121","email":"office@a-l-service.com",
     "address":{"@type":"PostalAddress","streetAddress":L["addr"].split("،")[0].split(",")[0],"addressLocality":"כפר קאסם" if L["code"]=="he" else "كفر قاسم","addressCountry":"IL"},
     "geo":{"@type":"GeoCoordinates","latitude":32.117812,"longitude":34.987313},
     "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Sunday","Monday","Tuesday","Wednesday","Thursday"],"opens":"07:30","closes":"17:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Friday","opens":"07:30","closes":"12:00"}],
     "areaServed":{"@type":"Country","name":"Israel"},"url":BASE+L["root"],"sameAs":[GMAPS_LISTING,"https://a-l-traffic.ussl.co.il/"],"inLanguage":L["code"]}
    if name:
        d={"@context":"https://schema.org","@type":"Service","name":name,"serviceType":name,"provider":{k:v for k,v in d.items() if k!="@context"},"areaServed":"IL"}
        if extra_type=="towing": d.update({"areaServed":{"@type":"Country","name":"Israel"},"hoursAvailable":{"@type":"OpeningHoursSpecification","dayOfWeek":["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"00:00","closes":"23:59"},"telephone":"+972-54-9395950"})
    return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'
APP='<script src="/app.js" defer></script>'
def cta(L): return f'<div class="row"><a class="btn p" href="tel:039379121">{L["cta_call"]}</a><a class="btn" href="https://wa.me/972549395950" target="_blank" rel="noopener">{L["cta_wa"]}</a></div>'
def home(L):
    r=L["root"]; svc=lambda s: f'{r}services/{s}.html'
    cards="".join(f'<div class="card"><div class="ic" aria-hidden="true">{i}</div><h3>{f"<a href=\"{svc(s)}\">{t}</a>" if s else t}</h3><p>{d}</p>'
      +(f'<a class="y" href="#towing-request">{L["tow_link"]}</a>' if s=="towing" else (f'<a class="y" href="{svc(s)}">{L["more"]}</a>' if s else ""))+'</div>' for i,t,d,s in L["services"])
    veh=f'<fieldset><legend>{L["vtype"]}</legend><label class="chk"><input type="radio" name="vehicle" value="{L["truck"]}" checked>{L["truck"]}</label><label class="chk"><input type="radio" name="vehicle" value="{L["bus"]}">{L["bus"]}</label></fieldset>'
    cons=L["consent"].format(r=r)
    td="".join(f"<li>{x}</li>" for x in L["td_items"])
    return f'''<section class="hero"><div class="wrap"><p class="tag">{L["tag"]}</p><h1>{L["h1"]}</h1><p class="lead">{L["lead"]}</p>
<div class="row"><a class="btn p" href="tel:039379121">📞 03-9379121</a><a class="btn" href="#services">{L["b_services"]}</a><a class="btn" href="#fault">{L["b_fault"]}</a><a class="btn" href="#towing-request">{L["b_tow"]}</a></div></div></section><div class="hazard"></div>
<section class="s" id="services"><div class="wrap"><h2>{L["s_title"]}</h2><p class="sub">{L["s_sub"]}</p><div class="grid">{cards}</div></div></section>
<section class="s alt" id="towing-request"><div class="wrap"><p class="y"><b>{L["tow_kicker"]}</b></p><h2>{L["tow_h"]}</h2>
<div class="card" id="towing-details" style="margin-top:24px"><h3>{L["td_title"]}</h3><ul>{td}</ul>
</div><div class="cols">
<form data-lead="towing" data-lang="{L["code"]}" novalidate><fieldset><legend>{L["need"]}</legend><label class="chk"><input type="checkbox" name="towing" checked>{L["towing"]}</label><label class="chk"><input type="checkbox" name="rescue">{L["rescue"]}</label></fieldset>
<div class="two"><div><label for="t-name">{L["cname"]}</label><input id="t-name" name="name" required minlength="2" maxlength="100" autocomplete="name"></div><div><label for="t-phone">{L["cphone"]}</label><input id="t-phone" name="phone" type="tel" required dir="ltr" autocomplete="tel" maxlength="18"></div></div>
{veh}<div><label for="t-loc">{L["loc"]}</label><input id="t-loc" name="location" required minlength="3" maxlength="300" placeholder="{L["loc_ph"]}"></div>
<div><label for="t-dest">{L["dest"]}</label><input id="t-dest" name="destination" maxlength="300" placeholder="{L["dest_ph"]}"></div>
<div><label for="t-det">{L["det"]}</label><textarea id="t-det" name="details" rows="3" maxlength="1500" placeholder="{L["det_ph"]}"></textarea></div>
<label class="chk"><input type="checkbox" name="consent" required>{cons}</label>
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn p" type="submit">{L["send_tow"]}</button><p class="err" role="alert" data-e1="{L["err_service"]}" data-e2="{L["err_fields"]}"></p></form>
<div><h3>{L["direct_h"]}</h3><p class="note">{L["direct1"]}</p><p class="note">{L["direct2"]}</p><a class="btn" href="tel:0549395950">📞 {L["tow_btn"]} · 054-9395950</a></div></div></div></section>
<section class="s" id="fault"><div class="wrap"><h2>{L["fault_h"]}</h2><p class="sub">{L["fault_sub"]}</p><div class="cols">
<form data-lead="fault" data-lang="{L["code"]}" novalidate>{veh}<div class="two"><div><label for="f-name">{L["fname"]}</label><input id="f-name" name="name" required minlength="2" autocomplete="name"></div><div><label for="f-phone">{L["fphone"]}</label><input id="f-phone" name="phone" type="tel" required dir="ltr" autocomplete="tel"></div></div>
<div><label for="f-model">{L["model"]}</label><input id="f-model" name="model" maxlength="100" placeholder="{L["model_ph"]}"></div>
<div><label for="f-desc">{L["fdesc"]}</label><textarea id="f-desc" name="details" required minlength="10" maxlength="3000" rows="5" placeholder="{L["fdesc_ph"]}"></textarea></div>
<label class="chk"><input type="checkbox" name="consent" required>{cons}</label>
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn p" type="submit">{L["send_fault"]}</button><p class="err" role="alert" data-e1="{L["err_service"]}" data-e2="{L["err_fields"]}"></p></form>
<div><h3>{L["safety_h"]}</h3><p class="note">{L["safety"]}</p><a class="btn" href="tel:0528189121">📞 {L["call_garage"]}</a></div></div></div></section>
<section class="alt"><div class="wrap vals">{"".join(f"<div><b>{a}</b><span>{b}</span></div>" for a,b in L["vals"])}</div></section>
<section class="s alt" id="contact"><div class="wrap"><h2>{L["contact_h"]}</h2><div class="cols"><div class="contact card">
<a href="tel:039379121">📞 {L["office"]} – 03-9379121</a><a href="tel:0508023393">📞 050-8023393</a><a href="tel:0549395950">🚨 {L["tow_btn"]} – 054-9395950</a><a href="mailto:office@a-l-service.com">✉️ office@a-l-service.com</a>
<p>📍 {L["addr"]}</p><div class="row" style="margin-top:4px"><a class="btn sm" href="{WAZE}" target="_blank" rel="noopener">{L["waze"]}</a><a class="btn sm" href="https://www.google.com/maps/search/?api=1&query={MAPQ}" target="_blank" rel="noopener">Google Maps</a><a class="btn sm" href="{GMAPS_LISTING}" target="_blank" rel="noopener">{L["reviews"]}</a></div></div>
<div class="card hours"><h3>🕒 {L["hours_h"]}</h3>{"".join(f"<div><span>{d}</span><span>{h}</span></div>" for d,h in L["hours"])}</div></div>
<iframe class="map" title="{L["map_t"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={MAPQ}&output=embed"></iframe></div></section>'''
ACC={"he":'''<h1>הצהרת נגישות</h1>
<p>א.ל שירותי תעבורה, מוסך לרכב כבד (משאיות ואוטובוסים) ושירותי חילוץ וגרירה, רואה חשיבות במתן שירות שוויוני לכלל הלקוחות, ופועלת להנגשת אתר האינטרנט שלה לאנשים עם מוגבלות, בהתאם לחוק שוויון זכויות לאנשים עם מוגבלות, התשנ"ח-1998, ולתקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), התשע"ג-2013.</p>
<h2>רמת הנגישות</h2><p>האתר נבנה במטרה לעמוד בדרישות התקן הישראלי ת"י 5568 המבוסס על הנחיות WCAG 2.0 ברמה AA. האתר נמצא בתהליך הנגשה מתמשך, ואיננו טוענים להתאמה מלאה לכל דרישות התקן.</p>
<h2>מה בוצע באתר</h2><ul><li>מבנה כותרות היררכי וסימון אזורי תוכן (כותרת, ניווט, תוכן ראשי, כותרת תחתונה).</li><li>הגדרת שפת הדף (עברית / ערבית) ותמיכה מלאה בכיוון כתיבה מימין לשמאל.</li><li>תוויות טקסט לכל שדות הטפסים והודעות שגיאה המוקראות לקוראי מסך.</li><li>אפשרות ניווט מלא באמצעות המקלדת, סימון פוקוס בולט וקישור "דילוג לתוכן".</li><li>ניגודיות צבעים גבוהה בין טקסט לרקע.</li><li>התאמה למסכים בגדלים שונים, כולל טלפונים ניידים, ותמיכה בהגדלת טקסט בדפדפן.</li><li>קישורי טלפון ודוא"ל לחיצים.</li></ul>
<h2>מגבלות ידועות</h2><p>ייתכן שחלקים מסוימים באתר אינם נגישים במלואם, ובהם: המפה המוטמעת של Google, וקישורים לשירותים חיצוניים כגון WhatsApp, Waze ו-Google Maps, שנגישותם באחריות הגורמים המפעילים אותם. אנו ממשיכים לפעול לשיפור הנגישות.</p>
<h2>נגישות פיזית במוסך</h2><p>לפרטים על הסדרי הנגישות במקום ניתן לפנות אלינו טלפונית לפני ההגעה.</p>
<h2>פנייה בנושא נגישות</h2><p>נתקלתם בבעיית נגישות? נשמח לשמוע ולתקן. אנא פרטו בפנייה את תיאור הבעיה, הדף שבו נתקלתם בה ופרטי התקשרות.</p>
<ul><li>רכז/ת נגישות</li><li>טלפון: <a href="tel:039379121">03-9379121</a></li><li>דוא"ל: <a href="mailto:office@a-l-service.com">office@a-l-service.com</a></li><li>כתובת: א-רבאט 1, כפר קאסם</li></ul>
<p>תאריך עדכון ההצהרה: 10/2026</p>''',
"ar":'''<h1>بيان إتاحة الوصول</h1>
<p>تولي أ.ل لخدمات النقل، كراج المركبات الثقيلة (شاحنات وحافلات) وخدمات الإنقاذ والقَطر، أهمية كبيرة لتقديم خدمة متساوية لجميع الزبائن، وتعمل على إتاحة موقعها الإلكتروني للأشخاص ذوي الإعاقة، وفقًا لقانون المساواة في الحقوق للأشخاص ذوي الإعاقة لعام 1998، وأنظمة المساواة في الحقوق للأشخاص ذوي الإعاقة (ملاءمات الإتاحة في الخدمة) لعام 2013.</p>
<h2>مستوى الإتاحة</h2><p>بُني الموقع بهدف الالتزام بمتطلبات المعيار الإسرائيلي 5568 المستند إلى إرشادات WCAG 2.0 بمستوى AA. الموقع في مرحلة إتاحة مستمرة، ولا ندّعي التوافق الكامل مع جميع متطلبات المعيار.</p>
<h2>ما تم تنفيذه في الموقع</h2><ul><li>بنية عناوين هرمية وتحديد مناطق المحتوى (الرأس، القائمة، المحتوى الرئيسي، التذييل).</li><li>تحديد لغة الصفحة (العربية / العبرية) ودعم كامل لاتجاه الكتابة من اليمين إلى اليسار.</li><li>تسميات نصية لجميع حقول النماذج ورسائل خطأ تُقرأ بواسطة قارئات الشاشة.</li><li>إمكانية التصفح الكامل بواسطة لوحة المفاتيح، إبراز واضح للتركيز ورابط "الانتقال إلى المحتوى".</li><li>تباين ألوان عالٍ بين النص والخلفية.</li><li>ملاءمة لشاشات بأحجام مختلفة بما فيها الهواتف المحمولة، ودعم تكبير النص في المتصفح.</li><li>روابط هاتف وبريد إلكتروني قابلة للنقر.</li></ul>
<h2>قيود معروفة</h2><p>قد لا تكون بعض أجزاء الموقع متاحة بالكامل، ومنها: خريطة Google المدمجة، والروابط إلى خدمات خارجية مثل WhatsApp وWaze وGoogle Maps، التي تقع مسؤولية إتاحتها على الجهات المشغّلة لها. نواصل العمل على تحسين الإتاحة.</p>
<h2>الإتاحة الفيزيائية في الكراج</h2><p>للاستفسار عن ترتيبات الإتاحة في المكان يمكن التواصل معنا هاتفيًا قبل الوصول.</p>
<h2>التواصل بشأن الإتاحة</h2><p>واجهتم مشكلة في الإتاحة؟ يسعدنا أن نسمع ونصلح. يرجى ذكر وصف المشكلة والصفحة التي واجهتموها فيها وتفاصيل الاتصال.</p>
<ul><li>منسّق/ة الإتاحة</li><li>الهاتف: <a href="tel:039379121">03-9379121</a></li><li>البريد الإلكتروني: <a href="mailto:office@a-l-service.com">office@a-l-service.com</a></li><li>العنوان: الرباط 1، كفر قاسم</li></ul>
<p>تاريخ تحديث البيان: 10/2026</p>'''}
PRIV={"he":'''<h1>מדיניות פרטיות</h1>
<p>מדיניות זו מתארת כיצד א.ל שירותי תעבורה 2017 בע"מ ("העסק") מטפלת במידע הנמסר באתר, בהתאם לחוק הגנת הפרטיות, התשמ"א-1981.</p>
<h2>איזה מידע נאסף</h2><p>בעת מילוי טופס גרירה, חילוץ או תיאור תקלה נמסרים שם, מספר טלפון, מיקום הרכב, סוג ודגם הרכב ותיאור התקלה. מסירת המידע אינה חובה על פי חוק, אך בלעדיה לא נוכל לטפל בפנייה.</p>
<h2>כיצד המידע מועבר</h2><p>בעת שליחת טופס, פרטי הפנייה נשלחים לתיבת הדוא"ל של העסק באמצעות שירות שליחת הטפסים FormSubmit (formsubmit.co), ובמקביל נפתחת הודעה מוכנה באפליקציית WhatsApp. על השימוש ב-WhatsApp חלים תנאי הפרטיות של חברת Meta, ועל FormSubmit – תנאי הפרטיות שלו. האתר מציג מפה של Google, הכפופה למדיניות הפרטיות של Google.</p>
<h2>מטרות השימוש</h2><p>המידע משמש ליצירת קשר חוזר, לתיאום שירות, גרירה או חילוץ ולמתן הצעת מחיר בלבד. לא נעביר את המידע לצד שלישי, למעט ספקי השירות הנ"ל לצורך מתן השירות או כנדרש על פי דין.</p>
<h2>אבטחה ושמירה</h2><p>אנו נוקטים אמצעים סבירים לשמירה על המידע ושומרים אותו רק כל עוד הדבר נדרש למטרות לעיל.</p>
<h2>זכויותיכם</h2><p>ניתן לבקש לעיין במידע עליכם, לתקנו או למחקו בפנייה ל-<a href="mailto:office@a-l-service.com">office@a-l-service.com</a> או בטלפון <a href="tel:039379121">03-9379121</a>.</p><p>עודכן: 10/2026</p>''',
"ar":'''<h1>سياسة الخصوصية</h1>
<p>توضح هذه السياسة كيفية تعامل أ.ل لخدمات النقل 2017 م.ض ("المصلحة") مع المعلومات المقدّمة عبر الموقع، وفقًا لقانون حماية الخصوصية لعام 1981.</p>
<h2>ما هي المعلومات التي تُجمع</h2><p>عند تعبئة نموذج القَطر أو الإنقاذ أو وصف العطل يتم تقديم الاسم، رقم الهاتف، موقع المركبة، نوعها وطرازها ووصف العطل. تقديم المعلومات ليس إلزاميًا قانونيًا، لكن بدونها لن نتمكن من معالجة الطلب.</p>
<h2>كيف تُنقل المعلومات</h2><p>عند إرسال النموذج تُرسل تفاصيل الطلب إلى البريد الإلكتروني للمصلحة بواسطة خدمة إرسال النماذج FormSubmit (formsubmit.co)، وفي الوقت نفسه تُفتح رسالة جاهزة في تطبيق WhatsApp. يخضع استخدام WhatsApp لسياسة الخصوصية لشركة Meta، ويخضع FormSubmit لسياسة الخصوصية الخاصة به. يعرض الموقع خريطة من Google تخضع لسياسة الخصوصية لـ Google.</p>
<h2>أغراض الاستخدام</h2><p>تُستخدم المعلومات للتواصل معكم، وتنسيق الخدمة أو القَطر أو الإنقاذ، وتقديم عرض سعر فقط. لن ننقل المعلومات إلى طرف ثالث باستثناء مزوّدي الخدمة المذكورين لغرض تقديم الخدمة أو كما يقتضي القانون.</p>
<h2>الأمان والحفظ</h2><p>نتخذ تدابير معقولة لحماية المعلومات ونحتفظ بها فقط طالما كان ذلك ضروريًا للأغراض المذكورة.</p>
<h2>حقوقكم</h2><p>يمكنكم طلب الاطلاع على معلوماتكم أو تصحيحها أو حذفها بالتواصل عبر <a href="mailto:office@a-l-service.com">office@a-l-service.com</a> أو الهاتف <a href="tel:039379121">03-9379121</a>.</p><p>تم التحديث: 10/2026</p>'''}
urls=[]
for L in (HE,AR):
    r=L["root"]; pre="" if L["code"]=="he" else "ar/"
    write(pre+"index.html",L,r,L["title"],L["desc"],home(L),ld(L),APP); urls.append(r)
    for fn,content,t in (("accessibility.html",ACC,L["acc"]),("privacy.html",PRIV,L["priv"])):
        write(pre+fn,L,r+fn,f'{t} | {L["name"]}',f'{t} – {L["name"]}',f'<section class="s"><div class="wrap doc">{content[L["code"]]}</div></section>'); urls.append(r+fn)
    for s in SLUGS:
        title,desc,h1,paras=L["pages"][s]; p=f"{r}services/{s}.html"
        body=f'<section class="hero"><div class="wrap" style="padding:64px 16px"><p class="tag">{L["tag"]}</p><h1>{h1}</h1></div></section><div class="hazard"></div><section class="s"><div class="wrap doc">'+"".join(f"<p>{x}</p>" for x in paras)+f'<h2>{L["cta_h"]}</h2>{cta(L)}<p style="margin-top:32px"><a class="y" href="{r}#services">{L["back"]}</a></p></div></section>'
        write(pre+f"services/{s}.html",L,p,title,desc,body,ld(L,extra_type=s,name=h1)); urls.append(p)
    nf=f'<section class="s"><div class="wrap"><h1>{L["nf_h"]}</h1><p><a class="y" href="{r}">{L["nf_back"]}</a></p></div></section>'
    write(pre+"404.html",L,r+"404.html",L["nf_h"],L["nf_h"],nf)
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{BASE}{p}</loc><lastmod>2026-10-24</lastmod></url>\n" for p in urls)+"</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
