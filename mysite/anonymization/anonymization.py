# Main library used for natural language processing (natural language toolkit)
import nltk
# Download all basic corpora and library as used in the book
# nltk.download('book')

# Function to do text anonymization based on parameter supplied
def anonymize_message(post_processed_list, anonymization_type):
    if(anonymization_type == 'general'):
        list_len = len(post_processed_list)
        i = 0
        count_person = 0;
        count_organization = 0;
        count_gpe = 0;
        count_geo = 0;
        count_tim = 0;
        count_art = 0;
        count_event = 0;

        while(i < list_len):
            if(post_processed_list[i][1] != 'O'):

                if (len(post_processed_list[i]) > 2):
                    ref_index = post_processed_list[i][2]
                    post_processed_list[i][0] = post_processed_list[ref_index][0]
                else:
                    if(post_processed_list[i][1] == 'per'):
                        count_person = count_person + 1
                        post_processed_list[i][0] = 'PERSON' + '-' + str(count_person)

                    elif(post_processed_list[i][1] == 'org'):
                        count_organization = count_organization + 1
                        post_processed_list[i][0] = 'ORG' + '-' + str(count_organization)

                    elif(post_processed_list[i][1] == 'gpe'):
                        count_gpe = count_gpe + 1
                        post_processed_list[i][0] = 'GPE' + '-' + str(count_gpe)

                    elif(post_processed_list[i][1] == 'geo'):
                        count_geo = count_geo + 1
                        post_processed_list[i][0] = 'GEO' + '-' + str(count_geo)

                    elif(post_processed_list[i][1] == 'tim'):
                        count_tim = count_tim + 1
                        post_processed_list[i][0] = 'TIME' + '-' + str(count_tim)

                    elif(post_processed_list[i][1] == 'art'):
                        count_art = count_art + 1
                        post_processed_list[i][0] = 'ART' + '-' + str(count_art)

                    elif(post_processed_list[i][1] == 'eve'):
                        count_event = count_event + 1
                        post_processed_list[i][0] = 'EVENT' + '-' + str(count_event)

            i = i + 1

    else:
        print 'to be defined'

    anonymized_message = ""

    for element in post_processed_list:
        phrase = element[0]
        anonymized_message = anonymized_message + phrase + " "

    anonymized_message = anonymized_message[:-1]

    return anonymized_message

if __name__ == "__main__":
    print('Anonymization module')
