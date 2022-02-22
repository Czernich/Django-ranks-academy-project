from numpy import number
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

def get_excel_data(xlsx_directory):
    excel_data = pd.read_excel(xlsx_directory)
    columns = excel_data.columns.ravel()
    x_values = excel_data['t'].tolist()
    y_values = excel_data['yt'].tolist()

    data_dict = {
        columns[0]: x_values,
        columns[1]: y_values,
    }

    return data_dict


# Srednia arytmetyczna
def arithmetic_average(dictionary):
    list = []
    avg = sum(dictionary['yt'])/len(dictionary['yt'])
    list.append(round(avg,3))
    return list

# Srednia chronologiczna
def chronological_average(dictionary):
    list = []
    mid_sum = 0
    for i in range(1,len(dictionary['yt'])-1):
        mid_sum += dictionary['yt'][i]

    avg = (0.5*dictionary['yt'][0] + mid_sum + 0.5*dictionary['yt'][len(dictionary['yt'])-1])/len(dictionary['yt'])
    list.append(round(avg,3))
    return list

# Przyrost absolutny [delta t/0]
def absolute_increase(dictionary):
    abs_increase = []
    current_value = 0
    for i in range(0,len(dictionary['yt'])):
        current_value = round(dictionary['yt'][i] - dictionary['yt'][0],2)
        abs_increase.append(current_value)
    return abs_increase

# Przyrost absolutny [delta t/t-1]
def absolute_increase_t_1(dictionary):
    abs_increase = [' ']
    current_value = 0
    for i in range(1,len(dictionary['yt'])):
        current_value = round(dictionary['yt'][i] - dictionary['yt'][1],2)
        abs_increase.append(current_value)
    return abs_increase

# Przyrost wzgledny [delta t/0]
def relative_increase(dictionary, absolute_increase):
    rel_increase = []
    current_value = 0
    for i in range(0,len(dictionary['yt'])):
        current_value = round(absolute_increase[i]/dictionary['yt'][0],2)
        rel_increase.append(current_value)
    return rel_increase

# Przyrost wzgledny [delta t/t-1]
def relative_increase_t_1(dictionary, absolute_increase):
    rel_increase = [' ']
    current_value = 0
    for i in range(1,len(dictionary['yt'])):
        current_value = round(absolute_increase[i]/dictionary['yt'][1],2)
        rel_increase.append(current_value)
    return rel_increase

# Indeks indywidualny jednopodstawowy
def single_base_individual_index(dictionary):
    individual_index = []
    current_value = 0
    for i in range(0,len(dictionary['yt'])):
        current_value = (dictionary['yt'][i] - dictionary['yt'][0])/dictionary['yt'][0] + 1
        individual_index.append(round(current_value,2))

    return individual_index

# Indeks indywidualny lancuchowy
def individual_string_index(dictionary):
    individual_index = [" ",]
    current_value = 0
    for i in range(1,len(dictionary['yt'])):
        current_value = dictionary['yt'][i]/dictionary['yt'][i-1]
        individual_index.append(round(current_value,2))

    return individual_index

# Srednie ruchome 3 okresowe
def three_period_moving_averages(dictionary):
    results_list = [' ']
    current_value = 0
    for i in range(0,len(dictionary['yt'])-2):
        current_value = 1/3*(dictionary['yt'][i] + dictionary['yt'][i+1] + dictionary['yt'][i+2])
        results_list.append(round(current_value,2))
    results_list.append(' ')
    return results_list

# Srednie ruchome 4 okresowe
def four_period_moving_averages(dictionary):
    results_list = [' ',' ']
    current_value = 0
    for i in range(0,len(dictionary['yt'])-3):
        current_value = 1/4*(0.5*dictionary['yt'][i] + dictionary['yt'][i+1] + dictionary['yt'][i+2] + 0.5*dictionary['yt'][i+3])
        results_list.append(round(current_value,2))
    results_list.append(' ')
    return results_list

# Srednie ruchome 5 okresowe
def five_period_moving_averages(dictionary):
    results_list = [' ',' ']
    current_value = 0
    for i in range(0,len(dictionary['yt'])-4):
        sum = 0
        for k in range(i,i+5):
            sum += dictionary['yt'][k]
        current_value = 1/5*sum
        results_list.append(round(current_value,2))
    results_list.extend([' ',' '])
    return results_list

