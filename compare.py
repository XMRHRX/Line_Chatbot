from shopee import Shopee
from pchome import PChome
class Compare_Interface:
    
    
    def getObj(self,name ):
        if(name.lower() == "shopee"):
            return Shopee(self._target , self._default_search ,self._default_sort, self._request_num  )
        if(name.lower() == "pchome"):
            return PChome(self._target , self._default_search ,self._default_sort, self._request_num )

    def __init__(self, target , default_search =0 ,defaul_sort=0, default_num = 5 ):
        self._target = target
        self._default_search = default_search
        self._default_sort = defaul_sort
        self._request_num = default_num
        
        self._shop_list=['pchome','shopee']
        
        
    def Search(self,some_shop):
        temp = self.getObj(some_shop)
        return temp.Search()

    def SearchALL(self):
        data_list=[]
        for i in self._shop_list:
            data_list+=self.Search(i)
        s=""
        for i in data_list:
            s+=i
        return s

