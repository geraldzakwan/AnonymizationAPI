# Main library used for natural language processing (natural language toolkit)
import nltk
# Download all basic corpora and library as used in the book
# nltk.download('book')

# Function to do text anonymization based on parameter supplied
def text_anonymization(processed_list, anonymization_type):
    if(anonymization_type == 'general'):
        list_len = len(processed_list)
        i = 0
        count_person = 0;
        count_organization = 0;
        count_gpe = 0;

        while(i < list_len):
            if(processed_list[i][1] != 'None'):
                if(processed_list[i][1] == 'PERSON'):
                    count_person = count_person + 1
                    processed_list[i][0] = 'PERSON' + '-' + str(count_person)
                elif(processed_list[i][1] == 'ORGANIZATION'):
                    count_organization = count_organization + 1
                    processed_list[i][0] = 'ORG' + '-' + str(count_organization)
                elif(processed_list[i][1] == 'GPE'):
                    count_gpe = count_gpe + 1
                    processed_list[i][0] = 'GPE' + '-' + str(count_gpe)

            i = i + 1

        return processed_list
    else:
        return 'to be defined'

if __name__ == "__main__":
    print('Anonymization module')
