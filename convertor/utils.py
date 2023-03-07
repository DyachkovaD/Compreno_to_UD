#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import re
import csv
import pickle

from morphology.pos_module import convert_pos
from morphology.feats_module import filter_feats
from morphology.fixes import imp_and_perf
from morphology.fixes import fix_lemmas
from morphology.fixes import indexation_bounded_csv
from morphology.fixes import bounded_foreign
from morphology.fixes import merge
from morphology.fixes import pos_invariable_fix


wordline_pattern = re.compile(r'^.+?\t.+?[A-Za-z]+')
foreign_bounded_token = re.compile(r'[A-za-z]+ [A-za-z]+')
number_bounded = re.compile(r'\d+,?\d*?-\d+,?\d*?')
hasch_number = re.compile(r'\d+#:\d+')

def convert_wordlines(infile, outfile):

    bounded_token_list = []
    with open('D:\Compreno\SEMarkup_project\compreno2UD\morphology\mwe.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        csv_dict = {}  # {(old_token, pos): [{part1:v, pos:v...},{part2:v...}}
        parts = []
        word_find = 0
        for row in reader:
            if row[0][0].isalpha():
                old_token = (f"{row[0]} | {row[1]}")
                bounded_token_list.append(row[0])
                word_find = 1
            if word_find:
                if row[0] == '%':
                    parts.append({'id': None, 'token': row[1], 'lemma': row[2], 'pos': row[3], 'feats': row[4], 'dep': row[5], 'head': row[6]})
                if row[0] == '##':
                    word_find = 0
                    csv_dict[old_token] = parts
                    parts = []
    csvfile.close()

    with open(infile, 'rb') as f, open(outfile, 'w', encoding="utf8") as out:
        data = pickle.load(f)
        sent_id = 0
        for i in range(len(data) - 1):
            print('Конвертация ...')
            print(data[i])
            text = ''
            word_counter = 0
            bounded = 0
            bounded_fgn = 0
            while word_counter != len(data[sent_id]):
                w = data[sent_id][word_counter]
                if word_counter == 0 or word_counter == len(data[sent_id]) - 1 \
                        or w['pos'] == 'NOUN' and w['feats'] != None and 'Case' in w['feats'] and w['feats']['Case'] == 'ZeroCase' \
                        or w['pos'] == 'Prefixoid' \
                        or w['pos'] in ('NOUN', 'ADJ') and w['feats'] != None and type(w['feats']) != str and 'Case' in w['feats'] and 'DativeSpecial' in w['feats']['Case']:
                    text += f"{w['token']}"
                else:
                    text += f" {w['token']}"
                word_counter += 1
            out.write(f"# sent_id = {sent_id + 1}\n")
            out.write(f"# text = {text}\n")

            for word in data[sent_id]:
                if word['feats'] == None:
                    word['feats'] = '_'
                if re.compile(r'\w+- \w+').fullmatch(word['token']):
                    word['token'] = word['token'].replace(' ', '')
                word['pos'] = convert_pos(word['token'], word['lemma'], word['pos'], word['feats'], word['dep'], word['label'], word['semrel'])
                word['pos'] = pos_invariable_fix(word['token'], word['pos'])
                if word['pos'] == 'VERB':
                    word['lemma'] = imp_and_perf(word['lemma'], word['feats'])
                if word['lemma'] == '#Expression':
                    word['pos'] = 'PROPN'
                if word['lemma'] == '#ForeignWord':
                    word['pos'] = 'X'
                word['lemma'] = fix_lemmas(word['token'], word['lemma'], word['feats'])
                if hasch_number.search(word['token']):
                    word['token'] = word['token'].replace('#', '')
                    word['lemma'] = word['token']
                if word['token'].lower() in bounded_token_list:
                    bounded = 1
                if foreign_bounded_token.search(word['token']) or number_bounded.fullmatch(word['token']):
                    bounded_fgn = 1
            if bounded:
                indexation_bounded_csv(data[sent_id], csv_dict, bounded_token_list)
            if bounded_fgn:
                bounded_foreign(data[sent_id])
            merge(data[sent_id])

            for word in data[sent_id]:
                word_counter = len(data[sent_id])
                if type(word['feats']) == str:
                    ud_feats = word['feats']
                else:
                    new_feats = filter_feats(word['token'], word['lemma'], word['pos'], word['feats'],word['label'], word['semrel'])
                    if type(new_feats) == str:
                        ud_feats = new_feats
                    else:
                        ud_feats = '|'.join(new_feats)

                out.write(f"{word['id']}\t{word['token']}\t{word['lemma']}\t{word['pos']}\t_\t{ud_feats}\t{word['head']}\t{word['dep']}\t{word['label']}\t{word['semrel']}\t_\n")
                word_counter -= 1
                if word_counter == 0:
                    break
            sent_id += 1
            out.write('\n')
            print('Закончено', sent_id)
    out.close()
    f.close()