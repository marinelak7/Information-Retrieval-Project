from greek_stemmer import stemmer
from collections import Counter

"""
Επιστρέφει μια λίστα της συμβολοσειράς Data χωρίς σημεία στίξης και με αντικατάσταση των περισσότερων ειδικών χαρακτήρων
"""
def punctuation_removal(Data):
    preprocessed_data = [] #Αρχικοποίηση μιας λίστας για την αποθήκευση προεπεξεργασμένων δεδομένων
    
    # Αφαίρεση σημείων στίξης και αντικατάσταση ειδικών χαρακτήρων στη συμβολοσειρά δεδομένων εισόδου
    preprocessed_data = Data.replace(',', ' ').replace('.', ' ').replace('-', ' ').replace('–', ' ').\
    replace(':', ' ').replace('«', ' ').replace('»', ' ').replace(';', ' ').replace('!', ' ').replace('…',' ').\
    replace('\t', ' ').replace('\b', ' ').replace('\xa0', ' ').replace('έ','ε').replace('ά','α').replace('ή','η').replace('ό','ο').\
    replace('ύ','υ').replace('ί','ι').replace('ώ','ω').replace('Ό','ο').replace('Έ','ε').replace('Ά','α').replace('Ή','η').\
    replace('Ύ','υ').replace('Ί','ι').replace('Ώ','ω').lower()
    
    # Διαχωρίστε την προεπεξεργασμένη συμβολοσειρά δεδομένων σε μια λίστα λέξεων
    preprocessed_data = preprocessed_data.split(' ')
    
    # Φιλτράρετε τις κενές συμβολοσειρές, τα κενά και τις μη αλφαβητικές λέξεις
    preprocessed_data = [word for word in preprocessed_data if word != '' and word != ' ' and word.isalpha()]
    
    
    return preprocessed_data

"""
Επιστρέφει μια ενωμένη συμβολοσειρά μιας λίστας λέξεων μετά την αφαίρεση των stopwords
"""
def stop_word_removal(preprocessed_data, stop_words_array):
    preprocessed_data1 = [] # Αρχικοποίηση μιας κενής λίστας για την αποθήκευση των προεπεξεργασμένων λέξεων μετά την αφαίρεση των λέξεων στάσης
    for word in preprocessed_data:
        if word not in stop_words_array: # Ελέγξτε αν η λέξη δεν βρίσκεται στη λίστα των stop words
            preprocessed_data1.append(word)
    preprocessed_data1 = ' '.join(preprocessed_data1) # Ενώστε τη λίστα των προεπεξεργασμένων λέξεων χωρίς τις stop words σε ένα ενιαίο αλφαριθμητικό                          
    return preprocessed_data1

"""
Returns a list from a string after stemming the words in it
"""
def stemming(preprocessed_data):
    preprocessed_data1 = []
    index = 0
    preprocessed_data = preprocessed_data.split(' ')
    for word in preprocessed_data:
        stemmed_word = stemmer.stem_word(word, 'VBG') # Get the stemmed version of the word using a stemmer
        if stemmed_word.islower(): # Check if the stemmed word is in lowercase
            del preprocessed_data[index] # If the stemmed word is lowercase, delete the corresponding word from the list
        else:
            preprocessed_data[index] = stemmed_word # If the stemmed word is not lowercase, replace the original word with the stemmed word in the list
        index += 1
    preprocessed_data1 = preprocessed_data      
    return preprocessed_data1            

"""
Επιστρέφει ένα αλφαριθμητικό μετά από επεξεργασία με αφαίρεση των σημείων στίξης και των stopwords
"""
def preprocess(Data, stop_words_array):
    # Κλήση της συνάρτησης punctuation_removal για την αφαίρεση των σημείων στίξης από την είσοδο Data
    # Κλήση της συνάρτησης stop_word_removal για την αφαίρεση των stop words από τα δεδομένα χωρίς σημεία στίξης
    preprocessed_data = stop_word_removal(punctuation_removal(Data), stop_words_array) 
    return preprocessed_data

"""
Επιστρέφει:
1. processed_data: μια λίστα που σχηματίζεται αφού η λίστα Data(speech) υποστεί τις διαδικασίες προεπεξεργασίας και στελέχωσης. Ελέγχει αν είναι κενή πριν επιστρέψει
2. tags1: Οι πιο συνηθισμένοι όροι στην προεπεξεργασμένη λίστα Data(speech)
"""
def process(Data, stop_words_array):

    preprocessed_data = preprocess(Data, stop_words_array) # Προεπεξεργασία των δεδομένων εισόδου και αφαίρεση των σημείων στίξης και των stopwords
    processed_data = stemming(preprocessed_data)

    data_list = preprocessed_data.split(' ') # Διαχωρισμός των προεπεξεργασμένων δεδομένων σε μια λίστα λέξεων
    word_frequency = Counter(data_list) # Μετρήστε τη συχνότητα κάθε λέξης στα προεπεξεργασμένα δεδομένα

    tags = word_frequency.most_common(5) # Βρείτε τους 5 πιο συνηθισμένους όρους από το λεξικό συχνότητας λέξεων
    tags1 = []
    for tag in tags:
        tags1.append(tag[0]) # Εξάγετε τους όρους από τις πιο κοινές ετικέτες
    
    if (processed_data != []): # Ελέγξτε αν τα επεξεργασμένα δεδομένα δεν είναι κενά πριν επιστρέψετε
        return processed_data, tags1
    else: # Επιστρέφει μια τιμή placeholder αν τα επεξεργασμένα δεδομένα είναι κενά
        return 1, 1
