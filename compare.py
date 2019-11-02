from shopee import Shopee
from pchome import PChome
class Compare_Interface:
    
    shop_list=['pchome','shopee']
    def getObj(self,name,target , default_search =0 ,defaul_sort=0, default_num = 5 ):
        if(name.lower() == "shopee"):
            return Shopee(target , default_search ,defaul_sort, default_num  )
        if(name.lower() == "pchome"):
            return PChome(target , default_search ,defaul_sort, default_num)

    def __init__(self, target , default_search =0 ,defaul_sort=0, default_num = 5 ):
        self._target = target
        self._default_search = default_search
        self._default_sort = defaul_sort
        self._request_num = default_num
        
        self._default_search = default_search
        
        
    def Search(self,some_shop):
        temp = self.getObj(some_shop,self._target)
        return temp.Search(self._target, self._default_search, self._default_sort, self._request_num)

    def SearchALL(self):
        data_list=[]
        for i in shop_list:
            data_list+=self.Search(i)
        return data_list

