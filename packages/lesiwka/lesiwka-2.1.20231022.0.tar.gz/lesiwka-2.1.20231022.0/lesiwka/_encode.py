import re

from .ascii import asciilator
from .diacritics import ACUTE
from .punctuation import APOSTROPHES, DELIMITERS

vowels_lower_cyr = "аеиіоу"
vowels_upper_cyr = vowels_lower_cyr.upper()
vowels_cyr = vowels_lower_cyr + vowels_upper_cyr

vowels_lower_lat = "aeyiou"
vowels_upper_lat = vowels_lower_lat.upper()
vowels_lat = vowels_lower_lat + vowels_upper_lat

iotted_lower_cyr = "єїюя"
iotted_upper_cyr = iotted_lower_cyr.upper()
iotted_cyr = iotted_lower_cyr + iotted_upper_cyr

iotted_lower_out = "еіуа"
iotted_upper_out = iotted_lower_out.upper()

iotted_lower_lat = "eiua"
iotted_upper_lat = iotted_lower_lat.upper()

iot_lower_cyr = "й"
iot_upper_cyr = iot_lower_cyr.upper()
iot_cyr = iot_lower_cyr + iot_upper_cyr

iot_lower_lat = "j"
iot_upper_lat = iot_lower_lat.upper()
iot_lat = iot_lower_lat + iot_upper_lat

consonants_lower_cyr = "бвдгґжзклмнпрстфхцчш"
consonants_upper_cyr = consonants_lower_cyr.upper()
consonants_cyr = consonants_lower_cyr + consonants_upper_cyr

consonants_lower_lat = "bvdhgžzklmnprstfxcčš"
consonants_upper_lat = consonants_lower_lat.upper()
consonants_lat = consonants_lower_lat + consonants_upper_lat

soft_sign_lower_cyr = "ь"
soft_sign_upper_cyr = soft_sign_lower_cyr.upper()
soft_sign_cyr = soft_sign_lower_cyr + soft_sign_upper_cyr

soft_sign_lat = ACUTE * 2

sqcq_lower_cyr = "щ"
sqcq_upper_cyr = sqcq_lower_cyr.upper()
sqcq_cyr = sqcq_lower_cyr + sqcq_upper_cyr

sqcq_lower_lat = "šč"
sqcq_upper_lat = sqcq_lower_lat.upper()

w_cyr = "вВ"
w_lat = "wW"

lower_cyr = (
    vowels_lower_cyr
    + iotted_lower_cyr
    + consonants_lower_cyr
    + iot_lower_cyr
    + soft_sign_lower_cyr
    + sqcq_lower_cyr
)
upper_cyr = (
    vowels_upper_cyr
    + iotted_upper_cyr
    + consonants_upper_cyr
    + iot_upper_cyr
    + soft_sign_upper_cyr
    + sqcq_upper_cyr
)
all_cyr = lower_cyr + upper_cyr