# Metoda wyrownania wykladniczego [alfa1 i alfa 2]
def exponential_smoothing_method(dictionary, alfa):
    results_list = []
    current_value = 0
    results_list.append(dictionary['yt'][0])
    for i in range(0,len(dictionary['yt'])-1):
        current_value = alfa*dictionary['yt'][i+1]+(1-alfa)*dictionary['yt'][i]
        results_list.append(round(current_value,2))
    return results_list

# Srednia geometryczna
def geometric_average(isi):
    list = []
    multiplication = 1
    iterator = 0
    for number in isi[1:len(isi)]:
        if number != '-':
            iterator += 1
            multiplication = multiplication * number
    result = multiplication**(1/iterator)
    list.append(round(result,3))
    return list

# Wartosc nastepnego wyrazu
def get_next_value(dictionary, geo_avg):
    results = []
    power = len(dictionary['yt']) + 1
    result = dictionary['yt'][0] * (geo_avg[0]**power)
    results.append(round(result,3))
    return results
    
# Usuniecie trendu zt
def trend_remove(dictionary,three_period_moving_averages):
    result = []
    for i in range(len(dictionary['yt'])):
        if three_period_moving_averages[i] != ' ':
            result.append(round(dictionary['yt'][i] - three_period_moving_averages[i],2))
        else:
            result.append(' ')
    return result

#Wyznaczanie wskaźników wachań okresowych i yt z kreską
def line_yt(yt, trend_remove):
    first_slice = trend_remove[::3]
    second_slice = trend_remove[1::3]
    third_slice = trend_remove[2::3]
    lists = [first_slice, second_slice, third_slice]
    Si_prims = []
    for list in lists:
        sum = 0
        length = 0
        for element in list:
            if element != ' ':
                length += 1
                sum = sum + element
        Si_prims.append(sum/length)
    
    s1 = round(Si_prims[0] - (Si_prims[0]+Si_prims[1]+ 1/3*(Si_prims[2])),3)
    s2 = round(Si_prims[1] - (Si_prims[0]+Si_prims[1]+ 1/3*(Si_prims[2])),3)
    s3 = round(Si_prims[2] - (Si_prims[0]+Si_prims[1]+ 1/3*(Si_prims[2])),3)

    si = [s1,s2,s3]
    slice_one = yt['yt'][0::3]
    slice_two = yt['yt'][1::3]
    slice_three = yt['yt'][2::3]

    result = []
    for i in range(len(slice_one)):
        result.append(round(slice_one[i]-si[0],2))
        result.append(round(slice_two[i]-si[1],2))
        result.append(round(slice_three[i]-si[2],2))
        
    return result
    
# Wyznaczanie et
def et_diff(three_period_moving_avg, line_yt):
    result = [' ']
    for i in range(1,len(line_yt)-1):
        result.append(round(line_yt[i]-three_period_moving_avg[i],2))
    result.append(' ')
    return result

# Wyznaczanie et^2
def et_power_two(et):
    result = [' ']
    for element in et:
        if element != ' ':
            result.append(round(element**2,2))
    result.append(' ')
    return result

# Wyznaczanie modulo z et
def et_absolute(et):
    result = [' ']
    for element in et:
        if element != ' ':
            result.append(round(abs(element),2))
    result.append(' ')
    return result

# Wyznaczanie MSE
def MSE_MAE(et_var):
    result = []
    sum = 0
    k = 0
    for i in range(len(et_var)-1): 
        if et_var[i] != ' ':
            sum += et_var[i]
            k += 1
    avg = round(sum/k,3)
    result.append(avg)
    return result
    

#yt + nastepny wyraz
def yt_next_value(dictionary, next_value):
    y_data = []
    for y in dictionary['yt']:
        y_data.append(y)
    y_data.append(round(next_value[0],2))
    return y_data


