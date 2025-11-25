import os
import json
import html
import re
from string import Template

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def make_product_schema(prod):
    schema = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": prod['title'],
        "image": prod.get('image_link',""),
        "description": prod['description'],
        "sku": prod['id'],
        "brand": {"@type":"Brand","name":"Emirates Shopping"},
        "offers": {
            "@type": "Offer",
            "priceCurrency": "AED",
            "price": prod['price'].replace(" AED", "").replace("AED ", ""),
            "url": prod['link'],
            "availability": "https://schema.org/InStock"
        }
    }
    return json.dumps(schema, ensure_ascii=False)

with open('products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

output_dir = "products-pages"
os.makedirs(output_dir, exist_ok=True)

# هيدر وفوتر ثابتين
header_html = """
<header class="main-header">
    <div class="container-bar">
        <a href="/" class="site-logo">Emirates Shopping</a>
        <nav>
            <a href="/products-pages/">المنتجات</a>
            <a href="/about-us.html">من نحن</a>
            <a href="/privacy.html">سياسة الخصوصية</a>
            <a href="/terms.html">الشروط والأحكام</a>
            <a href="/contact.html">اتصل بنا</a>
        </nav>
    </div>
</header>
"""

footer_html = """
<footer class="main-footer">
    <div class="footer-bar">
        <div>© {year} Emirates Shopping - كل الحقوق محفوظة</div>
        <div>
            <a href="/privacy.html">سياسة الخصوصية</a> |
            <a href="/terms.html">الشروط والأحكام</a> |
            <a href="/contact.html">اتصل بنا</a>
        </div>
    </div>
</footer>
"""

html_template_str = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>$title | Emirates Shopping</title>
    <meta name="description" content="$desc_long">
    <meta name="keywords" content="$title,$price,$desc_short,تسوق,عروض,الامارات,شراء اون لاين">
    <meta property="og:title" content="$title | Emirates Shopping" />
    <meta property="og:description" content="$desc_long" />
    <meta property="og:image" content="$image" />
    <meta property="og:type" content="product" />
    <meta property="og:url" content="$link" />
    <meta name="twitter:card" content="summary_large_image"/>
    <meta name="twitter:title" content="$title"/>
    <meta name="twitter:description" content="$desc_long"/>
    <meta name="twitter:image" content="$image"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <script type="application/ld+json">
    $schema_json
    </script>
    <style>
        body {background: linear-gradient(110deg,#3a80f7 0%,#5eedbc 100%); margin:0; font-family:'Cairo',Arial,sans-serif;}
        .container { max-width:745px; margin:60px auto 30px auto; background:white; border-radius:16px; box-shadow:0 8px 38px 0 rgb(52 52 151 / 10%); padding:48px 32px 32px 32px;}
        .main-header {background:#fff7;box-shadow:0 2px 14px #a8d9e170; padding:0; position:fixed; top:0; left:0; right:0; z-index:99;}
        .container-bar { max-width:1090px; margin:auto; display:flex; align-items:center; justify-content:space-between; padding:17px 12px;}
        .site-logo { font-weight:900; color:#3634ab; font-size:2.1em; text-decoration:none;}
        nav a {margin-right:24px;color:#3634ab; font-weight:600; font-size:1.12em; text-decoration:none; transition:.2s;}
        nav a:hover {color:#1eba71;}
        h1 {font-size:2.45em;color:#172255;margin-bottom:21px;margin-top:6px;}
        .product-img {text-align:center;margin-bottom:28px;}
        .product-img img {max-width:400px;width:96%;border-radius:20px;box-shadow:0 3px 25px 0 #1eba711c;}
        .price { color:#1eba71; font-size:2em; font-weight:900; margin-bottom:20px;}
        .desc { color:#363b3e; font-size:1.14em; line-height:1.9; margin-bottom:17px;}
        .desc-short { color:#888; font-size:1em; margin-bottom:29px;}

        .wa-btn {
            background:#1eba71; color:#fff; padding:16px 38px; border:0; border-radius:11px; font-size:1.15em;
            font-weight:700; cursor:pointer; transition:.21s; text-decoration:none; box-shadow:0 5px 22px #1eba711c; margin-top:28px; display:inline-block
        }
        .wa-btn:hover {background:#3634ab;}
        .prod-actions {display:flex; gap:18px; margin-bottom:30px;}
        .prod-actions a {flex:1;}
        .main-footer {width:100%;background:#3634ab; color:#fff; margin-top:40px; padding-top:26px; padding-bottom:17px; font-size:1.04em;}
        .footer-bar {max-width:900px;margin:auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap; padding:0 18px;}
        .footer-bar a {color:#5eedbc; margin-left:12px; text-decoration:underline;}
        @media(max-width:900px){.container{padding:16px} .footer-bar{flex-direction:column;gap:7px;}}
    </style>
</head>
<body>
    $header
    <div style="height:82px"></div>
    <div class="container">
        <div class="product-img"><img src="$image" alt="$title"></div>
        <h1>$title</h1>
        <div class="price">$price</div>
        <div class="desc">$desc_long</div>
        <div class="desc-short">$desc_short</div>
        <div class="prod-actions">
            <a class="wa-btn" href="https://wa.me/201110760081?text=اريد%20$wa_title%20(%20$price%20)%20عدد%20:%20[اكتب%20رقم%20الكمية]%20العنوان%20:%20[اكتب%20العنوان]" target="_blank">
                اطلب عبر واتساب
            </a>
            <a class="wa-btn" style="background:#3a80f7;" href="$link" target="_blank">
                شاهد المنتج على الموقع الرسمي
            </a>
        </div>
    </div>
    $footer
</body>
</html>
"""

from datetime import datetime
html_template_str = html_template_str.replace("$footer", "{__footer__}").replace("$header", "{__header__}")
# هروب علامات $ ما عدا المتغيرات
for escape_tag in ["title","price","desc_long","desc_short","link","image","schema_json","wa_title"]:
    html_template_str = html_template_str.replace("$"+escape_tag, f"[[{escape_tag}]]")
html_template_str = html_template_str.replace("$", "$$")
for escape_tag in ["title","price","desc_long","desc_short","link","image","schema_json","wa_title"]:
    html_template_str = html_template_str.replace(f"[[{escape_tag}]]", f"${escape_tag}")
html_template_str = html_template_str.replace("{__footer__}", footer_html.format(year=datetime.now().year))
html_template_str = html_template_str.replace("{__header__}", header_html)
html_template = Template(html_template_str)

for product in products:
    safe_title = clean_filename(product['title'])
    filename = f"{safe_title}.html"
    desc_long = f"{product['title']} هو منتج عصري وفاخر تم اختياره ليناسب احتياجاتك الشخصية بعناية. يتميز بجودة عالية وملاءمة مثالية لكل منزل/عمل أو هدية. استمتع بأداء المنتج وراحة استثنائية كل يوم. اطلب الآن بخصم مميز مع ضمان رضاك الكامل."
    desc_short = product.get('description','')
    price = product['price']
    schema_json = make_product_schema(product)
    page_content = html_template.substitute(
        title=html.escape(product['title']),
        wa_title=html.escape(product['title']),
        price=price,
        desc_long=html.escape(desc_long),
        desc_short=html.escape(desc_short),
        link=product['link'],
        image=product.get('image_link',''),
        schema_json=schema_json
    )
    outpath = os.path.join(output_dir, filename)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(page_content)
print(f"تم توليد صفحات المنتجات الاحترافية بالكامل في المجلد: {output_dir}")