abbr = (
    ("ЄІБ", "JeIB"),
    ("ЄАВТ", "JeAVT"),
    ("ЄАЕС", "JeAES"),
    ("ЄАНТК", "JeANTK"),
    ("ЄАР", "JeAR"),
    ("ЄБА", "JeBA"),
    ("ЄБРР", "JeBRR"),
    ("ЄВС", "JeVS"),
    ("ЄГФ", "JeHF"),
    ("ЄДІ", "JeDI"),
    ("ЄДАПС", "JeDAPS"),
    ("ЄДЕБО", "JeDEBO"),
    ("ЄДКІ", "JeDKI"),
    ("ЄДР", "JeDR"),
    ("ЄДРПОУ", "JeDRPOU"),
    ("ЄЕК", "JeEK"),
    ("ЄЕП", "JeEP"),
    ("ЄЕС", "JeES"),
    ("ЄЕСУ", "JeESU"),
    ("ЄК", "JeK"),
    ("ЄКА", "JeKA"),
    ("ЄКВ", "JeKV"),
    ("ЄКП", "JeKP"),
    ("ЄКПЛ", "JeKPL"),
    ("ЄКРН", "JeKRN"),
    ("ЄНП", "JeNP"),
    ("ЄНР", "JeNR"),
    ("ЄОВС", "JeOVS"),
    ("ЄП", "JeP"),
    ("ЄПС", "JePS"),
    ("ЄР", "JeR"),
    ("ЄРДР", "JeRDR"),
    ("ЄРПН", "JeRPN"),
    ("ЄРЦ", "JeRC"),
    ("ЄС", "JeS"),
    ("ЄСВ", "JeSW"),
    ("ЄСВС", "JeSVS"),
    ("ЄСПЛ", "JeSPL"),
    ("ЄУ", "JeU"),
    ("ЄХБ", "JeXB"),
    ("ЄЦ", "JeC"),
    ("ЄЦБ", "JeCB"),
    ("АВМ", "AVM"),
    ("БДЮТ", "BDJuT"),
    ("БЮТ", "BJuT"),
    ("ВВ", "WV"),
    ("ВВІР", "VVIR"),
    ("ВВВ", "VVV"),
    ("ВВНЗ", "VVNZ"),
    ("ВВП", "VWP"),
    ("ВВР", "VVR"),
    ("ВГК", "VHK"),
    ("ВГСУ", "VHSU"),
    ("ВД", "VD"),
    ("ВДАІ", "VDAI"),
    ("ВДВ", "VDV"),
    ("ВДЕ", "VĐE"),
    ("ВДНГ", "VDNH"),
    ("ВДПУ", "VDPU"),
    ("ВЗ", "VZ"),
    ("ВЗУН", "VZUN"),
    ("ВК", "VK"),
    ("ВКВ", "VKV"),
    ("ВККС", "VKKS"),
    ("ВККСУ", "VKKSU"),
    ("ВКЛ", "VKL"),
    ("ВЛК", "VLK"),
    ("ВМД", "VMD"),
    ("ВМС", "VMS"),
    ("ВМСУ", "VMSU"),
    ("ВМФ", "VMF"),
    ("ВНАУ", "VNAU"),
    ("ВНЗ", "VNZ"),
    ("ВНО", "VNO"),
    ("ВНП", "VNP"),
    ("ВНТ", "VNT"),
    ("ВНТУ", "VNTU"),
    ("ВОІВ", "WOIW"),
    ("ВП", "VP"),
    ("ВПК", "VPK"),
    ("ВПЛ", "VPL"),
    ("ВПС", "VPS"),
    ("ВПУ", "VPU"),
    ("ВР", "VR"),
    ("ВРП", "VRP"),
    ("ВРУ", "VRU"),
    ("ВРХ", "VRX"),
    ("ВРЮ", "VRJu"),
    ("ВС", "VS"),
    ("ВСП", "VSP"),
    ("ВССУ", "VSSU"),
    ("ВСУ", "VSU"),
    ("ВТС", "VTS"),
    ("ВТССУМ", "VTSSUM"),
    ("ВУЦВК", "WUCVK"),
    ("ВЦА", "VCA"),
    ("ВЦВК", "WCVK"),
    ("ВЧ", "VČ"),
    ("ВШ", "VŠ"),
    ("ВЯП", "VJaP"),
    ("ГеВ", "HeV"),
    ("ДЄС", "DJeS"),
    ("ДБЖ", "ĐBŽ"),
    ("ДВЗ", "DWZ"),
    ("ДНЯЗ", "DNJaZ"),
    ("ДЮСШ", "DJuSŠ"),
    ("ДЮСШОР", "DJuSŠOR"),
    ("ДЮФЛ", "DJuFL"),
    ("ЗЄС", "ZJeS"),
    ("КДЮСШ", "KDJuSŠ"),
    ("КПВВ", "KPWV"),
    ("ЛЄ", "LJe"),
    ("МВС", "MWS"),
    ("МРЕВ", "MREV"),
    ("МеВ", "MeV"),
    ("НАЗЯВО", "NAZJaVO"),
    ("НБСЄ", "NBSJe"),
    ("НБУВ", "NBUV"),
    ("НУВГП", "NUVHP"),
    ("ОІЯД", "OIJaD"),
    ("ОАЄ", "OAJe"),
    ("ОБСЄ", "OBSJe"),
    ("ОВД", "OVD"),
    ("ОВК", "OVK"),
    ("ОВП", "OVP"),
    ("ОВТ", "OVT"),
    ("ОДЮСШ", "ODJuSŠ"),
    ("ПАРЄ", "PARJe"),
    ("ПВЗВТ", "PWZVT"),
    ("РЄ", "RJe"),
    ("РАВ", "RAV"),
    ("РВВС", "RVWS"),
    ("СЄПН", "SJePN"),
    ("СДЮШО", "SDJuŠO"),
    ("СДЮШОР", "SDJuŠOR"),
    ("СРЮ", "SRJu"),
    ("СТОВ", "STOV"),
    ("СФРЮ", "SFRJu"),
    ("ТОВ", "TOV"),
    ("ТЮГ", "TJuH"),
    ("ТеВ", "TeV"),
    ("ТзОВ", "TzOV"),
    ("УЄФА", "UJeFA"),
    ("УЄЦАВ", "UJeCAV"),
    ("УАВПП", "UAVPP"),
    ("УВВ", "UVV"),
    ("УВК", "UVK"),
    ("УВКБ", "UVKB"),
    ("УВКПЛ", "UVKPL"),
    ("УВП", "UVP"),
    ("УЦОЯО", "UCOJaO"),
    ("ХВЄ", "XVJe"),
    ("ХДАВП", "XDAVP"),
    ("ЦДЮТ", "CDJuT"),
    ("ЦОВВ", "COVW"),
    ("ЦПКіВ", "CPKiV"),
    ("ЦСЄ", "CSJe"),
    ("ЦСВЯП", "CSVJaP"),
    ("ЧЄ", "ČJe"),
    ("ЧСВВ", "ČSVV"),
    ("ЮВТ", "JuVT"),
    ("ЮНІДО", "JuNIDO"),
    ("ЮНІСЕФ", "JuNISEF"),
    ("ЮНЕП", "JuNEP"),
    ("ЮНЕСКО", "JuNESKO"),
    ("ЮНКТАД", "JuNKTAD"),
    ("ЮНОПС", "JuNOPS"),
    ("ЮНСІТРАЛ", "JuNSITRAL"),
    ("ЮРС", "JuRS"),
    ("ЮУАЕС", "JuUAES"),
    ("ЮФ", "JuF"),
    ("ЯМР", "JaMR"),
    ("еВ", "eV"),
    ("вт", "vt"),
    ("Вт", "Vt"),
    ("ВТ", "VT"),
    ("АВК", "AVK"),
    ("АВН", "AVN"),
    ("АВС", "AVS"),
    ("АСУВ", "ASUV"),
    ("БДЖ", "BĐŽ"),
    ("БЄК", "BJeK"),
    ("ВЯВ", "VJaV"),
    ("ДЗЗСЄ", "DZZSJe"),
    ("Дз", "Dz"),
    ("дз", "dz"),
    ("ДПРОВТ", "DPROVT"),
    ("ДРЖ", "ĐRŽ"),
    ("ЕВП", "EVP"),
    ("ЄАІС", "JeAIS"),
    ("ЄАМЗ", "JeAMZ"),
    ("ЄАСЗ", "JeASZ"),
    ("ЄАСК", "JeASK"),
    ("ЄАСУ", "JeASU"),
    ("ЄБК", "JeBK"),
    ("ЄКНС", "JeKNS"),
    ("ЄСВОН", "JeSVON"),
    ("ЄСКБ", "JeSKB"),
    ("ЄСКС", "JeSKS"),
    ("ЄССЗ", "JeCCZ"),
    ("ЄСУБ", "JeSUB"),
    ("ЗАВЗ", "ZAVZ"),
    ("ЗВОВС", "ZVOVS"),
    ("ЗВЯЗ", "ZVJaZ"),
    ("ЗЕРАВ", "ZERAV"),
    ("ІВ", "IV"),
    ("КЗАУВ", "KZAUV"),
    ("КІВ", "KIV"),
    ("МСЯС", "MSJaS"),
    ("ОВ", "OV"),
    ("ОВСТ", "OVST"),
    ("ОСУВ", "OSUV"),
    ("ОУВ", "OUV"),
    ("ОЯП", "OJaP"),
    ("ПСЯБ", "PSJaB"),
    ("ПУВ", "PUV"),
    ("РЯЗ", "RJaZ"),
    ("РЯН", "RJaN"),
    ("РЯО", "RJaO"),
    ("СУВ", "SUV"),
    ("СЯС", "SJaS"),
    ("УВ", "UV"),
    ("УВС", "UVS"),
    ("УВФ", "UVF"),
    ("ХДС", "XĐS"),
    ("ЯБВ", "JaBV"),
    ("ЯБП", "JaBP"),
    ("ЯБЧ", "JaBČ"),
    ("ЯВ", "JaV"),
    ("ЯЕУ", "JaEU"),
    ("ЯЗ", "JaZ"),
    ("ЯЗК", "JaZK"),
    ("ЯМ", "JaM"),
    ("ЯРМД", "JaRMD"),
    ("ЯРР", "JaRR"),
    ("ЯРСД", "JaRSD"),
    ("ЯФ", "JaF"),
)
abbr_dot_pattern = (
    r"(?i:(?<=\b)|(?<=\b(г|з|і|к|с))|(?<=\b(ди|за|ін|по|св))|"
    r"(?<=\b(про|сло))|(?<=\b(буль|пере|родо))){0}(?=\.)"
)

