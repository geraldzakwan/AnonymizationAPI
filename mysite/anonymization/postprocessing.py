def restructure_sentence(ret_tokenize):
    ret_sentence = ""

    for token in ret_tokenize:
        ret_sentence = ret_sentence + token + " "

    return ret_sentence

# Asumsi entity ngk mungkin 2
def rebuild_to_original(ner_prediction, normalized_original_token):
    # print ''
    # print ''
    # print(ner_prediction)
    # print ''
    # print(normalized_original_token)
    # print ''
    # print ''

    c1 = 0
    c2 = 0
    result = ''
    token_with_space = ''
    for token in normalized_original_token:
        token_with_space = token_with_space + token[1] + ' '

    while(c1 < len(ner_prediction)):
        if(ner_prediction[c1][0] == normalized_original_token[c2][0]):
            result = result + normalized_original_token[c2][1] + ' '
            c1 = c1 + 1
            c2 = c2 + 1
            # print result + 'ATAS'
        else:
            result = result + ner_prediction[c1][0] + ' '
            c1 = c1 + 1
            c2 = c2 + 1
            while(normalized_original_token[c2][0] != ner_prediction[c1][0]):
                c2 = c2 + 1
            # print result + 'BAWAH'

    list_of_ret = []
    list_of_ret.append(result)
    list_of_ret.append(token_with_space)
    return list_of_ret
