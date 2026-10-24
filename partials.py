WA_SVG='<svg width="30" height="30" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>'
def head(L,title,desc,base,path,alt_path,extra=""):
    other="ar" if L["code"]=="he" else "he"
    he_path=path if L["code"]=="he" else alt_path; ar_path=alt_path if L["code"]=="he" else path
    he_cur=' aria-current="true"' if L["code"]=="he" else ""; ar_cur=' aria-current="true"' if L["code"]=="ar" else ""
    return f'''<!doctype html><html lang="{L["code"]}" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{base}{path}">
<link rel="alternate" hreflang="{L["code"]}" href="{base}{path}"><link rel="alternate" hreflang="{other}" href="{base}{alt_path}"><link rel="alternate" hreflang="x-default" href="{base}{path if L["code"]=="he" else alt_path}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:locale" content="{L["locale"]}"><meta property="og:url" content="{base}{path}"><meta property="og:image" content="{base}/img/og.webp"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700&family=Secular+One&family=Cairo:wght@400;700&display=swap"><link rel="stylesheet" href="/style.css"><link rel="icon" href="/favicon.ico">{extra}</head><body class="l-{L["code"]}">
<a class="skip" href="#main">{L["skip"]}</a>
<header><div class="wrap"><a class="logo" href="{L["root"]}">{L["logo"]}</a><nav aria-label="{L["navlabel"]}"><a href="{L["root"]}#services">{L["nav"][0]}</a><a href="{L["root"]}#towing-request">{L["nav"][1]}</a><a href="{L["root"]}#contact">{L["nav"][2]}</a></nav><div class="hd"><span class="lang"><a href="{he_path}" lang="he" hreflang="he"{he_cur}>עב</a> / <a href="{ar_path}" lang="ar" hreflang="ar"{ar_cur}>عر</a></span><a class="btn p sm" href="tel:039379121">📞 {L["callnow"]}</a></div></div></header>'''
def foot(L,scripts=""):
    r=L["root"]
    return f'''<footer><div class="wrap">{L["copy"]}<br><a href="{r}accessibility.html">{L["acc"]}</a>|<a href="{r}privacy.html">{L["priv"]}</a></div></footer>
<a class="wa" href="https://wa.me/972549395950" target="_blank" rel="noopener" aria-label="{L["walabel"]}">{WA_SVG}</a>
<div class="callbar"><a href="tel:039379121">📞 {L["callbar"]} 03-9379121</a><a href="https://wa.me/972549395950" target="_blank" rel="noopener">💬 {L["wa"]}</a></div>
{scripts}</body></html>'''
