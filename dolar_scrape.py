import requests
from bs4 import BeautifulSoup
import unicodedata

# --------------------

# busqueda('dolar blue')
# busqueda('won') // no disponible en la web
# busqueda('dolar oficial')
# busqueda('dolar mep/bolsa')
# busqueda('contado con liqui')
# busqueda('dolar cripto')
# busqueda('dolar tarjeta')

# funciones de busqueda (won no esta disponible actualmente)

# --------------------

coins = ['dolar blue','dolar oficial','dolar mep/bolsa','contado con liqui','dolar cripto','dolar tarjeta']

def common_text(texto): # cubre las posibles entradas que pueda tener el usuario
    # convierte la entrada del usuario a minusculas sin acentos 
    texto = texto.lower()
    # Eliminar acentos
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

def connection(): # realiza la conexion para poder scrapear la web
    
    base_url = 'https://dolarhoy.com/' # link - No tocar!!
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'} # heades predeterminados para evitar errores
    page = requests.get(base_url, headers=headers) # establece los headers
    soup = BeautifulSoup(page.text, 'html.parser') # convierte el codigo HTML a un objeto de bs4
    return soup 

def search(obj): # extrae el objeto segun lo que se necesite

    if common_text(obj) == "dolar blue":              # dolar blue tiene una estructura diferente asi que lo tratamos por aparte
        return blue_extraction()
    
    elif common_text(obj) == "everyone":
        message = ''
        soup = connection()
        div = soup.find_all('div', class_='tile is-child') 
        for a in coins:
            if a == 'dolar blue': message = message + blue_extraction() + '\n\n'
            else:
                for i in div:                                     
                    title = i.find('a', class_='title')
                    if title != None and common_text(title.text) == a: 
                        raw = i                                                                 
                        message = message + extraction(raw, title) + '\n\n' 
        return str(message.strip())

    else:
        soup = connection()
        div = soup.find_all('div', class_='tile is-child') # extrae todos los marcos
        for i in div:                                      # por cada marco extrae el title y lo compara
            title = i.find('a', class_='title')
            if title != None and common_text(title.text) == common_text(obj): # si el title coincide con el requerido: 
                raw = i                                                                   # define raw y llama a extraccion()
                return extraction(raw, title)

def blue_extraction():
    soup = connection()
    raw = soup.find('div', class_='tile is-child only-mobile')
    title = raw.find('a', class_='title')
    result = extraction(raw, title)
    return result

def extraction(raw, title): # trabaja el texto crudo (raw) para extraer los precios

    purchase = raw.find('div',class_='compra')                             # extrae el div 'compra' 
    if purchase.find('div', class_='val') == None: purchase_price = '-'    # en caso de que el valor este vacio lo reemplaza por '-'
    else: purchase_price = purchase.find('div', class_='val').text         # en caso de que tenga un valor, toma ese mismo

    sale = raw.find('div',class_='venta')                
    wrapper = sale.find('div',class_='venta-wrapper')    
    if wrapper.find('div', class_='val') == None: sale_price = '-'
    else: sale_price = wrapper.find('div', class_='val').text

    #print(f'{title.text}\npurchase: {precio_purchase}\nventa: {sale_price}\n')
    result = f'{title.text}\nCompra: {purchase_price}\nVenta: {sale_price}'
    return result

