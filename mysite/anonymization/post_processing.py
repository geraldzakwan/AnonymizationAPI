import nltk

# This should accept raw nltk structure from classifier result
def class_correction(processed_list):
    return processed_list

# This should accept FIX named entity
def restructure_list(corrected_list):
    restructured_list = []

    for chunk in corrected_list:
        i = 0
        chunk_type = type(chunk)

        if (chunk_type == nltk.tree.Tree):
            # This is named entity
            chunk_class = chunk.label()
            # chunk_pos_tag_list = []
            phrase = ""

            for element in chunk:
                phrase = phrase + element[0] + " "

            # Remove last space
            phrase = phrase[:-1]

            restructured_list.append([phrase, chunk_class])

        elif (chunk_type == tuple):
            # This isn't named entity
            restructured_list.append([chunk[0], 'O'])

        # Debugging
        # for elements in chunks:
        #     print elements,
        #     print i
        #     i = i + 1

    # for element in post_corrected_list:
    #     print element[0], element[1]

    return restructured_list

# Accept simple list, add marks to the same word
def coreference_resolution(restructured_list):
    word_map = {}

    for i in range(0, len(restructured_list)):
        element = restructured_list[i]
        element_class = element[1]

        if (element_class != 'O'):
            element_word = element[0]

            # The word occurs before
            if (element_word in word_map):
                # Add marks that point it to the first occurence
                restructured_list[i].append(word_map[element_word])
            else:
                word_map[element_word] = i

    return restructured_list
