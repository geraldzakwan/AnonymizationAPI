def restructure_list(processed_list):
    for chunks in processed_list:
        i = 0
        for elements in chunks:
            print elements,
            print i
            i = i + 1
