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
            restructured_list.append([chunk[0], 'None'])

        # Debugging
        # for elements in chunks:
        #     print elements,
        #     print i
        #     i = i + 1

    # for element in post_corrected_list:
    #     print element[0], element[1]

    return restructured_list

def coreference_resolution(restructured_list):
    return restructured_list
