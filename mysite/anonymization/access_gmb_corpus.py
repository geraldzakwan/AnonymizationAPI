import os
import collections

def to_conll_iob(annotated_sentence):
    """
    `annotated_sentence` = list of triplets [(w1, t1, iob1), ...]
    Transform a pseudo-IOB notation: O, PERSON, PERSON, O, O, LOCATION, O
    to proper IOB notation: O, B-PERSON, I-PERSON, O, O, B-LOCATION, O
    """
    proper_iob_tokens = []
    for idx, annotated_token in enumerate(annotated_sentence):
        tag, word, ner = annotated_token

        if ner != 'O':
            if idx == 0:
                ner = "B-" + ner
            elif annotated_sentence[idx - 1][2] == ner:
                ner = "I-" + ner
            else:
                ner = "B-" + ner
        proper_iob_tokens.append((tag, word, ner))
    return proper_iob_tokens

def read_corpus_ner(corpus_root, mode):
    ret_list = []

    # Create collections.Counter structure data
    # It is basically to count occurence of the words
    ner_count = collections.Counter()
    postag_count = collections.Counter()
    word_count = collections.Counter()

    # Debugging
    # print(type(ner_tags))

    # Debugging
    # Simply to count how many files are processed
    count_tag_file = 0
    # Simply to determine the total file size
    sum_file_size = 0
    # Exit point
    exit = False
    # Iterator
    it = 0

    #Iterate through all the files
    for root, dirs, files in os.walk(corpus_root):
        # if (exit):
        #     break;
        for filename in files:
            # if (exit):
            #     break;
            # Only process tag file
            if filename.endswith("en.tags"):
                count_tag_file = count_tag_file + 1
                sum_file_size = sum_file_size + os.path.getsize(os.path.join(root, filename))

                # Open the full path
                with open(os.path.join(root, filename), 'rb') as file_handle:
                    # Decode file content
                    file_content = file_handle.read().decode('utf-8').strip()

                    # Split sentences, sentences are separated with two newline characters
                    annotated_sentences = file_content.split('\n\n')

                    # Iterate through sentences
                    for annotated_sentence in annotated_sentences:

                        # Split words, words are separated with a newline character
                        annotated_tokens = [seq for seq in annotated_sentence.split('\n') if seq]

                        standard_form_tokens = []

                        for idx, annotated_token in enumerate(annotated_tokens):
                            # Split annotations, annotations are separated with a tab character
                            annotations = annotated_token.split('\t')

                            # The 1st annotation is the word itself, the 2nd is pos_tag, and the 3rd is it's named entity
                            word, pos_tag, ner = annotations[0], annotations[1], annotations[3]

                            if (mode == '--all'):
                                # Get all category including subcategory
                                ner_count[ner] += 1
                            elif (mode == '--core'):
                                # Get only the primary category
                                if ner != 'O':
                                    ner = ner.split('-')[0]

                                # Make it NLTK compatible
                                # Doesn't need it anymore since we're going to use scikit learn
                                # if pos_tag in ('LQU', 'RQU'):
                                #     pos_tag = "``"

                                standard_form_tokens.append((word, pos_tag, ner))

                                ner_count[ner] += 1
                            else:
                                sys.exit('Wrong arguments supplied.')

                            postag_count[pos_tag] += 1
                            word_count[word] += 1

                        conll_tokens = to_conll_iob(standard_form_tokens)

                        # This is to return list
                        # Make it NLTK Classifier compatible - [(w1, t1, iob1), ...] to [((w1, t1), iob1), ...]
                        # Because the classfier expects a tuple as input, first item input, second the class
                        # tuple_to_be_inserted = [((w, t), iob) for w, t, iob in conll_tokens]
                        # ret_list.append(tuple_to_be_inserted)
                        ret_list.append(conll_tokens)

                        # This is to use generator
                        # print('-------------------')
                        # for item in conlltags2tree(conll_tokens):
                        #     print(item)
                        # print('-------------------')
                        # print(conlltags2tree(conll_tokens))
                        # yield conlltags2tree(conll_tokens)

                        # Debugging
                        it = it + 1
                        # print(it)

    # This is to return list
    return ret_list
