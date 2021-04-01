def all_maximum(lst):
    lst_result = []
    nbmax = max(lst)
    for i, j in enumerate(lst):
        if j == nbmax:
            lst_result.append(i)
    return lst_result


def spellchecker(word, lst):
    probs = []
    wo_size = len(word)
    for element in lst:
        prob = 0
        el_size = len(element)
        for el_car in element:
            for wo_car in word:
                if el_car == wo_car:
                    prob += 1
        for i in range(4):
            if el_size == wo_size - i:
                prob += 4-i
        probs.append(prob)
    lst_maxs = all_maximum(probs)
    str_words = 'This command does not seems to exist, did you mean :\n'
    for indice in lst_maxs:
        str_words += '$' + lst[indice] + ' ?\n'
    return str_words
