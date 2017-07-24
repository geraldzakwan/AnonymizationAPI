def simple_anonymization(ner_prediction):
    ret_tokenize = []

    for chunk_tuple in ner_prediction:
        if (chunk_tuple[1] != 'O'):
            ret_tokenize.append(chunk_tuple[1])
        else:
            ret_tokenize.append(chunk_tuple[0])

    return ret_tokenize
