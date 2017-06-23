import sys
import classifier

if __name__ == "__main__":
    if(sys.argv[1] == 'naive_bayes'):
        if(sys.argv[2] == 'load'):
            cls = classifier.load(sys.argv[3])
        else:
            filename = 'NB_' + sys.argv[2] + '_train_data'
            cls = classifier.train_naive_bayes(int(sys.argv[2]), filename)
        result = classifier.classify(cls, 'default')
        print(result)
        # acc = classifier.calculate_accuracy(cls, 1000)
        # print(acc)
    elif(sys.argv[1] == 'perceptron'):
        if(sys.argv[2] == 'load'):
            cls = classifier.load(sys.argv[3])
        else:
            filename = 'P_' + sys.argv[2] + '_train_data'
            cls = classifier.train_perceptron(int(sys.argv[2]), filename)
        result = classifier.classify(cls, 'default')
        print(result)
        # acc = classifier.calculate_accuracy(cls, 1000)
        # print(acc)
