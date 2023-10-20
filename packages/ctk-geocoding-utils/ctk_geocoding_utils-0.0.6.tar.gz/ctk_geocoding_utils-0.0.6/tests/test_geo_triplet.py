import pytest
from data_geocoding_utils.shaping_rules import (advanced_city_shaping,
                                                    basic_city_shaping,
                                                    shape_postal_code)


class ShapePostalCodeTester():
    def __init__(self, true_duo, acceptable_postal_codes, unacceptable_postal_codes) -> None:
        self.true_duo = true_duo
        self.acceptable_postal_codes = acceptable_postal_codes
        self.unacceptable_postal_codes = unacceptable_postal_codes

    def test_positive_examples(self):
        for pcode in self.acceptable_postal_codes:
            print(shape_postal_code(*(pcode, self.true_duo['country_code'])))
            shaped_duo = {'postal_code': shape_postal_code(*(pcode, self.true_duo['country_code'])),
                          'country_code': self.true_duo['country_code']}
        assert shaped_duo == self.true_duo

    def test_negative_examples(self):
        for pcode in self.unacceptable_postal_codes:
            shaped_duo = {'postal_code': shape_postal_code(*(pcode, self.true_duo['country_code'])),
                          'country_code': self.true_duo['country_code']}
        assert not (shaped_duo == self.true_duo)


def test_shape_postal_code_cz():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "286 01",
                  "country_code": "CZ"},
        acceptable_postal_codes=['286 01', '28601', '286-01', '28 601'],
        unacceptable_postal_codes=['286 001', 'A601', '', '28'])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_gb():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "WR10",
                  "country_code": "GB"},
        acceptable_postal_codes=['WR10', 'WR10 2NR', 'WR10-2NR'],
        unacceptable_postal_codes=['2NR', 'WCR10', ''])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_ie():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "F12",
                  "country_code": "IE"},
        acceptable_postal_codes=['F12', 'F12 R6Y5', 'F12R6Y5'],
        unacceptable_postal_codes=['12F', 'R6Y5', ''])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_lu():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "L-5401",
                  "country_code": "LU"},
        acceptable_postal_codes=['L-5401', '5401', 'L5401'],
        unacceptable_postal_codes=['L540', '5401L', ''])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_lv():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "LV-4647",
                  "country_code": "LV"},
        acceptable_postal_codes=['LV-4647', '4647', 'LV4647'],
        unacceptable_postal_codes=['L4647', 'V4647', ''])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_md():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "MD-7311",
                  "country_code": "MD"},
        acceptable_postal_codes=['MD-73117', '7311', 'MD7311'],
        unacceptable_postal_codes=['M7311', 'D7311', ''])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_nl():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "6941",
                  "country_code": "NL"},
        acceptable_postal_codes=['6941', '6941 XL', '6941JW', '6941-GD'],
        unacceptable_postal_codes=['XL6941', 'J6941W', '', 'GD-6941'])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_pl():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "05-310",
                  "country_code": "PL"},
        acceptable_postal_codes=['05-310', '05 310', '05310'],
        unacceptable_postal_codes=['POL05310', 'P05-310', ''])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_pt():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "3740-171",
                  "country_code": "PT"},
        acceptable_postal_codes=['3740-171', '3740 171', '3740171'],
        unacceptable_postal_codes=['3740', '171', ''])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_se():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "822 30",
                  "country_code": "SE"},
        acceptable_postal_codes=['822 30', '82230', '822-30'],
        unacceptable_postal_codes=['822', '30', ''])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_shape_postal_code_sk():
    tester = ShapePostalCodeTester(
        true_duo={"postal_code": "956 12",
                  "country_code": "SK"},
        acceptable_postal_codes=['956 12', '95612', '956-12'],
        unacceptable_postal_codes=['956', '12', ''])

    tester.test_positive_examples()
    tester.test_negative_examples()


def test_basic_city_shaping():
    ines_cities = ['SANT GREGORI', 'AVENCHES',
                   'ETRETAT', 'PLAN LES OUATES', 'PARIS', 'LYON']
    db_cities = ['Sant Gregori (Municipio)', 'Avenches',
                 'Étretat', 'Plan-les-Ouates', 'Paris 12', 'Lyon ']
    for tc, uc in zip(ines_cities, db_cities):
        assert (basic_city_shaping(tc) == basic_city_shaping(uc))


