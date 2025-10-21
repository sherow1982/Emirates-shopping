import requests
from bs4 import BeautifulSoup
import json
import time
import xml.etree.ElementTree as ET # مكتبة جديدة لتحليل ملفات XML

# --- الإعدادات ---
BASE_URL = "https://emirates-shopping.sellsite.net/"
# تم تغيير المصدر إلى ملف sitemap.xml
SITEMAP_URL = BASE_URL + "sitemap.xml" 
OUTPUT_FILE = "products.json"
# headers لمحاكاة متصفح حقيقي وتجنب الحظر
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_product_links_from_sitemap():
    """تجلب هذه الدالة روابط جميع المنتجات من ملف sitemap.xml."""
    print(f"جاري جلب روابط المنتجات من: {SITEMAP_URL}")
    try:
        response = requests.get(SITEMAP_URL, headers=HEADERS)
        response.raise_for_status()  # للتأكد من أن الطلب ناجح
        
        # تحليل محتوى XML
        root = ET.fromstring(response.content)
        
        # مساحة الاسم (namespace) للـ sitemap، مهم جداً للبحث الصحيح
        namespace = {'ns': root.tag.split('}')[0][1:]}
        
        links = []
        # البحث عن كل وسوم <url> في ملف الـ sitemap
        for url in root.findall('ns:url', namespace):
            # البحث عن وسم <loc> داخل كل <url>
            loc_tag = url.find('ns:loc', namespace)
            if loc_tag is not None:
                product_url = loc_tag.text
                # فلترة الروابط لأخذ روابط المنتجات فقط
                if '/products/' in product_url:
                    links.append(product_url)
        
        print(f"تم العثور على {len(links)} منتج في الـ sitemap.")
        return links
        
    except requests.exceptions.RequestException as e:
        print(f"خطأ في جلب ملف sitemap: {e}")
        return []
    except ET.ParseError as e:
        print(f"خطأ في تحليل ملف XML: {e}")
        return []

def scrape_product_details(url):
    """تجلب هذه الدالة تفاصيل منتج واحد من صفحته (لم تتغير)."""
    print(f"  - جاري تفاصيل المنتج من: {url}")
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        name_tag = soup.find('h1', class_='product-title')
        name = name_tag.text.strip() if name_tag else "N/A"
        
        price_tag = soup.find('span', class_='price')
        price = price_tag.text.strip() if price_tag else "N/A"
        
        description_tag = soup.find('div', class_='product-description')
        description = description_tag.text.strip() if description_tag else "N/A"
        
        image_tag = soup.find('div', class_='product-image').find('img')
        image_url = image_tag['src'] if image_tag and image_tag.has_attr('src') else "N/A"
        
        product_data = {
            "name": name,
            "price": price,
            "description": description,
            "image_url": image_url,
            "product_url": url
        }
        
        return product_data
        
    except requests.exceptions.RequestException as e:
        print(f"    خطأ في جلب تفاصيل المنتج: {e}")
        return None
    except AttributeError as e:
        print(f"    خطأ في تحليل هيكل صفحة المنتج: {e}")
        return None

def main():
    """الدالة الرئيسية التي تنظم عملية الجلب."""
    all_products_data = []
    
    # 1. جلب جميع روابط المنتجات من الـ sitemap (هنا التغيير)
    product_links = get_product_links_from_sitemap()
    
    if not product_links:
        print("لم يتم العثور على أي منتجات. إنهاء العملية.")
        return

    # 2. المرور على كل رابط وجلب تفاصيله
    for link in product_links:
        product_details = scrape_product_details(link)
        if product_details:
            all_products_data.append(product_details)
        # إضافة تأخير صغير بين الطلبات
        time.sleep(1) 
    
    # 3. حفظ البيانات في ملف JSON
    if all_products_data:
        print(f"\nتم جلب بيانات {len(all_products_data)} منتج بنجاح.")
        print(f"جاري حفظ البيانات في ملف: {OUTPUT_FILE}")
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_products_data, f, ensure_ascii=False, indent=4)
        
        print("تم حفظ الملف بنجاح!")
    else:
        print("لم يتم جلب أي بيانات للمنتجات.")

# تشغيل الدالة الرئيسية
if __name__ == "__main__":
    main()
