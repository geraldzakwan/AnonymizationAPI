# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import classifier
import post_processing
import anonymization

# Initialization
cls = None

@csrf_exempt
def index(request):
    if (request.method == 'GET'):
        text = 'Welcome to English message anonymization API.'
        text += '\n\n'
        text += 'You can access several routes:'
        text += '\n'
        text += '1. "/anonymization/train" to train new model.'
        text += '\n'
        text += '2. "/anonymization/load" to load your trained model.'
        text += '\n'
        text += '3. "/anonymization/anonymize" to anonymize your message.'
        text += '\n\n'
        text += 'Use GET method to see the detailed explanation for each route.'
        text += '\n'
        text += 'Use POST method to execute the functionality of each route.'
    elif (request.method == 'POST'):
        text = 'Index routing has no POST handling mechanism.'

    return HttpResponse(text)

@csrf_exempt
def anonymize(request):
    global cls

    if (request.method == 'GET'):
        text = 'Welcome to anonymize route.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    message: "My friend, Ibrahim, comes from France."' + '\n' +'}'
    elif (request.method == 'POST'):
        text = request.POST.get('message')
        if (text == None):
            text = 'Wrong JSON format sent.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    message: "My friend, Ibrahim, comes from France."' + '\n' +'}'
        if (cls == None):
            text = 'Classifier has not been trained yet.'
        else:
            result = classifier.classify(cls, text)

            corrected_list = post_processing.class_correction(result)
            restructured_list = post_processing.restructure_list(corrected_list)
            post_processed_list = post_processing.coreference_resolution(restructured_list)

            anonymized_message = anonymization.anonymize_message(post_processed_list, 'general')
            restructured_message = anonymization.restructure_sentences(anonymized_message)

            text = restructured_message

    return HttpResponse(text)

@csrf_exempt
def train(request):
    global cls

    if (request.method == 'GET'):
        text = 'Welcome to train route.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    classifier: "perceptron"' + '\n' + '    sample: "20000"' + '\n' +'}'
        text += '\n'
        text += 'Classifier you can choose: perceptron, naive_bayes, svm.'
        text += '\n'
        text += 'Range of sample data training : 10000 - 50000.'
    elif (request.method == 'POST'):
        classifier_name = request.POST.get('classifier')
        sample_data = request.POST.get('sample')
        if (classifier_name == None or sample_data == None):
            text = 'Wrong JSON format sent.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    classifier: "perceptron"' + '\n' + '    sample: "20000"' + '\n' +'}'
        else:
            if (classifier_name == 'naive_bayes'):
                filename = 'NB_' + sample_data + '_train_data'
                cls = classifier.train_naive_bayes(int(sample_data), filename)
                text = 'Your model has been trained and saved. Classifier: ' + classifier_name + ', ' + 'Sample: ' + sample_data + '.'
            elif (classifier_name == 'perceptron'):
                filename = 'P_' + sample_data + '_train_data'
                cls = classifier.train_perceptron(int(sample_data), filename)
                text = 'Your model has been trained and saved. Classifier: ' + classifier_name + ', ' + 'Sample: ' + sample_data + '.'
            else:
                text = 'Classifier is not valid.'

    return HttpResponse(text)

@csrf_exempt
def load(request):
    global cls

    if (request.method == 'GET'):
        text = 'Welcome to load route.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    filename: "P_20000_train_data"' + '\n' +'}'
        text += '\n'
        text += 'Remember to put your file in the same directory as manage.py file.'
    elif (request.method == 'POST'):
        filename = request.POST.get('filename')
        if (filename == None):
            text = 'Wrong JSON format sent.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    filename: "P_20000_train_data"' + '\n' +'}'
        else:
            cls = classifier.load(filename)
            text = 'Classifier has been loaded from file: ' + filename

    return HttpResponse(text)
