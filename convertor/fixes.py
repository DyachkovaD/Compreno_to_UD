# -*- coding: utf-8 -*-

import csv
import re

def imp_and_perf(lemma, feats) -> str:
    """
    Меняет леммы совершенного вида на несовершенный
    у токенов несовершенного вида.
    """
    dict_of_aspect_pairs = {}

    with open('D:\Compreno\SEMarkup_project\compreno2UD\morphology\ImpToPerf.txt', 'r', encoding='utf8') as perfect_txt:
        for line in perfect_txt:
            imp, pf = line.strip('\n').split('\t')
            dict_of_aspect_pairs[pf] = imp
    if 'Aspect' in feats:
        if lemma in dict_of_aspect_pairs and feats['Aspect'] == 'Imperfective':
            lemma = dict_of_aspect_pairs[lemma]

    perfect_txt.close()

    return lemma


def check_verb_lemmas(lemma, pos):
    """
    Возвращает список лемм, которых нет в
    списке на конвертацию из совершенного в несовершенный вид.
    """
    absent_verbs = []

    with open('D:\Compreno\SEMarkup_project\compreno2UD\morphology\ImpToPerf.txt', 'r', encoding='utf8') as perfect_txt:
        l = list(perfect_txt)
        verb_list = []
        for line in l:
            new = line.strip('\n').split('\t')
            for i in new:
                verb_list.append(i)

        if pos == 'Verb' and lemma not in verb_list:
            absent_verbs.append(lemma)

    return absent_verbs

def fix_lemmas(token, lemma, feats) -> str:
    """
    Изменяет некорректные леммы.
    """

    # 'SpecialLexemes': 'Lex_KgSm'
    kg_sm_set = {'м': 'метр',
                 'тыс.': 'тысяча',
                 'млн.': 'миллион',
                 'млн': "миллион",
                 'с': "секунда",
                 'кг': "килограмм",
                 'км.': "километр",
                 'км': "километр",
                 'долл.': "доллар",
                 'долл': "доллар",
                 'т': "тонна",
                 'кв': "квадратный",
                 'сек.': "секунда",
                 'обл.': "область",
                 'млрд': "миллиард",
                 'млрд.': "миллиард",
                 'см': "сантиметр",
                 'руб': "рубль",
                 'бул.': "бульвар",
                 'буль.': "бульвар",
                 'Гб': "гигобайт",
                 'Мб' : "мегобайт",
                 'Тб' : "теробайт",
                 'ГВт': "гигаватт",
                 'ГГц': "гигагерц",
                 'ГДж': "гигаджоуль",
                 'ул.': "улица"}
    hash_lemma_set = {'#Acronym',
                      '#AngleBrackets',
                      '#BoxBracketsProperName',
                      '#BracketedProperName',
                      '#CommaDash',
                      '#CommaForDirectSpeech',
                      '#Cue',
                      '#DashColonForQuotation',
                      '#DashCommaForQuotation',
                      '#DashFullStopForQuotation',
                      '#ElliptedAdjective',
                      '#ElliptedNoun',
                      '#ElliptedNumeral',
                      '#ElliptedPseudoNumeral',
                      '#ElliptedVerb',
                      '#EmergencyGap',
                      '#Enumeration',
                      '#ExclamationSentence',
                      '#Expression',
                      '#ForeignWord',
                      '#FormattedProperName',
                      '#IgnorableBrackets',
                      '#NormalForPostpositionalDeclarativeQuotation',
                      '#NormalNotSentenceParenthetic',
                      '#NormalSentence',
                      '#NormalSentenceWithDots',
                      '#Number',
                      '#ParagraphForCue',
                      '#PhoneNumber',
                      '#QuestionExclamationSentence',
                      '#QuestionSentence',
                      '#Quotation',
                      '#QuotationWithComma',
                      '#QuotationWithStop',
                      '#Reference',
                      '#Reporting_AfterMarkedEnd',
                      '#Reporting_Colon',
                      '#Reporting_Comma',
                      '#Reporting_FullStop',
                      '#RomanNumber',
                      '#Sentence_IntroducingDirectSpeech',
                      '#SentenceWithBracketBoundaries',
                      '#SentenceWithReport',
                      '#TemplateExpression',
                      '#UnbracketedProperName',
                      '#UnknownName',
                      '#UnknownWord',
                      '#URL',
                      '#Субстантиватор'}

    if lemma in hash_lemma_set:
        lemma = token
    if lemma == 'считывать': #очень неприятный костыль для глагола в случаях: "он считает, что сделал правильно"
        lemma = 'считать'
    if token.lower() == 'они':
        lemma = 'они'
    elif token.lower() == 'оно':
        lemma = 'оно'
    elif token.lower() == 'она':
        lemma = 'она'

    if lemma in kg_sm_set and 'SpecialLexemes' in feats and feats['SpecialLexemes'] == 'Lex_KgSm':
        lemma = kg_sm_set[lemma]

    return lemma

def indexation_bounded_csv(sent, csv_dict, bounded_token_list):
    """
    Разделяет токены, которые есть в доке csv, состоящие из нескольких токенов.
    Меняет индексацию.
    """

    for word in sent:
        divided_words = []
        c = 0
        if word['token'].lower() in bounded_token_list:
            for token in csv_dict.items():
                if token[0].startswith(word['token'].lower()) and word['pos'] in token[0]:
                    for part in token[1]:
                        if part['head'] != '_':
                            head = int(part['head'])
                        else:
                            head = word['head']
                        new_word = {'id': word['id'] + c, 'token': part['token'], 'lemma': part['lemma'].lower(),
                                    'pos': part['pos'], 'feats': part['feats'], 'dep': part['dep'], 'head': head,
                                    'label': '_', 'semrel': '__'}

                        if new_word['head'] != 0:
                            new_word['head'] = new_word['id'] - new_word['head']
                        else:
                            new_word['head'] = word['head']
                            new_word['label'] = new_word['label']
                            new_word['semrel'] = word['semrel']
                        if new_word['id'] == 1:
                            new_word['token'] = new_word['token'].title()
                        c += 1
                        divided_words.append(new_word)
                    if word['token'].lower() in ('больше, чем', 'более, чем'):
                        for word in sent:
                            if word['head'] == 0:
                                b_head = word['id']
                        divided_words[0]['head'] = b_head
                        divided_words[1]['head'] = word['head']
                        divided_words[2]['head'] = word['head']

                    dic = {k: k for k in range(1, len(sent))}
                    start = sent.index(word)
                    for i in divided_words:
                        sent.insert(start, i)
                        start += 1
                    stop = sent.index(word)
                    sent.remove(word)
                    for old_word in sent[stop:]:
                        old_word['id'] += len(divided_words) - 1
                    count = 1
                    for i in range(len(sent)):
                        if sent[i]['semrel'] == '__':
                            continue
                        else:
                            dic[count] = sent[i]['id']
                            count += 1
                    for i in range(len(sent)):
                        if sent[i]['semrel'] == '__':
                            sent[i]['semrel'] = '_'
                            continue
                        else:
                            for item in dic:
                                if sent[i]['head'] == item:
                                    sent[i]['head'] = dic[item]
                                    break
                    break


def bounded_foreign(sent):
    """
    Разделяет иностранные слова, состоящие из нескольких токенов.
    Разделяет токены типа: 1990-1991
    """

    foreign_bounded_token = re.compile(r'[A-za-z]+ [A-za-z]+')
    number_bounded = re.compile(r'\d+,?\d*?-\d+,?\d*?')
    divided_words = []
    c = 0
    for word in sent:
        divided_words = []
        c = 0
        if foreign_bounded_token.search(word['token']):
            f_parts = word['token'].split()
            first_token_id = word['id'] + c
            new_word = {'id': first_token_id, 'token': f_parts[0], 'lemma': f_parts[0], 'pos': 'X', 'feats': 'Foreign=Yes',
                        'dep': word['dep'], 'head': word['head'], 'label': word['label'], 'semrel': word['semrel']}
            divided_words.append(new_word)
            c += 1
            for f_part in f_parts[1:]:
                new_word = {'id': word['id'] + c, 'token': f_part, 'lemma': f_part, 'pos': '__', 'feats': 'Foreign=Yes',
                            'dep': 'flat:foreign', 'head': first_token_id, 'label': '_', 'semrel': word['semrel']}
                c += 1
                divided_words.append(new_word)

            dic = {k: k for k in range(1, len(sent))}
            start = sent.index(word)
            for i in divided_words:
                sent.insert(start, i)
                start += 1
            stop = sent.index(word)
            sent.remove(word)
            for old_word in sent[stop:]:
                old_word['id'] += len(divided_words) - 1
            count = 1
            for i in range(len(sent)):
                if sent[i]['pos'] == '__':
                    continue
                else:
                    dic[count] = sent[i]['id']
                    count += 1
            for i in range(len(sent)):
                if sent[i]['pos'] == '__':
                    if new_word['token'] in ('%', '$', '°', '€', '+', '№', '#', '@', '~', '^', '&'):
                        new_word['pos'] = 'SYM'
                    else:
                        sent[i]['pos'] = 'X'
                    continue
                else:
                    for item in dic:
                        if sent[i]['head'] == item:
                            sent[i]['head'] = dic[item]
                            break
        elif number_bounded.fullmatch(word['token']) and word['pos'] in ('ADJ', 'NUM') and word['label'] != 'Specification':
                parts = re.compile(r'(\d+,?\d*?)(-)(\d+,?\d*?)').findall(word['token'])
                first_token_id = word['id'] + c
                new_word = {'id': first_token_id, 'token': parts[0][0], 'lemma': parts[0][0], 'pos': word['pos'], 'feats': word['feats'],
                            'head': word['head'], 'dep': word['dep'], 'label': word['label'], 'semrel': word['semrel']}
                c += 1
                divided_words.append(new_word)
                new_word = {'id': word['id'] + c, 'token': parts[0][1], 'lemma': parts[0][1], 'pos': '__', 'feats': '_',
                            'head': first_token_id + 2, 'dep': 'punct', 'label': '_', 'semrel': 'punct'}
                c += 1
                divided_words.append(new_word)
                new_word = {'id': word['id'] + c, 'token': parts[0][2], 'lemma': parts[0][2], 'pos': '__', 'feats': word['feats'],
                            'head': first_token_id, 'dep': word['dep'], 'label': word['label'], 'semrel': word['semrel']}
                c += 1
                divided_words.append(new_word)

                dic = {k: k for k in range(1, len(sent))}
                start = sent.index(word)
                for i in divided_words:
                    sent.insert(start, i)
                    start += 1
                stop = sent.index(word)
                sent.remove(word)
                for old_word in sent[stop:]:
                    old_word['id'] += len(divided_words) - 1
                count = 1
                for i in range(len(sent)):
                    if sent[i]['pos'] == '__':
                        continue
                    else:
                        dic[count] = sent[i]['id']
                        count += 1
                for i in range(len(sent)):
                    if sent[i]['pos'] == '__':
                        if sent[i]['dep'] == 'punct':
                            sent[i]['pos'] = 'PUNCT'
                        else:
                            sent[i]['pos'] = word['pos']
                        continue
                    else:
                        for item in dic:
                            if sent[i]['head'] == item:
                                sent[i]['head'] = dic[item]
                                break

