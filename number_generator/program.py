
# ALGORITHM FOR CONVERTING NUMBERS TO SAMPLES
# ___________________________________________
# INPUT: A positive integer, up to 9999.
# INPUT: A dictionary of sample references.
# OUTPUT: A list of sample references.

# We present a function for each language, documenting which samples
# are necessary. Since the sample generation depends on the language
# we shall document the format of the dictionary per function by
# providing a sample dictionary. Such sample dictionary is also
# used for testing purposes.

# Each dictionary contains the sample "error" which is returned
# whenever there is an error while invoking the procedure.

# Example use:
# > generate_num_english(152, english_samples())
# ['one', 'hundred', 'and', 'fifty', 'two']
# > generate_num_french(152, french_samples())
# ['cent', 'cinquante', 'deux']
# > generate_num_bambara(152, bambara_samples())
# ['keme', 'ni', 'bi', 'duuru', 'ni', 'fila']

###
### ENGLISH
###

def english_samples():
  return {
    'error': 'error',
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety',
    100: 'hundred',
    1000: 'thousand',
    'and': 'and',
    'comma': ', '
  }
#end english_samples

def generate_num_english(d, dict):
  if (d < 0 or d > 9999): return [dict['error']]
  # Non-regular terminals
  if (d <= 19): return [dict[d]]
  if (d <= 90 and d % 10 == 0): return [dict[d]]
  # Regular terminals
  if (d <= 99): return [dict[(d//10)*10],dict[d%10]]
  if (d <= 900 and d % 100 == 0): return [dict[d//100],dict[100]]
  if (d <= 9000 and d % 1000 == 0): return [dict[d//1000],dict[1000]]
  # Regular non-terminals
  if (d <= 999):
    result = [dict[d//100],dict[100],dict['and']]
    result.extend(generate_num_english(d%100, dict))
    return result
  if (d <= 9999):
    result = [dict[d//1000],dict[1000]]
    imm = generate_num_english(d%1000, dict)
    if (dict['and'] not in imm): result.append(dict['and'])
    else: result.append(dict['comma'])
    result.extend(imm)
    return result
# end generate_num_english

###
### FRENCH (International)
###

def french_samples():
  return {
    'error': 'error',
    0: 'zero',
    1: 'un',
    2: 'deux',
    3: 'trois',
    4: 'quatre',
    5: 'cinq',
    6: 'six',
    7: 'sept',
    8: 'huit',
    9: 'neuf',
    10: 'dix',
    11: 'onze',
    12: 'douze',
    13: 'treize',
    14: 'quatorze',
    15: 'quinze',
    16: 'seize',
    20: 'vingt',
    30: 'trente',
    40: 'quarante',
    50: 'cinquante',
    60: 'soixante',
    80: 'quatre-vingts',
    100: 'cent',
    '100s': 'cents',
    1000: 'mille',
    'and': 'et',
    'comma': ', '
  }
#end french_samples

def generate_num_french(d, dict):
  if (d < 0 or d > 9999): return [dict['error']]
  # Non-regular terminals
  if (d <= 16): return [dict[d]]
  if ((d <= 60 or d == 80) and d % 10 == 0): return [dict[d]]
  # Regular terminals
  if (d >= 17 and d <= 19): return [dict[10],dict[d%10]]
  if (d <= 60 and d % 10 == 1): return [dict[(d//10)*10],dict['and'],dict[1]]
  if (d <= 60): return [dict[(d//10)*10],dict[d%10]]
  # Regular non-terminals
  if (d <= 99):
    result = [dict[(d//20)*20]]
    if (d == 61): result.append(dict['and'])
    result.extend(generate_num_french((d-60)%20, dict))
    return result
  if (d <= 999):
    result = [dict['100s']] if (d >= 200 and d % 100 == 0) else [dict[100]]
    if (d >= 200): result.insert(0,dict[d//100])
    if (d % 100 > 0): result.extend(generate_num_french(d%100, dict))
    return result
  if (d <= 9999):
    result = [dict[1000]]
    if (d >= 2000): result.insert(0,dict[d//1000])
    if (d % 1000 > 0): result.extend(generate_num_french(d%1000, dict))
    return result

###
### BAMBARA
###

def bambara_samples():
  return {
    'error': 'error',
    0: '???',
    1: 'kelen',
    2: 'fila',
    3: 'saba',
    4: 'naani',
    5: 'duuru',
    6: 'wooro',
    7: 'wolonwula',
    8: 'seegin',
    9: 'kononton',
    10: 'tan',
    20: 'mugan',
    100: 'keme',
    '10s': 'bi',
    '100s': 'keme',
    '1000s': 'wa',
    'and': 'ni'
  }

def generate_num_bambara(d, dict):
  if (d < 0 or d > 9999): return [dict['error']]
  # Non-regular terminals
  if (d <= 10 or d == 20 or d == 100): return [dict[d]]
  # Regular terminals
  if (d <= 99 and d % 10 == 0): return [dict['10s'],dict[d//10]]
  if (d <= 999 and d % 100 == 0): return [dict['100s'],dict[d//100]]
  if (d <= 9999 and d % 1000 == 0): return [dict['1000s'],dict[d//1000]]
  # Regular non-terminals
  result = []
  if (d//1000 > 0):
    result.extend(generate_num_bambara((d//1000)*1000, dict))
  if ((d%1000)//100 > 0):
    if (result): result.append(dict['and'])
    result.extend(generate_num_bambara(((d%1000)//100)*100, dict))
  if ((d%100)//10 > 0):
    if (result): result.append(dict['and'])
    result.extend(generate_num_bambara(((d%100)//10)*10, dict))
  if ((d%10) > 0):
    if (result): result.append(dict['and'])
    result.extend(generate_num_bambara(d%10, dict))
  return result


