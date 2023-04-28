import requests
import openpyxl

query = input('çekilecek adresi giriniz: ')
page_count = int(input('kaç sayfa çekilecek: '))
if page_count > 200:
    print('200 sayfadan fazla çekilemez.')
    exit()
all_products = []
for i in range(1, page_count):
    print('Sayfa: ' + str(i))
    response = requests.get('https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/' + query+ '&pi=' + str(i))
    if response.status_code == 200:
        data = response.json()['result']
        if data['products']:
            for product in data['products']:
                all_products.append(product['id'])

unique_products = set(all_products)
print('Toplam ürün sayısı: ' + str(len(unique_products)))
print('Ürün detayları çekiliyor...')
with open('products.txt', 'w') as f:
    for product_id in unique_products:
        f.write(str(product_id) + '\n')
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet['A1'] = 'Product ID'
worksheet['B1'] = 'Product Name'
worksheet['C1'] = 'Price'
worksheet['D1'] = 'Images'
worksheet['E1'] = 'Merchant'
worksheet['F1'] = 'Category'
worksheet['G1'] = 'Category ID'
worksheet['H1'] = 'Product Code'

with open('products.txt', 'r') as f:
    j = 0
    for line in f.readlines():
        product_id = line.strip()
        response = requests.get(
                'https://public.trendyol.com/discovery-web-productgw-service/api/productDetail/' + str(product_id))
        if response.status_code == 200:
            data = response.json()['result']
            worksheet['A' + str(j + 2)] = product_id
            worksheet['B' + str(j + 2)] = data['name']
            worksheet['C' + str(j + 2)] = data['price']['sellingPrice']['text']
            images = ''
            for image in data['images']:
                images += 'https://cdn.dsmcdn.com/'+image + ','
            worksheet['D' + str(j + 2)] = images
            worksheet['E' + str(j + 2)] = data['merchant']['name']
            worksheet['F' + str(j + 2)] = data['originalCategory']['name']
            worksheet['G' + str(j + 2)] = data['originalCategory']['id']
            worksheet['H' + str(j + 2)] = data['productCode']
            j += 1
workbook.save("products.xlsx")
print('Ürün detayları çekildi.')