def createResults(xlsx_file):
    excel_data = get_excel_data(xlsx_file)
    ar_average = arithmetic_average(excel_data)
    chr_average = chronological_average(excel_data)
    abs_increase = absolute_increase(excel_data)
    abs_increase_t_1 = absolute_increase_t_1(excel_data)
    rel_increase = relative_increase(excel_data, abs_increase)
    rel_increase_t_1 = relative_increase_t_1(excel_data, abs_increase_t_1)
    individual_index = single_base_individual_index(excel_data)
    string_index = individual_string_index(excel_data)
    three_period_moving_avg = three_period_moving_averages(excel_data)
    four_period_moving_avg = four_period_moving_averages(excel_data)
    five_period_moving_avg = five_period_moving_averages(excel_data)
    exponential_smoothing_method_alfa1 = exponential_smoothing_method(excel_data, 0.3)
    exponential_smoothing_method_alfa2 = exponential_smoothing_method(excel_data, 0.7)
    geometric_avg = geometric_average(string_index)
    next_value = get_next_value(excel_data, geometric_avg)
    next_value_index = len(excel_data['yt']) + 1
    yt_additive_value = yt_next_value(excel_data, next_value)
    zt = trend_remove(excel_data, three_period_moving_avg)
    yt_lined = line_yt(excel_data, zt)
    et = et_diff(three_period_moving_avg, yt_lined) 
    et_power = et_power_two(et)
    et_abs = et_absolute(et)
    mse = MSE_MAE(et_power)
    mae = MSE_MAE(et_abs)


    results = {
        'excel_data': {
            'name': 'Dane Excel ',
            'data': excel_data,
            },
        'ar_average': {
            'name': 'Średnia arytmetyczna',
            'data': ar_average,
            },
        'chr_average': {
            'name': 'Średnia chronologiczna',
            'data': chr_average,
            },   
        'abs_increase': {
            'name': 'Przyrost absolutny [delta t/0]',
            'data': abs_increase,
            },
        'abs_increase_t_1': {
            'name': 'Przyrost absolutny [delta t/t-1]',
            'data': abs_increase_t_1,
            },
        'rel_increase': {
            'name': 'Przyrost względny [delta t/0]',
            'data': rel_increase,
            },
        'rel_increase_t_1': {
            'name': 'Przyrost względny [delta t/t-1]',
            'data': rel_increase_t_1,
            },
        'individual_index': {
            'name': 'Indeks indywidualny jednopodstawowy',
            'data': individual_index,
            },
        'string_index': {
            'name': 'Indeks indywidualny łancuchowy',
            'data': string_index,
            },
        'three_period_moving_avg': {
            'name': 'Średnie ruchome 3 okresowe',
            'data': three_period_moving_avg,
            },
        'four_period_moving_avg': {
            'name': 'Średnie ruchome 4 okresowe',
            'data': four_period_moving_avg,
            },
        'five_period_moving_avg': {
            'name': 'Średnie ruchome 5 okresowe',
            'data': five_period_moving_avg,
            },
        'exponential_smoothing_method_alfa1': {
            'name': 'Metoda wyrownania wykladniczego alfa=0.3',
            'data': exponential_smoothing_method_alfa1,
            },
        'exponential_smoothing_method_alfa2': {
            'name': 'Metoda wyrownania wykladniczego alfa=0.7',
            'data': exponential_smoothing_method_alfa2,
            },
        'geometric_avg': {
            'name': 'Średnia geometryczna',
            'data': geometric_avg,
            },
        'next_value': {
            'name': f'Wartość {next_value_index} wyrazu',
            'data': next_value,
            },
        'yt_additive_value': {
            'name': f'Yt + {next_value_index} wyraz',
            'data': yt_additive_value,
            },
        'zt': {
            'name': 'Usunięcie trendu zt',
            'data': zt,
            },
        'yt_lined': {
            'name': 'ȳt',
            'data': yt_lined,
            },
        'et_diff': {
            'name': 'et',
            'data': et,
            },
        'et_power': {
            'name': 'et^2',
            'data': et_power,
            },
        'et_abs': {
            'name': '|et|',
            'data': et_abs,
            },
        'mse': {
            'name': 'MSE',
            'data': mse,
            },
        'mae': {
            'name': 'MAE',
            'data': mae,
            },

    }
    return results


    
