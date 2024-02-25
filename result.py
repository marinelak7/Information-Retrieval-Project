import similarity_formula as cs
import data_initialization as initialize
import random as rand

"""
Επιστρέφει τα 5 πιο παρόμοια έγγραφα (συνεδριάσεις) σε ένα ερώτημα:

1. ID συνεδρίασης
2. όνομα του ομιλητή
3. πολιτικό κόμμα του ομιλητή
4. ετικέτες - πιο συχνές λέξεις στην ομιλία
"""
def retrieve_sitting(query, data_frame, index_dictionary, words_dictionary, tags_dictionary):
    similarities = cs.doc_query_similarity(words_dictionary, query) # Υπολογισμός της ομοιότητας μεταξύ του ερωτήματος και κάθε εγγράφου (συνεδρίαση)
    
    sittings = []
    for sitting in similarities:
        data = [item for sublist in data_frame.iloc[[index_dictionary[sitting]], [0, 5]].values.tolist() for item in sublist] # Πάρτε τα δεδομένα (ID της συνεδρίασης, όνομα ομιλητή, πολιτικό κόμμα) της συνεδρίασης από το πλαίσιο δεδομένων data_frame

        # Πάρτε τις πιο συχνές λέξεις (ετικέτες) στην ομιλία της συνεδρίασης από το λεξικό ετικετών
        # Προσάρτηση πληροφοριών σχετικά με τη συνεδρίαση
        sittings.append([sitting] + data + [' '.join(tags_dictionary.get(sitting))] + [similarities[sitting]])
    
    return sittings


"""
Επιστρέφει πληροφορίες για μια συγκεκριμένη συνεδρίαση:

1. όνομα του ομιλητή
2. ημερομηνία διεξαγωγής της συνεδρίασης
3. πολιτικό κόμμα του ομιλητή
4. ομιλία 
5. ετικέτες - πιο συχνές λέξεις στην ομιλία
"""
def retrieve_sitting__information(sitting_id, data_frame, index_dictionary, tags_dictionary):
    # Ανάκτηση των σχετικών δεδομένων (όνομα ομιλητή, ημερομηνία, πολιτικό κόμμα, ομιλία) της συνεδρίασης από το πλαίσιο δεδομένων data_frame
    data = [item for sublist in data_frame.iloc[[index_dictionary[int(sitting_id)]], [0, 1, 5, 10]].values.tolist() for item in sublist]
    
    
    return data + [' '.join(tags_dictionary.get(int(sitting_id)))]


"""
Επιστρέφει όλες τις συνεδριάσεις ενός ομιλητή:

1. ID συνεδρίασης
2. πολιτικό κόμμα του ομιλητή
3. ετικέτες - πιο συχνές λέξεις στην ομιλία
"""
def retrieve_sittings_for_speaker(speaker, data_frame, index_dictionary, tags_dictionary, member_dictionary):
    speaker_sittings_ids = member_dictionary[speaker]
    
    # Αρχικοποίηση μιας κενής λίστας για την αποθήκευση πληροφοριών σχετικά με τις συνεδριάσεις του ομιλητή
    sittings = []
    
    # Επαναλάβετε κάθε αναγνωριστικό συνεδρίασης που σχετίζεται με τον ομιλητή
    for sitting_id in speaker_sittings_ids:
        # Λάβετε πληροφορίες σχετικά με τη συνεδρίαση (πολιτικό κόμμα, ετικέτες) χρησιμοποιώντας το αναγνωριστικό συνεδρίασης
        sitting_info = retrieve_sitting__information(sitting_id, data_frame, index_dictionary, tags_dictionary)
        
        # Προσάρτηση πληροφοριών σχετικά με τη συνεδρίαση (ταυτότητα συνεδρίασης, πολιτικό κόμμα, ετικέτες) στον κατάλογο συνεδριάσεων
        sittings.append([sitting_id] + sitting_info[2::2])
    
    # Αντιστροφή της σειράς των συνεδριάσεων (εάν χρειάζεται)
    sittings = sittings[::-1]
    
    # Επιστρέφει τη λίστα των συνεδριάσεων που σχετίζονται με τον ομιλητή
    return sittings


"""
Επιστρέφει 5 συνεδριάσεις από ένα κόμμα, κάθε συνεδρίαση από διαφορετικό μέλος:

1. ID συνεδρίασης
2. όνομα του ομιλητή
3. ετικέτες - πιο συχνές λέξεις στην ομιλία
"""
def retrieve_sittings_for_party(party, data_frame, index_dictionary, tags_dictionary, party_dictionary, member_dictionary):
    
    sittings = []
    
    # Καθορίστε τον μέγιστο αριθμό ομιλητών που θα λάβετε υπόψη (το πολύ 5 ή τον συνολικό αριθμό των ομιλητών του κόμματος)
    max_speakers = 5 if len(party_dictionary[party]) > 5 else len(party_dictionary[party])
    for speaker in party_dictionary[party][:max_speakers]:
        for sitting_id in member_dictionary[speaker]:
            
            # Λήψη πληροφοριών σχετικά με τη συνεδρίαση (αναγνωριστικό συνεδρίασης, όνομα ομιλητή, ετικέτες) χρησιμοποιώντας το αναγνωριστικό συνεδρίασης
            sitting_info = retrieve_sitting__information(sitting_id, data_frame, index_dictionary, tags_dictionary)
            sittings.append([sitting_id] + sitting_info[0::4])
            #sittings.append([sitting_id] + get_sitting_info(sitting_id, Data, index_dict, tags_dict)[0::4])
            break
            
    sittings = sittings[::-1] # Αντιστροφή της σειράς των συνεδριάσεων (εάν χρειάζεται)
    return sittings

    
    

