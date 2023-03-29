import pysrt as srt
import re
import os

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def chunker(input_list):
    length = len(input_list)
    return [input_list[x:x+125] for x in range(0,length, 125)]

def translate_text(target, text):
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    result = translate_client.translate(text, target_language=target)
    return result

    