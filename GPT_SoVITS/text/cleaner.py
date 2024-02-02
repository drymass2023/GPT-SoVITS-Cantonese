import re
from text import cantonese, chinese, japanese, cleaned_text_to_sequence, symbols, english
import ToJyutping

language_module_map = {"zh": cantonese, "ja": japanese, "en": english}
special = [
    ("%", "zh", "SP"),
    ("￥", "zh", "SP2"),
    ("^", "zh", "SP3"),
    # ('@', 'zh', "SP4")#不搞鬼畜了，和第二版保持一致吧
]
def chinese_dialect_cleaners(text, language_module, symbols):
    # Your pre-processing steps remain unchanged
    text = re.sub(r'\[GD\](.*?)\[GD\]', lambda x: cantonese._to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    
    # Text normalization using the language module
    norm_text = language_module.text_normalize(text)

    if isinstance(norm_text, list):
        # Handle tuples and None values within the list
        texts = []
        for tuple_item in norm_text:
            if isinstance(tuple_item, tuple) and tuple_item[1] is not None:
                texts.append(tuple_item[1])
        norm_text = ' '.join(texts)
        
    if language_module.language == "zh":
        phones, word2ph = language_module.g2p(norm_text)
        print("Normalized Text (norm_text):", norm_text)
        print("Length of Normalized Text (norm_text):", len(norm_text))

        print("Phones (phones):", phones)
        print("Length of Phones (phones):", len(phones))

        print("Word to Phoneme Mapping (word2ph):", word2ph)
        print("Length of Word to Phoneme Mapping (word2ph):", len(word2ph))
        norm_text_list = norm_text.split(' ') 
        assert len(phones) == sum(word2ph), "Mismatch in phones and word2ph lengths"
        assert len(norm_text) == len(word2ph), "Mismatch in normalized text and word2ph lengths"
    else:
        phones = language_module.g2p(norm_text)
        word2ph = None

    # Ensure that the phonemes are all in the expected symbol set
    for ph in phones:
        assert ph in symbols, f"Phoneme {ph} not in symbol set"

    # Returning the phones, word2ph, and normalized text
    return phones, word2ph, norm_text
    
def clean_text(text, language):
    for special_s, special_l, target_symbol in special:
        if special_s in text and language == special_l:
            return clean_special(text, language, special_s, target_symbol)
    language_module = language_module_map[language]
    norm_text = language_module.text_normalize(text)
    if language == "zh":
        phones, word2ph = language_module.g2p(norm_text)
        assert len(phones) == sum(word2ph)
        assert len(norm_text) == len(word2ph)
    else:
        phones = language_module.g2p(norm_text)
        word2ph = None

    for ph in phones:
        assert ph in symbols
    return phones, word2ph, norm_text


def clean_special(text, language, special_s, target_symbol):
    """
    特殊静音段sp符号处理
    """
    text = text.replace(special_s, ",")
    language_module = language_module_map[language]
    norm_text = language_module.text_normalize(text)
    phones = language_module.g2p(norm_text)
    new_ph = []
    for ph in phones[0]:
        assert ph in symbols
        if ph == ",":
            new_ph.append(target_symbol)
        else:
            new_ph.append(ph)
    return new_ph, phones[1], norm_text


def text_to_sequence(text, language):
    phones = clean_text(text)
    return cleaned_text_to_sequence(phones)


if __name__ == "__main__":
    print(clean_text("你好%啊啊啊额、还是到付红四方。", "zh"))
