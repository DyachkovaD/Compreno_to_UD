#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import argparse
from morphology.utils import convert_wordlines


def parse():
    parser = argparse.ArgumentParser(description='Videos to images')
    parser.add_argument('--indir', type=str, help='Input dir for compreno txt')
    parser.add_argument('--outdir', type=str, help='Output dir for UD converted txt')
    args = parser.parse_args()

    return args


# когда отлаживаешь код, легче хардкодить файлы,
# а на будущее сделан argparse для доступа к конвертеру из консоли

indir = 'D:\Compreno\converted_full_notest.bin'
outdir = 'D:\\UD_text_full_notest.conllu'

if __name__ == '__main__':
    print('Starting conversion')

    # args = parse()
    convert_wordlines(indir, outdir)

    print('DONE')