w_pattern = (
    r"((?<=\b)|(?<=[_%s])){0}((?=[%s])|(?=[%s])|(?=\W*$)|"
    r"(?=\W*[%s](?:\W|$))|(?=\W+[%s]))"
    % (
        vowels_cyr + iotted_cyr + w_cyr,
        consonants_cyr + iot_cyr + sqcq_cyr + w_lat,
        APOSTROPHES,
        DELIMITERS,
        consonants_cyr
        + iot_cyr
        + sqcq_cyr
        + iotted_cyr
        + consonants_lat
        + iot_lat,
    )
)

capital_pattern = r"(?<=[%s]){0}(?=\W*$)"
sqcq_capital_pattern = capital_pattern % upper_cyr
iotted_capital_pattern = capital_pattern % (
    vowels_upper_cyr + iotted_upper_cyr
)

apostrophe_pattern = r"(?<=[%s])[%s]{0}" % (all_cyr + w_lat, APOSTROPHES)
iotted_pattern = r"((?<=\b)|(?<=[%s])){0}" % (vowels_cyr + iotted_cyr)
ending_pattern = r"(?=[%s]|\W+[%s]|\W*$)" % (
    lower_cyr + "w",
    lower_cyr + vowels_lat + consonants_lat + iot_lat + w_lat,
)
acuted_pattern = r"(?<=[%s]){0}" % (consonants_cyr + sqcq_cyr)

