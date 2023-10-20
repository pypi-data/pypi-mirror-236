import re
import unicodedata

from iso3166 import countries_by_alpha3
from unidecode import unidecode

alpha3_to_alpha2_map = {
    k: countries_by_alpha3[k].alpha2 for k in countries_by_alpha3.keys()}
alpha3_to_alpha2_map['ROM'] = 'RO'
alpha3_to_alpha2_map['KOS'] = 'XK'


def remove_spaces_and_symbols(s):
    return ''.join(e for e in s if e.isalnum())


def replace_symbols_with_spaces(s):
    return re.sub(' +', ' ', ''.join(e if e.isalnum() else ' ' for e in s))


def strip_accents(s):
   return (''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


def shape_postal_code(pcode, cc_alpha2):

    light_pcode = remove_spaces_and_symbols(pcode)

    if cc_alpha2 == 'CZ':
        if bool(re.compile(r'[0-9]{5}$').match(light_pcode)):
            pcode = light_pcode[:3] + ' ' + light_pcode[3:]

    elif cc_alpha2 == 'GB':
        match = re.compile(
            r'([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA)').match(pcode)
        if bool(match):
            pcode = match.group(0)

    elif cc_alpha2 == 'IE':
        if bool(re.compile(r'[A-Z]{1}[0-9]{2}').match(light_pcode)):
            pcode = light_pcode[:3]

    elif cc_alpha2 == 'LU':
        if bool(re.compile(r'L?[0-9]{4}$').match(light_pcode)):
            pcode = 'L-' + light_pcode[-4:]

    elif cc_alpha2 == 'LV':
        if bool(re.compile(r'(LV)?[0-9]{4}$').match(light_pcode)):
            pcode = 'LV-' + light_pcode[-4:]

    elif cc_alpha2 == 'MD':
        if bool(re.compile(r'(MD)?[0-9]{4}$').match(light_pcode)):
            pcode = 'MD-' + light_pcode[-4:]

    elif cc_alpha2 == 'NL':
        if bool(re.compile(r'[0-9]{4}').match(light_pcode)):
            pcode = light_pcode[:4]

    elif cc_alpha2 == 'PL':
        if bool(re.compile(r'[0-9]{5}$').match(light_pcode)):
            pcode = light_pcode[:2] + '-' + light_pcode[2:]

    elif cc_alpha2 == 'PT':
        if bool(re.compile(r'[0-9]{7}$').match(light_pcode)):
            pcode = light_pcode[:4] + '-' + light_pcode[4:]

    elif cc_alpha2 == 'SE':
        if bool(re.compile(r'[0-9]{5}$').match(light_pcode)):
            pcode = light_pcode[:3] + ' ' + light_pcode[3:]

    elif cc_alpha2 == 'SK':
        if bool(re.compile(r'[0-9]{5}$').match(light_pcode)):
            pcode = light_pcode[:3] + ' ' + light_pcode[3:]

    return pcode


def basic_city_shaping(city):
    # basic shaping
    output_city = city
    output_city = re.sub("[\(\[].*?[\)\]]", "", output_city)
    output_city = output_city.lower()
    output_city = strip_accents(output_city)
    output_city = replace_symbols_with_spaces(output_city)
    output_city = ''.join([i for i in output_city if not i.isdigit()])
    output_city = output_city.strip()
    return output_city

def fra_language_city_shaping(city):
    output_city = city
    output_city = output_city.replace(' ste ', ' sainte ')
    output_city = output_city.replace(' st. ', ' saint ')
    output_city = output_city.replace(' st ', ' saint ')
    output_city = output_city.replace(' ste. ', ' sainte ')

    if output_city.startswith('st '):
        output_city = 'saint ' + output_city[len('st '):]
    elif output_city.startswith('st. '):
        output_city = 'saint ' + output_city[len('st. '):]
    elif output_city.startswith('ste '):
        output_city = 'sainte ' + output_city[len('ste '):]
    elif output_city.startswith('ste. '):
        output_city = 'sainte ' + output_city[len('ste. '):]
    return output_city

def ger_language_city_shaping(city):
    output_city = city
    output_city = output_city.replace('ä', 'ae')
    output_city = output_city.replace('ö', 'oe')
    output_city = output_city.replace('ü', 'ue')
    output_city = output_city.replace('ß', 'ss')
    output_city = output_city.replace(' st ', ' sankt ')
    output_city = output_city.replace(' st. ', ' sankt ')
    if output_city.startswith('st '):
        output_city = 'sankt ' + output_city[len('st '):]
    elif output_city.startswith('st. '):
        output_city = 'sankt ' + output_city[len('st. '):]
    return output_city

def handle_special_characters_city_shaping(city, cc_alpha2):
    output_city = city
    if cc_alpha2 in ['SE']:
        output_city = output_city.replace('ä', 'ae')
        output_city = output_city.replace('ö', 'oe')

    if cc_alpha2 in ['DK', 'SE']:
        output_city = output_city.replace('å', 'aa')

    if cc_alpha2 in ['DK', 'NO']:
        output_city = output_city.replace('ø', 'o')

    if cc_alpha2 in ['DK', 'NO']:
        output_city = output_city.replace('æ', 'ae')

    if cc_alpha2 in ['BY', 'LT', 'PL', 'RS', 'SI', 'UA']:
        output_city = unidecode(output_city)

    if cc_alpha2 in ['BY', 'PL', 'UA']:
        output_city = output_city.replace('y', 'i')
    return output_city

def handle_stop_words_city_shaping(city, cc_alpha2):
    output_city = city
    if cc_alpha2 in ['NO']:
        output_city = ' '.join([w for w in output_city.split() if len(w) > 1])

    if cc_alpha2 in ['CH', 'DK', 'FI']:
        output_city = ' '.join([w for w in output_city.split() if len(w) > 2])

    if cc_alpha2 in ['LT']:
        output_city = output_city.replace('k.', '')

    if cc_alpha2 in ['ES']:
        output_city = output_city.replace(' de ', ' ')
        output_city = output_city.replace(' del ', ' ')
        output_city = output_city.replace(' de la ', ' ')
        output_city = output_city.replace(' de los ', ' ')
        output_city = output_city.replace(' de las ', ' ')

        output_city = output_city.replace(' los ', ' ')
        output_city = output_city[output_city.startswith(
            'los ') and len('los '):]
        output_city = output_city.replace(' las ', ' ')
        output_city = output_city[output_city.startswith(
            'las ') and len('las '):]
        output_city = output_city.replace(' la ', ' ')
        output_city = output_city[output_city.startswith(
            'la ') and len('la '):]
        output_city = output_city.replace(' el ', ' ')
        output_city = output_city[output_city.startswith(
            'el ') and len('el '):]
    return output_city

def handle_splits_city_shaping(city, cc_alpha2):
    output_city = city
    if cc_alpha2 in ['AT', 'CH', 'DE', 'ES', 'SI']:
        output_city = output_city.split(sep='/')[0]

    if cc_alpha2 in ['BG']:
        output_city = output_city.split(sep='/')[-1]

    if cc_alpha2 in ['DE', 'SI']:
        output_city = output_city.split(sep='-')[0]

    if cc_alpha2 in ['DE', 'ES']:
        output_city = output_city.split(sep=',')[0]
    return output_city

def advanced_city_shaping(city, cc_alpha2):
    output_city = city.lower()

    # Language specificities #

    if cc_alpha2 in ['BE', 'FR', 'CH']:
        output_city = fra_language_city_shaping(output_city)

    ## DE ##
    if cc_alpha2 in ['AT', 'DE']:
        output_city = ger_language_city_shaping(output_city)

    # Special characters #
    output_city = handle_special_characters_city_shaping(output_city, cc_alpha2)

    # Stop words and co. #
    output_city = handle_stop_words_city_shaping(output_city, cc_alpha2)

    # Splits #
    output_city = handle_splits_city_shaping(output_city, cc_alpha2)
    
    return basic_city_shaping(output_city)
