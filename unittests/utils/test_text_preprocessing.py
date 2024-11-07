from utils.text_preprocessing import get_document_maps, get_title, get_section_maps, contains_valid_word_like_sequence, extract_line_contents, extract_document_data
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def test_get_title():
    test_document_name = '024-003l_S2k_Neugeborenen-Transport_2024-08.pdf'
    expected_output = 'S2k Neugeborenen Transport'
    assert expected_output == get_title(test_document_name)

def test_contains_valid_word_like_sequence():
    valid_sequence = '1. A) Hallo, das ist ein Test.'
    invalid_sequence = '1. 23_02_1998'
    assert contains_valid_word_like_sequence(valid_sequence)
    assert not contains_valid_word_like_sequence(invalid_sequence)

