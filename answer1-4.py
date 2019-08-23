import requests
from typing import Callable, Generator


def error_handler(func: Callable) -> Callable:
    """
        Bu decorator gelen Response'un 200 (OK) koduyla sorunsuz gelip
        gelmediğini kontrol eder. Eğer OK'sa response'u json formatına çevirip
        içindeki results keyinin gösterdiği value'yu geri döndürür.
    """
    def wrapper(*args, **kwargs) -> dict:
        results=None
        response = func(*args, **kwargs)
        if response.ok:
            response = response.json()
            results = response.get('results')
        return results
    return wrapper


def converter(func:Callable) -> Callable:
    """
        Fonksiyonun döndürdüğü değeri list'e cast eden decorator.
    """
    def wrapper(*args, **kwargs) -> dict:
        response = func(*args, **kwargs)
        return list(response)
    return wrapper


class RequestData:
    """
       RequestData Api'dan veri alma işlemlerini gerçekleştirmek
       için gerekli istek methodlarını içeren Class'tır.
    """
    BASE_URL = 'https://randomuser.me/api/'

    def __init__(self, count:str, *args, **kwargs):
        """
            Gelen parametreyi BASE_URL sonundaki results parametresine ekler.
            Böylece constructor'da Api'den kaç adet user datası alınacağı 
            ayarlanır. (Soruda result olarak verilen parametre Api dökümanından
            kontrol edilerek results olarak düzeltilmiştir.)
        """
        self.url = self.BASE_URL + '?results={}'.format(count)

    @error_handler
    def _make_request(self):
        """
            Api'ye GET isteği atıp gelen yanıtı döndüren method
        """
        response = requests.get(self.url)
        return response

    @converter
    def get_location(self):
        """
            make request methoduyla Api'ye istek atıp gelen yanıt içerisinden
            location keyinin gösterdiği value'yu generator olarak döndüren
            method
        """
        results = self._make_request()
        for item in results:
            yield item.get('location')

    @converter
    def get_login(self):
        """
            make request methoduyla Api'ye istek atıp gelen yanıt içerisinden
            login keyinin gösterdiği value'yu generator olarak döndüren method
        """
        results = self._make_request()
        for item in results:
            yield item.get('login')

# 100 adet username ekrana yaz
users = RequestData(100)
for username in users.get_login():
    print(username.get('username'))

# 20 adet street ekrana yaz
locations = RequestData(20)
for location in locations.get_location():
    print(location.get('street'))

# Alperen Çubuk
