from shopee import Shopee
from pchome import PChome

class ShopFactory:
    def __init__(self):
        pass
    def getObj(self,name):
        if(name.lower() == "shopee"):
            return Shopee()
        if(name.lower() == "pchome"):
            return PChome()