#用來定義不同檔案之間共用的變數[全域變數]，目前只有user_id用到

#初始化
def _init():
    global _global_dict
    _global_dict = {}
#定義一個全域性變數
def set_value(name, value):
    _global_dict[name] = value
#獲得一個全域性變數,不存在則返回預設值
def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue