#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import re

adj_feats = ('Case', 'Gender', 'Number', 'DegreeOfComparison')  # +Anim если это Acc Plur
adv_feats = 'DegreeOfComparison'
noun_feats = ('Animatedness', 'Case', 'Gender', 'Number')
num_feats = ('Animatedness', 'Case', 'Gender')
verb_feats = ('Aspect', 'Mood', 'Number', 'Person', 'Tense', 'GrammaticalType', 'Voice', 'Gender')
pron_feats = ('Animatedness', 'Case', 'Gender', 'Number', 'Person')
det_feats = {'Animatedness', 'Case', 'Degree', 'Gender', 'Number'}

pos_feats = {'ADJ': adj_feats,
             'ADV': adv_feats,
             'NOUN': noun_feats,
             'PROPN': noun_feats,
             'NUM': num_feats,
             'VERB': verb_feats,
             'PRON': pron_feats,
             'AUX': verb_feats,
             'DET': det_feats}

pos_empty = {'ADP', 'INTJ', 'PART', 'SCONJ',
             'CCONJ', 'PUNCT', 'SYM', 'X', 'DET'}

case_set = {'Accusative': 'Acc',
            'Dative': 'Dat',
            'Genitive': 'Gen',
            'Instrumental': 'Ins',
            'Locative': 'Loc',
            'Nominative': 'Nom',
            'Partitive': 'Par',
            'Vocative': 'Voc'}

person_set = {'PersonFirst': '1',
              'PersonSecond': '2',
              'PersonThird': '3'}   #PersonZero

degree_set = {'DegreeSuperlative': 'Sup',
              'DegreePositive': 'Pos',
              'DegreeComparative': 'Cmp'}

mood_set = {'Imperative': 'Imp',
            'Subjunctive': 'Cnd'} #Indicative

abbr_set = {'Abbreviation', 'Lex_Abbreviation', 'Lex_KgSm', 'Lex_LetterAbbreviation', 'Lex_LetterDotAbbreviation'}

neg_set = {'не', 'несмотря', 'ни', 'невзирая', 'нет', 'нет-нет', 'никто', 'ничто',
           'никакой', 'никоторый', 'никак', 'ничей', 'нисколько', 'никогда', 'нигде', 'никуда', 'ниоткуда',
           'некого', 'нечего', 'негде', 'некуда', 'неоткуда', 'некогда', 'незачем'}

short_set = {'ParticipleShortForm', 'AdjectiveShortForm'}

rel_pron = {'кто', 'что', 'какой', 'чей'}

