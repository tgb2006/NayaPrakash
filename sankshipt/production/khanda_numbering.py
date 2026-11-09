"""Render khanda-introduction references in the current local chapter numbering."""

from functools import lru_cache
from pathlib import Path
import json
import re


GU = '૦૧૨૩૪૫૬૭૮૯'
TO_GU = str.maketrans('0123456789', GU)


@lru_cache
def chapters(khanda):
    mapping = Path(__file__).resolve().parents[2] / 'Image/chapter-image-map.json'
    records = json.loads(mapping.read_text(encoding='utf-8-sig'))
    return [(int(re.search(r'chapter_(\d+)_', r['source_file'])[1]), r['chapter_in_khanda'])
            for r in records if r['khanda'] == khanda]


def local_number(number):
    return f'{number:02d}'.translate(TO_GU)


def local_span(khanda, first, last, separator='–'):
    sequence = [ordinal for legacy, ordinal in chapters(khanda) if first <= legacy <= last]
    if not sequence or sequence != list(range(sequence[0], sequence[-1]+1)):
        raise ValueError(f'Khanda {khanda}: unexpected chapter group {first}–{last}')
    return local_number(sequence[0])+separator+local_number(sequence[-1])


@lru_cache
def reference_rules(khanda, kind):
    legacy_count={2:'૯',3:'૧૧૬'}.get(khanda)
    count=str(len(chapters(khanda))).translate(TO_GU)
    pairs={}
    if legacy_count:
        pairs[legacy_count+' અધ્યાય']=count+' અધ્યાય'
    if khanda==2:
        pairs.update({
            '૦૬૫ થી ૦૬૮':local_span(2,65,68,' થી '),
            '૦૬૬.':local_span(2,66,66)+'.',
            '૦૬૮. અપરસંગ્રહભેદક વ્યવહાર (મુક્ત-સંસારી)':
                local_span(2,68,68)+'. અપરસંગ્રહભેદક અને અંતિમ વ્યવહાર',
        })
    if khanda==3:
        first,second=local_span(3,9,14),local_span(3,69,75)
        fourth_a,fourth_b=local_span(3,24,30),local_span(3,76,152)
        pairs.update({
            '૦૦૯-૦૧૪, ૦૬૭-૦૭૫':first+', '+second,
            '૦૦૯ થી ૦૧૪ તથા ૦૬૭ થી ૦૭૫':first.replace('–',' થી ')+' તથા '+second.replace('–',' થી '),
            '૦૨૪-૦૩૦, ૦૭૬-૧૫૨':fourth_a+', '+fourth_b,
            '૦૨૪ થી ૦૩૦ તથા ૦૭૬ થી ૧૫૨':fourth_a.replace('–',' થી ')+' તથા '+fourth_b.replace('–',' થી '),
            '૯૬ અધ્યાયોમાં':'૮૯ અધ્યાયોમાં',
            'આ ખંડના ૧૧૬ અધ્યાયો નીચે મુજબના ચાર મુખ્ય શાસ્ત્રીય સોપાનોમાં સુવ્યવસ્થિત વિભાજિત છે:':
                'કુલ ૧૩૩ અધ્યાયમાં ચાર મુખ્ય શાખાઓ નીચે દર્શાવી છે. પેટાક્રમ ૨૬–૪૨માં નિશ્ચય, શુદ્ધ અને વ્યવહાર નયો તથા ૧૩૨–૧૩૩માં નિત્ય અને અનિત્ય નય છે.',
        })
    if kind in ('chart','list_item'):
        numbers={}
        for legacy,ordinal in chapters(khanda):
            numbers.setdefault(f'{legacy:03d}'.translate(TO_GU),local_number(ordinal))
    else:
        numbers={}
        if khanda==6:
            pairs.update({'અધ્યાય ૧૬૨':'અધ્યાય ૦૫','અધ્યાય ૧૬૪':'અધ્યાય ૦૭'})
    alternatives=[re.escape(value) for value in sorted(pairs,key=len,reverse=True)]
    if numbers:
        alternatives.append(r'(?<![૦-૯])(?:'+'|'.join(numbers)+r')(?![૦-૯]| નયચક્ર)')
    return '|'.join(alternatives),pairs|numbers


def normalize_references(text, khanda, kind):
    pattern,replacements=reference_rules(khanda,kind)
    return re.sub(pattern,lambda match:replacements[match[0]],text) if pattern else text
