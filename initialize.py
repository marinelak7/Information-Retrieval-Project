import pandas as pd
import data_processing as dp
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

"""
Returns two lists: The first is a dataframe containing the content of the CSV file without including the political party 'βουλη' (useless data) 
                    and the second contains the stop words from the stopwords.txt file.
"""


def readCSV():
    print("Reading CSV and StopWords file...")
    #Data_temp = pd.read_csv('Greek_Parliament_Proceedings_1989_2020.csv')
    # Load the CSV file into a DataFrame, filtering out rows with political party 'βουλη'
    Data_temp = pd.read_csv('Greek_Parliament_Proceedings_1989_2020_DataSample.csv')
    Data = Data_temp.loc[(Data_temp['political_party'] != 'βουλη')] #Φιλτράρει τις γραμμές από αυτό το DataFrame όπου η τιμή στη στήλη 'political_party' είναι 'βουλη'
    Data.reset_index(drop=True, inplace=True)  #Ο δείκτης του DataFrame μηδενίζεται έτσι ώστε να ξεκινάει από το 0 και να αυξάνεται κατά 1. Αυτό γίνεται με τη μέθοδο `reset_index()` με το όρισμα `drop=True`, το οποίο εμποδίζει την προσθήκη του παλιού δείκτη ως νέας στήλης στο DataFrame.

    stop_words_array = []
    
    # Διάβασε τις λέξεις στάσης από ένα αρχείο και αποθήκευσε τες σε μια λίστα
    with open(".\\app_files\stopwords.txt", "r", encoding="utf8") as file: #Ανοίγει ένα αρχείο με όνομα `stopwords.txt` που βρίσκεται στον κατάλογο ".\app_files\" σε κατάσταση ανάγνωσης με κωδικοποίηση utf-8.
        for stopword in file.readlines():
            stopword = stopword[:-1] # Αφαιρέστε τον χαρακτήρα νέας γραμμής
            stop_words_array.append(stopword)
    print('Done!')
    return Data, stop_words_array 

"""
Επιστρέφει:
1. Δεδομένα: ένα πλαίσιο δεδομένων που δίνεται από τη συνάρτηση readCSV()
2. index_dict: λεξικό (κλειδί: id, δηλαδή ο αριθμός αναγνώρισης της επεξεργασμένης ομιλίας, τιμή: δείκτης της εν λόγω ομιλίας στο πλαίσιο δεδομένων Data)
3. words_dict: λεξικό συχνότητας όρων (κλειδί: λέξη, δηλαδή οποιαδήποτε συμβολοσειρά που υπάρχει σε μια επεξεργασμένη ομιλία, τιμή: id που με τη σειρά της αποτελεί κλειδί για την τιμή της συχνότητας της εν λόγω λέξης)
4. stop_words_array: κατάλογος που δίνεται από τη συνάρτηση readCSV()
5. member_dict: λεξικό των μελών του κοινοβουλίου (κλειδί: όνομα μέλους, τιμή: κατάλογος των id των επεξεργασμένων ομιλιών του)
6. party_dict: λεξικό κοινοβουλευτικού κόμματος (κλειδί: όνομα κόμματος, τιμή: κατάλογος των ονομάτων των μελών του κόμματος)
7. tags_dict: λεξικό (κλειδί: id, τιμή: κατάλογος που περιέχει τις 5 πιο συχνές λέξεις της ομιλίας του id'd)

Αυτή η συνάρτηση υπολογίζει όλες τις απαραίτητες πληροφορίες για να μπορεί η εφαρμογή να εκτελεί ερωτήματα χρησιμοποιώντας το σενάριο data_processing.
Δεν επεξεργάζονται όλες οι ομιλίες: Εάν οι ομιλίες παραλείπονται λόγω της προσαύξησης, είναι μικρότερες ή ίσες με 100 λέξεις, περιέχουν μόνο stopwords
ή δεν έχουν τεκμηριωμένο ομιλητή ή κόμμα, τότε δεν θα βρίσκονται στην τελική βάση δεδομένων.
"""
def init():
    
    Data, stop_words_array = readCSV() # Ανάγνωση δεδομένων από το αρχείο CSV και λήψη πίνακα stop words
    Data_list = Data['speech'].values.tolist() # Μετατροπή της στήλης ομιλίας από DataFrame σε λίστα
    Data_length = len(Data_list) # Υπολογίστε το μήκος των δεδομένων

    # Αρχικοποίηση λεξικών και μεταβλητών για την αποθήκευση επεξεργασμένων δεδομένων
    index_dict = {}
    words_dict = {}
    tags_dict = {}
    member_dict = {}
    party_dict = {}

    # Αρχικοποίηση μεταβλητών για την παρακολούθηση της προόδου
    past_percentage = 0
    index = 0
    id = 0

    #CHANGE THIS VARIABLE TO MODIFY THE AMOUNT OF DATA THAT'LL BE PROCESSED (HIGHER == LESS DATA, ALL DATA == 1)
    ################################
    increment = 5
    ################################
    
    # Βεβαιωθείτε ότι το increment είναι έγκυρο
    if (increment <= 0):
        print('Increment can\'t be less than 1. (Set automatically to 1)')
        increment = 1

    #t0 = time.time()
    # Εκτύπωση αρχικής προόδου
    print ('Processing: 0%')
    for speech in Data_list:

        # Λάβετε το όνομα του βουλευτή και το πολιτικό κόμμα που σχετίζεται με την ομιλία
        name = Data['member_name'][index]
        party = Data['political_party'][index]
        speech_list = speech.split(' ') # Διαχωρίστε την ομιλία σε μια λίστα λέξεων
        
        # Ελέγξτε τις συνθήκες για την επεξεργασία της ομιλίας
        if (len(speech_list) > 100 and index%increment == 0 and type(name) == str and type(party) == str):
            result, tags = dp.process(speech, stop_words_array)

            # Ελέγξτε αν το αποτέλεσμα της επεξεργασίας είναι έγκυρο
            if (type(result) != int):

                index_dict[id] = index

                # Ενημέρωση λεξικού συχνότητας λέξεων
                for word in result:
                    if word in words_dict:
                        if id in words_dict[word]:
                            words_dict[word][id] += 1
                        else:
                            words_dict[word][id] = 1
                    else:
                        words_dict[word] = {}
                        words_dict[word][id] = 1
            
                tags_dict[id] = tags

                # Ενημέρωση λεξικού μέλους
                if name in member_dict:
                    member_dict[name].append(id)
                else:
                    member_dict[name] = [id]

                # Ενημέρωση λεξικού κόμματος
                if party in party_dict:
                    if name not in party_dict[party]:
                        party_dict[party].append(name)
                else:
                    party_dict[party] = [name]
            
                id += 1

        index += 1    

        # Εκτύπωση ποσοστού επεξεργασίας
        percentage = int(index/Data_length*100)
        if (past_percentage != percentage):
            print('Processing: ' + str(percentage) + '%')
            past_percentage = percentage

    print('Done!')
    return Data, index_dict, words_dict, stop_words_array, member_dict, party_dict, tags_dict 

