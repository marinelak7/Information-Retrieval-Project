import pandas as pd
import data_processing as dp
import warnings
import ReadCSV as r

# Ignore warnings
warnings.filterwarnings("ignore")


def init():
    
    Data, stop_words_array = r.readCSV() # Ανάγνωση δεδομένων από το αρχείο CSV και λήψη πίνακα stop words
    Data_list = Data['speech'].values.tolist() # Μετατροπή της στήλης ομιλίας από DataFrame σε λίστα
    Data_length = len(Data_list) # Υπολογίστε το μήκος των δεδομένων

    # Αρχικοποίηση λεξικών και μεταβλητών για την αποθήκευση επεξεργασμένων δεδομένων
    index_dict, words_dict, tags_dict, member_dict, party_dict = {}, {}, {}, {}, {}

    # Αρχικοποίηση μεταβλητών για την παρακολούθηση της προόδου
    past_percentage = 0
    id, index = 0, 0

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
    print ('Επεξεργασία: 0%')
    for speech in Data_list:

        # Λάβετε το όνομα του βουλευτή και το πολιτικό κόμμα που σχετίζεται με την ομιλία
        name = Data['member_name'][index]
        party = Data['political_party'][index]
        speech_list = speech.split(' ') # Διαχωρίστε την ομιλία σε μια λίστα λέξεων
        
        # Ελέγξτε τις συνθήκες για την επεξεργασία της ομιλίας
        if (len(speech_list) > 100 and index%increment == 0 and isinstance(name, str) and isinstance(party, str)):
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
        past_percentage = print_progress(index, Data_length, past_percentage)

    print('ΟΚ')
    return Data, index_dict, words_dict, stop_words_array, member_dict, party_dict, tags_dict 


def print_progress(index, Data_length, past_percentage):
    # Εκτύπωση ποσοστού επεξεργασίας
        percentage = int(index/Data_length*100)
        if (past_percentage != percentage):
            print('Επεξεργασία: ' + str(percentage) + '%')
        
        return percentage