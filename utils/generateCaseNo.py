import pinyin


def get_pinyin_first_alpha(name):
    return "".join([i[0] for i in pinyin.get(name, " ").split(" ")]).upper()




