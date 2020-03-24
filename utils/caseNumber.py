import datetime

import pinyin


def get_pinyin_first_alpha(name):
    time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%d')
    return "".join([i[0] for i in pinyin.get(name, " ").split(" ")]).upper()+ '_' + time

