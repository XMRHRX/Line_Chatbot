from shopee import Shopee
from pchome import PChome
class Compare_Interface:
    
    shop_list=['pchome','shopee']
    def getObj(self,target , default_search =0 ,defaul_sort=0, default_num = 5 ):
        if(name.lower() == "shopee"):
            return Shopee(target , default_search ,defaul_sort, default_num  )
        if(name.lower() == "pchome"):
            return PChome()

    def __init__(self, target , default_search =0 ,defaul_sort=0, default_num = 5 ):
        self._default_search = default_search
        self._default_sort = defaul_sort
        self._request_num = default_num
        self._target = target
        self._default_search = default_search
        self._shop_list = [getObj(i,self._target, default_search,self._default_sort, self._request_num) for i in shop_list]
        
        
    
    

    def SearchALL(self):
        pass

