import itertools
import random

from colorama import Fore

COUNT = 300  # Количество симуляций
OUTPUT_COUNT = 10  # Количество выводимых элементов
RANDOM = True  # Флаг рандомизации предметов (если False - Будет использовать предметы по указанному порядку)
result_dicts = {i: {} for i in range(COUNT)}

# Возможные названия гравировок для вставки в предметы
positive_names = ['Cжатие', 'Титаноборец', 'Подготовка', 'Защита', 'Гильотина', 'Адреналин']

# Требуемые гравировки
required_names = {
    'Cжатие': 15,
    'Титаноборец': 15,
    'Подготовка': 15,
    'Защита': 15,
    'Гильотина': 15,
    'Адреналин': 10
}
# Название предметов и количество дырок для гравировок
items = {
    'Гравировка №1': {
        'positive_name_1': 12,
    },
    'Гравировка №2': {
        'positive_name_1': 12,
    },
    'Фетранит': {
        'positive_name_1': 9,
        'positive_name_2': 9
    },
    'Ожерелье': {
        'positive_name_1': 6,
        'positive_name_2': 3
    },
    'Серьга 1': {
        'positive_name_1': 6,
        'positive_name_2': 3
    },
    'Серьга 2': {
        'positive_name_1': 6,
        'positive_name_2': 3
    },
    'Кольцо 1': {
        'positive_name_1': 6,
        'positive_name_2': 3
    },
    'Кольцо 2': {
        'positive_name_1': 6,
        'positive_name_2': 3
    },
}


def get_names(required_names, mas, repeat):  # Получение названий гравировок
    return [combination for combination in itertools.product([item for item in required_names.keys() if item in mas], repeat=repeat) if len(set(combination)) == repeat]


def get_sum(counter_value, name):  # Получение суммы вставленных гравировок
    res = 0
    for value in result_dicts[counter_value].values():
        if isinstance(value, dict):
            res += value.get(name, 0)
    return res


def get_max_value(counter_value, name, value):  # Получение количества поинтов гравировки для вставки в предмет
    max_value = required_names.get(name)
    sum_val = get_sum(counter_value, name)
    dif = max_value - sum_val
    if dif > 0:
        if dif < value:
            return dif
        else:
            return value


for counter_value in range(0, COUNT):
    items_copy = items.copy()
    if RANDOM:
        keys = list(items_copy.keys())
        random.shuffle(keys)
        items_copy = {k: items_copy.get(k) for k in keys}
    for item, item_dict in items_copy.items():
        results = []
        saved_results = []
        keys = [key for key in item_dict.keys() if key.startswith('positive_name')]
        names = get_names(required_names, positive_names, repeat=len(keys))
        for names_item in names:
            result = {}
            for key, name in zip(keys, names_item):
                max_value = item_dict.get(key)
                res = get_max_value(counter_value, name, max_value)
                if res is None:
                    result[name] = -max_value
                else:
                    result[name] = res
                #print(name, key, item_dict, res)
            if all(True if value > 0 else False for value in result.values()):
                results.append(result)
            else:
                saved_results.append(result)

        if (len(result_dicts[counter_value].keys())) == 0 and (len(results) >= counter_value + 1 or len(saved_results) >= counter_value + 1):
            if len(results) >= counter_value + 1:
                results = sorted(results, key=lambda x: sum(x.values()), reverse=True)
                res_dict = results[counter_value]
                #print(f'[{item}] BASE: ', res_dict, results)
            else:
                saved_results = sorted(saved_results, key=lambda x: (sum(value for value in x.values() if value > 0), sum(abs(value) for value in x.values())), reverse=True)
                res_dict = {k: abs(v) for k, v in saved_results[counter_value].items()}
                #print(f'[{item}] SAVED: ', res_dict,  saved_results)
            result_dicts[counter_value][item] = res_dict
        else:
            if len(results) > 0 or len(saved_results) > 0:
                if len(results) > 0:
                    results = sorted(results, key=lambda x: sum(x.values()), reverse=True)
                    res_dict = results[0]
                    #print(f'[{item}] BASE: ', res_dict, results)
                else:
                    saved_results = sorted(saved_results, key=lambda x: (
                    sum(value for value in x.values() if value > 0), sum(abs(value) for value in x.values())),
                                           reverse=True)
                    res_dict = {k: abs(v) for k, v in saved_results[0].items()}
                    #print(f'[{item}] SAVED: ', res_dict, saved_results)
                result_dicts[counter_value][item] = res_dict

# Получение наиболее хороших вариантов
best_keys = {}
for counter_value in range(0, COUNT):
    best_items = 0
    excess = {}
    for key, value in result_dicts[counter_value].items():
        for value_key, value_value in value.items():
            excess[value_key] = excess.get(value_key, 0) + value_value

    for key, value in excess.items():
        requried = required_names.get(key)
        if value >= requried:
            best_items += 1
    best_keys[counter_value] = best_items

best_keys = [k for k, v in sorted(best_keys.items(), key=lambda item: item[1], reverse=True)]
print(best_keys)

# Вывод ТОП n вариантов
for counter_value in best_keys[:OUTPUT_COUNT]:
    print(f'\n\nВариант №{counter_value + 1}')
    excess = {}

    for key, value in result_dicts[counter_value].items():
        max_values = items.get(key)
        print(Fore.LIGHTMAGENTA_EX, key, sep='', end='\t')
        if isinstance(max_values, dict) and isinstance(value, dict) and len(max_values.keys()) == len(value.keys()):
            text = ', '.join(f'{Fore.LIGHTYELLOW_EX}{v} {Fore.LIGHTRED_EX if value.get(v) != max_values.get(m_v) else Fore.LIGHTGREEN_EX}{value.get(v)}/{max_values.get(m_v)}' for v, m_v in zip(value, max_values))
            print(text)
        for value_key, value_value in value.items():
            excess[value_key] = excess.get(value_key, 0) + value_value
    print()
    for key, value in excess.items():
        requried = required_names.get(key)
        if value > requried:
            print(Fore.LIGHTRED_EX, end='')
        elif value < requried:
            print(Fore.LIGHTYELLOW_EX, end='')
        else:
            print(Fore.LIGHTGREEN_EX, end='')
        print(f'{key} | {value}/{requried}', Fore.RESET)
