import re
import cn2an
import opencc
import ToJyutping
def get_jyutping(text):
    return ToJyutping.get_jyutping_list(text)
# List of (Latin alphabet, ipa) pairs:
latin_to_ipa = {
    'A': 'ei˥',
    'B': 'biː˥',
    'C': 'siː˥',
    'D': 'tiː˥',
    'E': 'iː˥',
    'F': 'e˥fuː˨˩',
    'G': 'tsiː˥',
    'H': 'ɪk̚˥tsʰyː˨˩',
    'I': 'ɐi˥',
    'J': 'tsei˥',
    'K': 'kʰei˥',
    'L': 'e˥llou˨˩',
    'M': 'ɛːm˥',
    'N': 'ɛːn˥',
    'O': 'ou˥',
    'P': 'pʰiː˥',
    'Q': 'kʰiːu˥',
    'R': 'aː˥lou˨˩',
    'S': 'ɛː˥siː˨˩',
    'T': 'tʰiː˥',
    'U': 'juː˥',
    'V': 'wiː˥',
    'W': 'tʊk̚˥piː˥juː˥',
    'X': 'ɪk̚˥siː˨˩',
    'Y': 'waːi˥',
    'Z': 'iː˨sɛːt̚˥'
}
symbols = set(latin_to_ipa.values())
class CantoneseLanguageModule:
    def __init__(self):
        self.converter = opencc.OpenCC('jyutjyu')
        self.language = "zh" 
    
    def text_normalize(self, text):
        # Ensure that the input 'text' is a string, not a list.
        if not isinstance(text, str):
            raise ValueError("text should be a string.")

        # Convert numbers and Latin letters to Cantonese
        text = self.number_to_cantonese(text.upper())
        text = self.latin_to_cantonese(text)

        # Use the Jyutping conversion here and assume the return is a list.
        norm_text = get_jyutping(text)
        return norm_text
    def g2p(self, text):
      norm_text = self.text_normalize(text)
      if isinstance(norm_text, list):
        # Flatten the list if nested and ensure all items are strings
        phones = []
        for item in norm_text:
            if isinstance(item, list):
                phones += item  # If 'item' is a sublist, add its items to 'phones'
            elif isinstance(item, str):
                phones.append(item)  # If 'item' is already a string, append it
            # If 'item' is a tuple (or another type), handle it accordingly here
            # e.g., if you expect a tuple, you might want to do something with it
            # You need to know the structure that `get_jyutping` function returns
      else:
        phones = norm_text.split()  # If 'norm_text' is a string, split into list

    # Now create a mapping value for each phoneme
    # This simple example just creates a mapping of '1', but you can adjust
      word2ph = [1] * len(phones)
    
      return phones, word2ph    
    def number_to_cantonese(self, text):
        # Convert numerals to written Cantonese using cn2an library.
        return re.sub(r'\d+(?:\.?\d+)?', lambda x: cn2an.an2cn(x.group(), "low"), text)

    def latin_to_cantonese(self, text):
        # Convert Latin alphabet to Cantonese using the dictionary lookup.
        for latin, ipa in latin_to_ipa.items():
            text = text.replace(latin, ipa + ' ')
        return text

# Utility function to convert text to Jyutping (placed outside the class for global access)
def get_jyutping(text):
    return ToJyutping.get_jyutping_list(text)
    