def test_advanced_city_shaping_at():
    cc_alpha2 = 'AT'
    ines_cities = ['HOFSTAETTEN AN DER RAAB', 'GROEDIG', 'MUENCHENDORF', 'GROSSPETERSDORF',
                   'ST GEORGEN BEI GRIESKIRCHEN', 'GROSS ST FLORIAN', 'ST VALENTIN', 'NEUDORF']

    db_cities = ['Hofstätten an der Raab', 'Grödig', 'Münchendorf', 'Großpetersdorf',
                 'Sankt Georgen bei Grieskirchen', 'Groß Sankt Florian', 'St. Valentin', 'Neudorf / Novo Selo']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_be():
    cc_alpha2 = 'BE'
    ines_cities = ['ST GERARD', 'ST. AMAND', 'STE ODE', 'STE. CECILE', 'HAINE ST PAUL',
                   'COURT ST. ETIENNE', 'BERCHEM STE AGATHE', 'LAVAUX STE. ANNE']
    db_cities = ['Saint-Gérard', 'Saint-Amand', 'Sainte-Ode', 'Sainte-Cécile',
                 'Haine-Saint-Paul', 'Court-Saint-Etienne', 'Berchem-Sainte-Agathe', 'Lavaux-Sainte-Anne']
    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_bg():
    cc_alpha2 = 'BG'
    ines_cities = ['LOM']

    db_cities = ['Лом / Lom']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_by():
    cc_alpha2 = 'BY'
    ines_cities = ['MINSK', 'NOVYY DVOR']

    db_cities = ['Минск', 'Новый Двор']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_ch():
    cc_alpha2 = 'CH'
    ines_cities = ['ST PREX', 'ST. AUBIN SAUGES', 'STE CROIX', 'STE. CROIX',
                   'CHATEL ST DENIS', 'CHEZARD ST. MARTIN', 'VILLARS STE CROIX', 'VILLARS STE. CROIX',
                   'RENENS', 'BIEL 3']

    db_cities = ['Saint-Prex', 'Saint-Aubin-Sauges', 'Sainte-Croix', 'Sainte-Croix',
                 'Châtel-Saint-Denis', 'Chézard-Saint-Martin', 'Villars-Sainte-Croix', 'Villars-Sainte-Croix',
                 'Renens VD', 'Biel/Bienne']
    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_de():
    cc_alpha2 = 'DE'
    ines_cities = ['SCHWAEBISCH GMUEND', 'LEMFOERDE', 'GROSSRAESCHEN',
                   'ST INGBERT', 'ST. GOARSHAUSEN', 'NEUKIRCH', 'BRETNIG', 'CHEMNITZ']

    db_cities = ['Schwäbisch Gmünd', 'Lemförde', 'Großräschen', 'Sankt Ingbert',
                 'Sankt Goarshausen', 'Neukirch/Lausitz', 'Bretnig-Hauswalde', 'Chemnitz, Sachsen']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_dk():
    cc_alpha2 = 'DK'
    ines_cities = ['RYOMGAARD', 'KOBENHAVN O', 'VALLENSBAEK', 'FREDERIKSBERG']

    db_cities = ['Ryomgård', 'København Ø', 'Vallensbæk', 'Frederiksberg C']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_es():
    cc_alpha2 = 'ES'
    ines_cities = ['QUINTANILLA DE ARRIBA', 'VILAFRANCA DEL PENEDES	', 'QUINTANILLA DE LA MATA', 'CADALSO DE LOS VIDRIOS',
                   'FRESNILLO DE LAS DUEÑAS', 'SAN JERONIMO LOS PERALES', 'PUENTE LA REINA', 'ALHAURIN EL GRANDE', 'BARRIO']

    db_cities = ['Quintanilla De Arriba', 'Vilafranca Del Penedes', 'Quintanilla De La Mata', 'Cadalso De Los Vidrios',
                 'Fresnillo De Las Dueñas', 'San Jeronimo Perales', 'Puente La Reina/Gares', 'Alhaurin El Grande', 'Barrio, El (Mieres)']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_fi():
    cc_alpha2 = 'FI'
    ines_cities = ['HALIKKO']

    db_cities = ['Halikko As']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_fr():
    cc_alpha2 = 'FR'
    ines_cities = ['ST DESIRAT', 'ST. NAZAIRE', 'STE MARGUERITE', 'STE. SAVINE',
                   'TRITH ST LEGER', 'AUBIN ST. VAAST', 'PONT STE MARIE', 'RILLY STE SYRE']

    db_cities = ['Saint-Désirat', 'Saint-Nazaire', 'Sainte-Marguerite', 'Sainte-Savine',
                 'Trith-Saint-Léger', 'Aubin-Saint-Vaast', 'Pont-Sainte-Marie', 'Rilly-Sainte-Syre']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_lt():
    cc_alpha2 = 'LT'
    ines_cities = ['SAUKENAI', 'KAZOKISKIU']

    db_cities = ['Šaukėnai', 'Kazokiškių k.']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_no():
    cc_alpha2 = 'NO'
    ines_cities = ['TROMSO', 'HAERLAND', 'KRISTIANSUND']

    db_cities = ['Tromsø', 'Hærland', 'Kristiansund N']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_pl():
    cc_alpha2 = 'PL'
    ines_cities = ['BUDZYN']

    db_cities = ['Budzyń']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_rs():
    cc_alpha2 = 'RS'
    ines_cities = ['SURCIN']

    db_cities = ['Surčin']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_se():
    cc_alpha2 = 'SE'
    ines_cities = ['BORLAENGE', 'GOETEBORG', 'KAALLERED']

    db_cities = ['Borlänge', 'Göteborg', 'Kållered']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_si():
    cc_alpha2 = 'SI'
    ines_cities = ['AJDOVSCINA', 'IZOLA', 'CELJE']

    db_cities = ['Ajdovščina', 'Izola/Isola', 'Celje - dostava']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))


def test_advanced_city_shaping_ua():
    cc_alpha2 = 'UA'
    ines_cities = ['UMAN', 'MYKOLAYIV']

    db_cities = ['Умань', 'Миколаїв (Миколаїв)']

    for tc, uc in zip(ines_cities, db_cities):
        assert (advanced_city_shaping(tc, cc_alpha2) ==
                advanced_city_shaping(uc, cc_alpha2))
