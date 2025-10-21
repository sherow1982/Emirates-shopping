import requests
from bs4 import BeautifulSoup
import json

# رابط الصفحة التي نريد سحب البيانات منها
URL = 'https://www.namshi.com/uae-en/men-sale/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()  # التأكد من أن الطلب ناجح

    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    
    # --- التغيير الرئيسي هنا ---
    # استخدام محددات جديدة تعتمد على data-testid لتكون أكثر استقرارًا
    products_list = soup.find_all('a', {'data-testid': 'product-card'})

    if not products_list:
        print("لم يتم العثور على أي منتجات. قد يكون المحدد (Selector) قد تغير مرة أخرى.")
    else:
        for item in products_list:
            # استخراج اسم المنتج
            name = item.find('h3', {'data-testid': 'product-name'}).get_text(strip=True)
            
            # استخراج السعر
            price = item.find('span', {'data-testid': 'product-price'}).get_text(strip=True)
            
            # استخراج رابط الصورة
            image_url = item.find('img')['src']
            
            # استخراج رابط المنتج الكامل
            product_url = item['href']
            if not product_url.startswith('http'):
                product_url = 'https://www.namshi.com' + product_url

            products.append({
                'name': name,
                'price': price,
                'image_url': image_url,
                'product_url': product_url
            })

    # حفظ البيانات في ملف JSON
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

    print(f"تم سحب {len(products)} منتج بنجاح وحفظها في ملف products.json")

except requests.exceptions.RequestException as e:
    print(f"خطأ في طلب HTTP: {e}")
except Exception as e:
    print(f"حدث خطأ غير متوقع: {e}")