affricate_exclude_patterns = (
    r"(?i:(?<=ме)){0}(?i:((?=заклад)|(?=захис)))",
    r"(?i:(?<=\bро)){0}(?i:(?=зал))",
    (
        r"(?i:((?<=\bбу)|(?<=\bзагоро)|(?<=\bме)|(?<=\bпро)|(?<=\bсту)))"
        r"{0}(?i:(?=заг[іо]н))"
    ),
    r"(?i:((?<=\bвищеві)|(?<=\bкінові)|(?<=\bлітві)|(?<=\bра)|(?<=\bспецві)))"
    r"{0}(?i:(?=зна[кч]))",
    r"(?i:(?<=епі)){0}(?i:(?=зах[іо]д))",
    r"(?i:(?<=пі)){0}(?i:(?=жи[вw]))",
    r"(?<=\b){0}(?i:(?=зо[cт]))",
)
affricate_pattern_1 = r"(?i:(?<=\bпере)){0}(?i:з)(?i:(?=вен|він|вон|ижч))"
affricate_pattern_2 = (
    r"(?i:(?!(?<=\bві)|(?<=\bна)|(?<=\bо)|(?<=\bпере)|(?<=\bпі)|(?<=\bпона)|"
    r"(?<=\bпопі)|(?<=\bпре)|(?<=\bсере)|(?<=\bневі)|(?<=\bнепі)|(?<=\bнапере)"
    r"|(?<=\bопі))){0}"
)