def merge(sent):
    """
    Сливает токены
    """
    acronim_semrel_set = {'"Airbus:AIRBUS_AS_AIRPLANE"',
                          '"Boeing:BOEING_AIRPLANE"',
                          '"Dreamliner:DREAMLINER"',
                          '"Eurofighter:EUROFIGHTER_AIRPLANE"',
                          '"Fokker:FOKKER_AIRPLANE"',
                          '"Messerschmitt:MESSERSCHMITT_AIRPLANE"',
                          '"Rivet_Joint:RIVET_JOINT"',
                          '"Sukhoi_Superjet:SUKHOI_SUPERJET"',
                          '"Ан:AN_AIRPLANES"',
                          '"Атлант:ATLANT_AIRPLANE"',
                          '"Бе:BE_AIRPLANES"',
                          '"Боинг:BOEING_AIRPLANE"',
                          '"Гольфстрим:GULFSTREAM_AIRPLANE"',
                          '"Ил:IL_AIRPLANES"',
                          '"Кодрон:CAUDRON"',
                          '"Конкорд:CONCORD_AIRPLANE"',
                          '"мессершмитт:MESSERSCHMITT_AIRPLANE"',
                          '"Ривет_Джойнт:RIVET_JOINT"',
                          '"сессна:CESSNA_AIRPLANE"',
                          '"Су:SU_AIRPLANES"',
                          '"Суперджет:SUKHOI_SUPERJET"',
                          '"Т-тридцатьтри:T_THIRTYTHREE"',
                          '"Ту:TU_AIRPLANES"',
                          '"Фоккер:FOKKER_AIRPLANE"',
                          '"цессна:CESSNA_AIRPLANE"',
                          '"Як:YAK_AIRPLANES"'}

    acronim_patern = re.compile(r'\w+-\d+\w*')
    counter = 0
    while counter != len(sent) - 1:
        c = 0
        # Если Case = ZeroCase/DativeSpecial или pos = Prefixoid или случаи типа ТУ-154 / 70 - х
        if sent[counter]['pos'] in ('NOUN', 'NUM') and sent[counter]['feats'] != None and type(sent[counter]['feats']) != str and 'Case' in sent[counter]['feats'] and sent[counter]['feats']['Case'] == 'ZeroCase' \
                or sent[counter]['pos'] == 'Prefixoid' and sent[counter]['token'] not in ('бен', 'де') \
                or sent[counter]['semrel'] in acronim_semrel_set and sent[counter + 1]['token'] == '-' and sent[counter + 2]['label'] == 'Specifier_Number'\
                or sent[counter]['pos'] in ('NOUN', 'ADJ') and sent[counter]['feats'] != None and type(sent[counter]['feats']) != str and 'Case' in sent[counter]['feats'] and 'DativeSpecial' in sent[counter]['feats']['Case'] \
                or sent[counter]['token'].isdigit() and sent[counter + 1]['token'] == '-' and sent[counter + 2]['lemma'] in ('й', 'ый') \
                or sent[counter]['pos'] == 'PROPN' and sent[counter + 1]['token'] == '-' and sent[counter + 2]['token'].startswith('на-') \
                or sent[counter]['label'] == 'QuantityForComposite' and sent[counter]['pos'] == 'Invariable':
            to_merge_token = sent[counter]['token']
            id_skip = sent[counter]['id']
            if sent[counter + 1]['token'] == '-':    # если слово через тире
                if sent[counter]['token'].isdigit() and sent[counter + 2]['lemma'] in ('й', 'ый'):
                    new_token = {'id': sent[counter]['id'],
                                 'token': to_merge_token + sent[counter + 1]['token'] + sent[counter + 2]['token'],
                                 'lemma': to_merge_token + sent[counter + 1]['lemma'] + sent[counter + 2]['lemma'],
                                 'pos': 'ADJ',
                                 'feats': sent[counter]['feats'],
                                 'dep': 'amod',
                                 'head': sent[counter]['head'],
                                 'label': sent[counter]['label'],
                                 'semrel': sent[counter]['semrel']}
                elif sent[counter]['pos'] == 'PROPN' and sent[counter + 2]['token'].startswith('на-'):
                    new_token = {'id': sent[counter]['id'],
                                 'token': to_merge_token + sent[counter + 1]['token'] + sent[counter + 2]['token'],
                                 'lemma': to_merge_token + sent[counter + 1]['lemma'] + sent[counter + 2]['lemma'],
                                 'pos': sent[counter]['pos'],
                                 'feats': sent[counter]['feats'],
                                 'dep': sent[counter]['dep'],
                                 'head': sent[counter]['head'],
                                 'label': sent[counter]['label'],
                                 'semrel': sent[counter]['semrel']}

                elif sent[counter]['semrel'] in acronim_semrel_set and sent[counter + 2]['label'] == 'Specifier_Number':
                    new_token = {'id': sent[counter]['id'],
                                 'token': to_merge_token + sent[counter + 1]['token'] + sent[counter + 2]['token'],
                                 'lemma': to_merge_token + sent[counter + 1]['lemma'] + sent[counter + 2]['lemma'],
                                 'pos': 'PROPN',
                                 'feats': 'Abbr=Yes',
                                 'dep': sent[counter]['dep'],
                                 'head': sent[counter]['head'],
                                 'label': sent[counter]['label'],
                                 'semrel': sent[counter]['semrel']}

                else:
                    new_token = {'id': sent[counter]['id'],
                                 'token': to_merge_token + sent[counter + 1]['token'] + sent[counter + 2]['token'],
                                 'lemma': to_merge_token + sent[counter + 1]['lemma'] + sent[counter + 2]['lemma'],
                                 'pos': sent[counter + 2]['pos'],
                                 'feats': sent[counter + 2]['feats'],
                                 'dep': sent[counter + 2]['dep'],
                                 'head': sent[counter + 2]['head'],
                                 'label': sent[counter + 2]['label'],
                                 'semrel': sent[counter + 2]['semrel']}
                c += 2
                dic = {k: k for k in range(1, len(sent))}
                dic[id_skip] = '_'
                dic[id_skip + 1] = '_'
                for i in range(id_skip + 2, len(dic)):
                    dic[i] = dic[i] - 2

                for j in range(new_token['id'] - 1, len(sent) - c):
                    if j == new_token['id'] - 1:
                        del sent[j]
                        del sent[j + 1]
                        sent[j] = new_token
                    else:
                        sent[j]['id'] -= c

                for i in range(len(sent)):
                    for item in dic:
                        if sent[i]['head'] == item:
                            sent[i]['head'] = dic[item]
                            break
            else:   # если слово не через тире
                new_token = {'id': sent[counter]['id'],
                             'token': to_merge_token + sent[counter + 1]['token'],
                             'lemma': to_merge_token + sent[counter + 1]['lemma'],
                             'pos': sent[counter + 1]['pos'],
                             'feats': sent[counter + 1]['feats'],
                             'dep': sent[counter + 1]['dep'],
                             'head': sent[counter + 1]['head'],
                             'label': sent[counter + 1]['label'],
                             'semrel': sent[counter + 1]['semrel']}
                c += 1
                dic = {k: k for k in range(1, len(sent))}
                dic[id_skip] = '_'
                for i in range(id_skip + 1, len(dic)):
                    dic[i] = dic[i] - 1

                for j in range(new_token['id'] - 1, len(sent) - c):
                    if j == new_token['id'] - 1:
                        sent[j] = new_token
                        del sent[j + 1]
                    else:
                        sent[j]['id'] -= c

                for i in range(len(sent)):
                    for item in dic:
                        if sent[i]['head'] == item:
                            sent[i]['head'] = dic[item]
                            break
        else:
            counter += 1

def pos_invariable_fix(token, pos):
    """
    Меняет часть речи, если она invariable
    """
    dict_of_pairs = {}

    with open('D:\Compreno\SEMarkup_project\compreno2UD\morphology\pos_invariable.txt', 'r', encoding='utf8') as pos_txt:
        for line in pos_txt:
            t, ps = line.strip('\n').split('\t')
            dict_of_pairs[t] = ps

        if token.lower() in dict_of_pairs:
            pos = dict_of_pairs[token.lower()]
    pos_txt.close()

    return pos