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

        return text
        
    def g2p(self, text):
        # Normalize text
        norm_text = self.text_normalize(text)
        # Use ToJyutping to get a list of (character, jyutping) tuples
        jyutping_tuples = ToJyutping.get_jyutping_list(norm_text)
        
        phones = []
        word2ph = []
        
        for char, jyutping in jyutping_tuples:
            if jyutping:
                # Split the jyutping if it's not already a list of phonemes
                phonemes = jyutping.split()
                phones.extend(phonemes)
                word2ph.append(len(phonemes))
            else:
                # Handle non-convertible characters (punctuation, etc.)
                continue

        # Now 'phones' should contain only valid Jyutping phonemes
        # and 'word2ph' the phoneme count for each word.
        
        return phones, word2ph
        
    def number_to_cantonese(self, text):
        # Convert numerals to written Cantonese using cn2an library.
        return re.sub(r'\d+(?:\.?\d+)?', lambda x: cn2an.an2cn(x.group(), "low"), text)

    def latin_to_cantonese(self, text):
        # Convert Latin alphabet to Cantonese using the dictionary lookup.
        for latin, ipa in latin_to_ipa.items():
            text = text.replace(latin, ipa + ' ')
        return text
    
    def cantonese_to_ipa(text):
      converter = opencc.OpenCC('jyutjyu')  # Create a new instance of the converter for use in this function
      text = CantoneseLanguageModule.number_to_cantonese(text.upper())
      text = converter.convert(text).replace('-', '').replace('$', ' ')
      text = re.sub(r'[A-Z]', lambda x: latin_to_ipa(x.group())+' ', text)
      text = re.sub(r'[、；：]', '，', text)
      text = re.sub(r'\s*，\s*', ', ', text)
      text = re.sub(r'\s*。\s*', '. ', text)
      text = re.sub(r'\s*？\s*', '? ', text)
      text = re.sub(r'\s*！\s*', '! ', text)
      text = re.sub(r'\s*$', '', text)
      return text
# Utility function to convert text to Jyutping (placed outside the class for global access)
def get_jyutping(text):
    return ToJyutping.get_jyutping_list(text)
   