patterns = ()
patterns += (
    (abbr_dot_pattern.format("в"), "v"),
    (abbr_dot_pattern.format("В"), "V"),
)
patterns += tuple((r"\b{0}\b".format(cyr), lat) for cyr, lat in abbr)

patterns += ((sqcq_capital_pattern.format(sqcq_upper_cyr), sqcq_upper_lat),)
patterns += tuple(
    (iotted_capital_pattern.format(cyr), iot_upper_cyr + out)
    for cyr, out in zip(iotted_upper_cyr, iotted_upper_out)
)

patterns += tuple(
    (w_pattern.format(cyr), lat) for cyr, lat in zip(w_cyr, w_lat)
)

patterns += ((sqcq_upper_cyr + ending_pattern, sqcq_lower_lat.title()),)

patterns += tuple(
    (apostrophe_pattern.format(cyr), iot_lower_cyr + out)
    for cyr, out in zip(iotted_lower_cyr, iotted_lower_out)
)
patterns += tuple(
    (apostrophe_pattern.format(cyr) + ending_pattern, iot_upper_cyr + out)
    for cyr, out in zip(iotted_upper_cyr, iotted_lower_out)
)
patterns += tuple(
    (apostrophe_pattern.format(cyr), iot_upper_cyr + out)
    for cyr, out in zip(iotted_upper_cyr, iotted_upper_out)
)

patterns += tuple(
    (iotted_pattern.format(cyr) + ending_pattern, iot_upper_cyr + out)
    for cyr, out in zip(iotted_upper_cyr, iotted_lower_out)
)

patterns += tuple(
    (acuted_pattern.format(cyr), ACUTE + out)
    for cyr, out in zip(iotted_lower_cyr, iotted_lower_out)
)
patterns += tuple(
    (acuted_pattern.format(cyr), ACUTE + out)
    for cyr, out in zip(iotted_upper_cyr, iotted_upper_out)
)

patterns += tuple(
    (pattern.format("д"), "d") for pattern in affricate_exclude_patterns
)
patterns += tuple(
    (pattern.format("Д"), "D") for pattern in affricate_exclude_patterns
)
patterns += (
    (affricate_pattern_1.format("д"), "ƶ"),
    (affricate_pattern_1.format("Д"), "Ƶ"),
)
patterns += (
    (affricate_pattern_2.format("дж"), "đ"),
    (affricate_pattern_2.format("Дж"), "Đ"),
    (affricate_pattern_2.format("дз"), "ƶ"),
    (affricate_pattern_2.format("Дз"), "Ƶ"),
)

table = dict(
    zip(
        vowels_cyr + consonants_cyr + iot_cyr + soft_sign_cyr,
        vowels_lat + consonants_lat + iot_lat + soft_sign_lat,
    )
)
table.update(
    {
        cyr: iot_lower_lat + lat
        for cyr, lat in zip(iotted_lower_cyr, iotted_lower_lat)
    }
)
table.update(
    {
        cyr: iot_upper_lat + lat
        for cyr, lat in zip(iotted_upper_cyr, iotted_upper_lat)
    }
)
table[sqcq_lower_cyr] = sqcq_lower_lat
table[sqcq_upper_cyr] = sqcq_upper_lat
table = str.maketrans(table)


def pre_validate(text):
    return re.search("[ґєіїҐЄІЇ]", text) or not re.search("[ёўъыэЁЎЪЫЭ]", text)


def encode(text, no_diacritics=False):
    if not pre_validate(text):
        return text

    result = text

    for pattern, repl in patterns:
        result = re.sub(pattern, repl, result)

    result = result.translate(table)

    if no_diacritics:
        result = asciilator(result)

    return result
