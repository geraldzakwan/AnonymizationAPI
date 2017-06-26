import sys
import classifier
import post_processing
import anonymization

if __name__ == "__main__":
    if(sys.argv[1] == 'naive_bayes'):
        if(sys.argv[2] == 'load'):
            cls = classifier.load(sys.argv[3])
        else:
            filename = 'NB_' + sys.argv[2] + '_train_data'
            cls = classifier.train_naive_bayes(int(sys.argv[2]), filename)

        text = 'Geraldi Dzakwan is a student at Bandung Institute of Technology. Geraldi Dzakwan will graduate next year.'
        result = classifier.classify(cls, text)
        # print(result)
        # acc = classifier.calculate_accuracy(cls, 1000)
        # print(acc)

        corrected_list = post_processing.class_correction(result)
        restructured_list = post_processing.restructure_list(corrected_list)
        post_processed_list = post_processing.coreference_resolution(restructured_list)
        # print(post_processed_list)

        anonymized_message = anonymization.anonymize_message(post_processed_list, 'general')
        print(anonymized_message)

    elif(sys.argv[1] == 'perceptron'):
        if(sys.argv[2] == 'load'):
            cls = classifier.load(sys.argv[3])
        else:
            filename = 'P_' + sys.argv[2] + '_train_data'
            cls = classifier.train_perceptron(int(sys.argv[2]), filename)

        text = 'Geraldi Dzakwan is a student at Bandung Institute of Technology. Geraldi Dzakwan will graduate next year.'
        result = classifier.classify(cls, text)
        # print(result)
        # acc = classifier.calculate_accuracy(cls, 1000)
        # print(acc)

        corrected_list = post_processing.class_correction(result)
        restructured_list = post_processing.restructure_list(corrected_list)
        post_processed_list = post_processing.coreference_resolution(restructured_list)
        # print(post_processed_list)

        anonymized_message = anonymization.anonymize_message(post_processed_list, 'general')
        print(anonymized_message)