def filter_feats(token, lemma, pos, feats, label, semrel):
    abbr_check = 0
    foreign_check = 0
    short_check = 0
    neg_check = 0

    for f in abbr_set:
        if f in feats.values() and token == lemma:
            abbr_check = 1
    pattern = re.compile(r'[a-zA-Z]+')
    if pattern.search(token):
        foreign_check = 1
    if 'RCNegative' in feats.values() or lemma in neg_set:
        neg_check = 1
    for f in short_set:
        if 'AdjectiveShortness' in feats and feats['AdjectiveShortness'] == f:
            short_check = 1

    if pos in pos_feats:
        needed_feat = {k: v for k, v in feats.items() if k in pos_feats[pos]}
        if 'GrammaticalType' in needed_feat:
            needed_feat['VerbForm'] = needed_feat.pop('GrammaticalType')
        if pos == 'AUX' or pos == 'VERB':
            if 'VerbForm' in needed_feat:
                if needed_feat['VerbForm'] == 'GTInfinitive':
                    needed_feat['VerbForm'] = 'Inf'
                elif needed_feat['VerbForm'] in ('GTVerb', 'GTInvariable'):
                    needed_feat['VerbForm'] = 'Fin'
                elif needed_feat['VerbForm'] in ('GTParticipleAttributive', 'GTParticiple'):
                    needed_feat['VerbForm'] = 'Part'
                    if short_check == 0:
                        needed_feat['Case'] = feats['Case']
                elif needed_feat['VerbForm'] == 'GTAdverb' and pos == 'VERB':
                    needed_feat['VerbForm'] = 'Conv'

        if 'Animatedness' in needed_feat:
            needed_feat['Animacy'] = needed_feat.pop('Animatedness')
        if 'Animacy' in needed_feat:
            if needed_feat['Animacy'] == 'Inanimate':
                needed_feat['Animacy'] = 'Inan'
            else:
                needed_feat['Animacy'] = 'Anim'
        elif pos == 'ADJ' and needed_feat['Case'] == 'Accusative' and needed_feat['Gender'] == 'Masculine' and 'Animatedness' in feats \
            or lemma in ('оба', 'обе', 'два', 'три', 'четыре') and needed_feat['Case'] == 'Accusative' \
            or lemma == 'один' and 'Case' in needed_feat and needed_feat['Case'] == 'Accusative' and needed_feat['Gender'] == 'Masculine':
            if feats['Animatedness'] == 'Inanimate':
                needed_feat['Animacy'] = 'Inan'
            else:
                needed_feat['Animacy'] = 'Anim'

        if 'Case' in needed_feat:
            if needed_feat['Case'] in case_set:
                needed_feat['Case'] = case_set[needed_feat['Case']]
            elif needed_feat['Case'] == 'Prepositional':
                needed_feat['Case'] = 'Loc'
            if pos == 'ADJ' and 'AdjectiveShortness' in needed_feat and needed_feat['AdjectiveShortness'] == 'AdjectiveShortForm':
                needed_feat.pop('Case')
        if 'Case' in needed_feat and needed_feat['Case'] == 'Genitive|Partitive':
            needed_feat['Case'] = 'Gen'
        if 'Case' in needed_feat and needed_feat['Case'] not in ('Acc', 'Dat', 'Gen', 'Ins', 'Loc', 'Nom', 'Par', 'Voc'):
            needed_feat.pop('Case')

        if pos == 'NUM' and 'Gender' in needed_feat and lemma not in ('i', 'ii', 'оба', 'один', 'полтора', 'два'):
            needed_feat.pop('Gender')

        if 'Gender' in needed_feat:
            if needed_feat['Gender'] == 'Feminine' or 'SyntacticGender' in feats and feats['SyntacticGender'] == 'SyntFeminine':
                needed_feat['Gender'] = 'Fem'
            elif needed_feat['Gender'] == 'Neuter' or 'SyntacticGender' in feats and feats['SyntacticGender'] == 'SyntNeuter':
                needed_feat['Gender'] = 'Neut'
            elif needed_feat['Gender'] == 'Masculine':
                needed_feat['Gender'] = 'Masc'
            elif needed_feat['Gender'] == 'Common':
                needed_feat.pop('Gender')
        if 'Gender' in needed_feat:
            if 'DefectnessOfNumberParadigm' in feats and feats['DefectnessOfNumberParadigm'] == 'PluraliaTantum':
                needed_feat.pop('Gender')
            elif 'SyntacticGender' in feats and feats['SyntacticGender'] == 'NoSyntGender':
                needed_feat.pop('Gender')
        if pos in ('VERB', 'AUX') and 'Gender' in needed_feat:
            if needed_feat['VerbForm'] == 'Fin' and needed_feat['Tense'] == 'Past' and needed_feat['Number'] == 'Singular' \
                    or needed_feat['VerbForm'] == 'Part' and needed_feat['Number'] == 'Singular':
                pass
            else:
                    needed_feat.pop('Gender')
        if lemma == 'тысяча' and 'Gender' in needed_feat:
            needed_feat['Gender'] = 'Fem'
        if token == 'деньги' and 'Gender' in needed_feat:
            lemma = 'деньги'
            needed_feat.pop('Gender')

        if 'Number' in needed_feat:
            if needed_feat['Number'] == 'Plural':
                needed_feat['Number'] = 'Plur'
            else:
                needed_feat['Number'] = 'Sing'

        if pos in ('VERB', 'AUX') and 'Tense' in needed_feat and needed_feat['Tense'] == 'Past' and 'Person' in needed_feat:
            needed_feat.pop('Person')
        if 'Person' in needed_feat:
            if needed_feat['Person'] in person_set:
                needed_feat['Person'] = person_set[needed_feat['Person']]
            else:
                needed_feat.pop('Person')

        if 'DegreeOfComparison' in needed_feat:
            needed_feat['Degree'] = needed_feat.pop('DegreeOfComparison')
        if 'Degree' in needed_feat:
            if needed_feat['Degree'] in degree_set:
                needed_feat['Degree'] = degree_set[needed_feat['Degree']]

        if 'Aspect' in needed_feat:
            if needed_feat['Aspect'] == 'Perfective':
                needed_feat['Aspect'] = 'Perf'
            else:
                needed_feat['Aspect'] = 'Imp'
            if 'Pairness' in feats and feats['Pairness'] == 'BiAspectual':
                needed_feat.pop('Aspect')

        if 'Mood' in needed_feat:
            if needed_feat['Mood'] in mood_set:
                needed_feat['Mood'] = mood_set[needed_feat['Mood']]
            else:
                needed_feat.pop('Mood')
        if pos == 'VERB' and 'Mood' not in needed_feat:
            needed_feat['Mood'] = 'Ind'

        if 'Tense' in needed_feat:
            if needed_feat['Tense'] == 'Present':
                needed_feat['Tense'] = 'Pres'
            elif needed_feat['Tense'] == 'Future':
                needed_feat['Tense'] = 'Fut'
            if 'Aspect' in needed_feat and needed_feat['Aspect'] == 'Perf' and needed_feat['Tense'] == 'Pres':
                needed_feat['Tense'] = 'Fut'

        if 'Voice' in needed_feat:
            if needed_feat['Voice'] == 'Active':
                needed_feat['Voice'] = 'Act'
            elif needed_feat['Voice'] == 'Passive':
                needed_feat['Voice'] = 'Pass'
            elif needed_feat['Voice'] == 'VoiceSya':
                if 'SyntPassive' in feats.values():
                    needed_feat['Voice'] = 'Pass'
                elif 'SyntActive' in feats.values():
                    needed_feat['Voice'] = 'Act'
                else:
                    needed_feat['Voice'] = 'Mid'

        if 'VerbForm' in needed_feat and needed_feat['VerbForm'] == 'Part':
            if 'Person' in needed_feat:
                needed_feat.pop('Person')
            if 'Mood' in needed_feat:
                needed_feat.pop('Mood')
        if 'VerbForm' in needed_feat and needed_feat['VerbForm'] == 'Conv':
            if 'Mood' in needed_feat:
                needed_feat.pop('Mood')
            if 'Number' in needed_feat:
                needed_feat.pop('Number')
            if 'Person' in needed_feat:
                needed_feat.pop('Person')
            if 'Gender' in needed_feat:
                needed_feat.pop('Gender')
        if 'VerbForm' in needed_feat and needed_feat['VerbForm'] == 'Inf':
            if 'Gender' in needed_feat:
                needed_feat.pop('Gender')
            if 'Tense' in needed_feat:
                needed_feat.pop('Tense')
            if 'Mood' in needed_feat:
                needed_feat.pop('Mood')
            if 'Number' in needed_feat:
                needed_feat.pop('Number')

        if lemma == 'себя':
            if 'Animacy' in needed_feat:
                needed_feat.pop('Animacy')
            if 'Number' in needed_feat:
                needed_feat.pop('Number')
        if 'кто' in lemma or 'что' in lemma: # чтобы сюда попали "кто-то", "что-нибудь" и др.
            if 'Person' in needed_feat:
                needed_feat.pop('Person')
        if 'где' in lemma or 'куда' in lemma or 'когда' in lemma or 'откуда'in lemma or 'зачем' in lemma:
            needed_feat = '_'
        if lemma == 'сколько':
            if 'Animacy' in needed_feat:
                needed_feat.pop('Animacy')
            if 'Number' in needed_feat:
                needed_feat.pop('Number')
        if 'какой' in lemma or 'чей' in lemma or 'который' in lemma:
            spec_pron_feats = {'Case', 'Number', 'Gender'}
            needed_feat = {k: v for k, v in needed_feat.items() if k in spec_pron_feats}
            if 'Number' in needed_feat and needed_feat['Number'] == 'Plur':
                if 'Gender' in needed_feat:
                    needed_feat.pop('Gender')

        if token in ('более','менее'):
            needed_feat['Degree'] = 'Cmp'

        if pos in ('DET', 'ADJ', 'PRON', 'NUM') and 'Number' in needed_feat and 'Animasy' in needed_feat \
            and 'Case' in needed_feat and needed_feat['Number'] == 'Plur' and needed_feat['Case'] != 'Acc':
            needed_feat.pop('Gender')
            needed_feat.pop('Animacy')

        if pos not in ('NOUN', 'PROPN') and 'Gender' in needed_feat and 'Number' in needed_feat and needed_feat['Number'] == 'Plur':
            needed_feat.pop('Gender')

        if label == 'OrderInTimeAndSpace' and semrel == '"#number:#number:DIGITAL_NUMBER"' or semrel == '"#day_number:DAY_NUMBER"':
            needed_feat = '_'

        if abbr_check:
            needed_feat = {'Abbr': 'Yes'}
        if foreign_check:
            needed_feat['Foreign'] = 'Yes'
        if neg_check:
            if type(needed_feat) == str:
                if needed_feat != '_':
                    needed_feat = needed_feat + '|' + 'Polarity=Neg'
                else:
                    needed_feat = 'Polarity=Neg'
            else:
                needed_feat['Polarity'] = 'Neg'
        if short_check:
            needed_feat['Variant'] = 'Short'

        if type(needed_feat) == str:
            needed_feats = needed_feat
        else:
            needed_feat = dict(sorted(needed_feat.items()))
            needed_feats = [(m + '=' + n) for m, n in needed_feat.items()]

    elif pos in pos_empty:
        needed_feats = '_'
        if pos == 'X' and foreign_check == 1:
            needed_feats = 'Foreign=Yes'
        if neg_check:
            needed_feats = 'Polarity=Neg'

    else:
        needed_feats = '_'

    return needed_feats
