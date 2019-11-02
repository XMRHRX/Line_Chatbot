


class Shop():
    _search_dict = {0:"price", 1:"rank", 2:"new",3:"sale"}
    _sort_dict = {0:'asc',1:'desc'}
    def __init__(self, target , default_search = 0 ,defaul_sort=0, default_num = 5 ):
        self._sort_by = defaul_sort
        self._search_by = default_search
        self._request_num = default_num
        self._target = target
    
    def Search(self):
        pass

    def checkAccept(self,to_be_check,accept_list):
        for i in to_be_check:
            if(i in accept_list):
                return to_be_check[i]
        return accept_list[0]
