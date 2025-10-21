import requests
from bs4 import BeautifulSoup
import json
import time
import os

# --- الإعدادات ---
BASE_URL = "https://emirates-shopping.sellsite.net/"
LISTING_URL = BASE_URL
# سيتم حفظ الملف في المسار الجذر للمستودع
OUTPUT_FILE = "products.json" 
# headers لمحاكاة متصفح حقيقي وتجنب الحظر
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_product_links():
    """تجلب هذه الدالة روابط جميع المنتجات من صفحة القائمة الرئيسية."""
    print(f"جاري جلب روابط المنتجات من: {LISTING_URL}")
    try:
        response = requests.get(LISTING_URL, headers=HEADERS)
        response.raise_for_status()  # للتأكد من أن الطلب ناجح
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_items = soup.find_all('div', class_='product-item')
        
        links = []
        for item in product_items:
            link_tag = item.find('a')
            if link_tag and link_tag.has_attr('href'):
                full_link = BASE_URL + link_tag['href'].lstrip('/')
                links.append(full_link)
        
        print(f"تم العثور على {len(links)} منتج.")
        return links
        
    except requests.exceptions.RequestException as e:
        print(f"خطأ في جلب روابط المنتجات: {e}")
        return []

def scrape_product_details(url):
    """تجلب هذه الدالة تفاصيل منتج واحد من صفحته."""
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
    
    product_links = get_product_links()
    
    if not product_links:
        print("لم يتم العثور على أي منتجات. إنهاء العملية.")
        return

    for link in product_links:
        product_details = scrape_product_details(link)
        if product_details:
            all_products_data.append(product_details)
        time.sleep(1) 
    
    if all_products_data:
        print(f"\nتم جلب بيانات {len(all_products_data)} منتج بنجاح.")
        print(f"جاري حفظ البيانات في ملف: {OUTPUT_FILE}")
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_products_data, f, ensure_ascii=False, indent=4)
        
        print("تم حفظ الملف بنجاح!")
    else:
        print("لم يتم جلب أي بيانات للمنتجات.")

if __name__ == "__main__":
    main()
