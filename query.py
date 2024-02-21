import query_similarity as cs
import initialize as it
import random as rand

"""
Επιστρέφει τα 5 πιο παρόμοια έγγραφα (συνεδριάσεις) σε ένα ερώτημα:

1. ID συνεδρίασης
2. όνομα του ομιλητή
3. πολιτικό κόμμα του ομιλητή
4. ετικέτες - πιο συχνές λέξεις στην ομιλία
"""
def get_sittings(query, Data, index_dict, words_dict, tags_dict):
    similarities = cs.doc_query_similarity(words_dict, query) # Υπολογισμός της ομοιότητας μεταξύ του ερωτήματος και κάθε εγγράφου (συνεδρίαση)
    
    sittings = []
    for sitting in similarities:
        data = [item for sublist in Data.iloc[[index_dict[sitting]], [0, 5]].values.tolist() for item in sublist] # Πάρτε τα δεδομένα (ID της συνεδρίασης, όνομα ομιλητή, πολιτικό κόμμα) της συνεδρίασης από το πλαίσιο δεδομένων Data

        # Πάρτε τις πιο συχνές λέξεις (ετικέτες) στην ομιλία της συνεδρίασης από το λεξικό ετικετών
        # Προσάρτηση πληροφοριών σχετικά με τη συνεδρίαση
        sittings.append([sitting] + data + [' '.join(tags_dict.get(sitting))] + [similarities[sitting]])
    
    return sittings

"""
Επιστρέφει πληροφορίες για μια συγκεκριμένη συνεδρίαση:

1. όνομα του ομιλητή
2. ημερομηνία διεξαγωγής της συνεδρίασης
3. πολιτικό κόμμα του ομιλητή
4. ομιλία 
5. ετικέτες - πιο συχνές λέξεις στην ομιλία
"""
def get_sitting_info(sitting_id, Data, index_dict, tags_dict):
    # Ανάκτηση των σχετικών δεδομένων (όνομα ομιλητή, ημερομηνία, πολιτικό κόμμα, ομιλία) της συνεδρίασης από το πλαίσιο δεδομένων Data
    data = [item for sublist in Data.iloc[[index_dict[int(sitting_id)]], [0, 1, 5, 10] ].values.tolist() for item in sublist]
    
    
    return data + [' '.join(tags_dict.get(int(sitting_id)))]

"""
Επιστρέφει όλες τις συνεδριάσεις ενός ομιλητή:

1. ID συνεδρίασης
2. πολιτικό κόμμα του ομιλητή
3. ετικέτες - πιο συχνές λέξεις στην ομιλία
"""
def get_sittings_by_speaker(speaker, Data, index_dict, tags_dict, member_dict):
    #sittings =  [[sitting_id] + get_sitting_info(sitting_id, Data, index_dict, tags_dict)[2::2] for sitting_id in member_dict[speaker]]
    #return sittings[::-1]
    speaker_sittings_ids = member_dict[speaker]
    
    # Αρχικοποίηση μιας κενής λίστας για την αποθήκευση πληροφοριών σχετικά με τις συνεδριάσεις του ομιλητή
    sittings = []
    
    # Επαναλάβετε κάθε αναγνωριστικό συνεδρίασης που σχετίζεται με τον ομιλητή
    for sitting_id in speaker_sittings_ids:
        # Λάβετε πληροφορίες σχετικά με τη συνεδρίαση (πολιτικό κόμμα, ετικέτες) χρησιμοποιώντας το αναγνωριστικό συνεδρίασης
        sitting_info = get_sitting_info(sitting_id, Data, index_dict, tags_dict)
        
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
def get_sittings_by_party(party, Data, index_dict, tags_dict, party_dict, member_dict):
    
    sittings = []
    
    # Καθορίστε τον μέγιστο αριθμό ομιλητών που θα λάβετε υπόψη (το πολύ 5 ή τον συνολικό αριθμό των ομιλητών του κόμματος)
    max_speakers = 5 if len(party_dict[party])>5 else len(party_dict[party])
    for speaker in party_dict[party][:max_speakers]:
        for sitting_id in member_dict[speaker]:
            
            # Λήψη πληροφοριών σχετικά με τη συνεδρίαση (αναγνωριστικό συνεδρίασης, όνομα ομιλητή, ετικέτες) χρησιμοποιώντας το αναγνωριστικό συνεδρίασης
            sitting_info = get_sitting_info(sitting_id, Data, index_dict, tags_dict)
            sittings.append([sitting_id] + sitting_info[0::4])
            #sittings.append([sitting_id] + get_sitting_info(sitting_id, Data, index_dict, tags_dict)[0::4])
            break
            
    sittings = sittings[::-1] # Αντιστροφή της σειράς των συνεδριάσεων (εάν χρειάζεται)
    return sittings
    #return sittings[::-1]
    
    

"""# for testing
if __name__ == "__main__":
    global Data, member_dict, party_dict, tags_dict
    Data, Docs, index_dict, words_dict, stop_words_array, member_dict, party_dict, tags_dict = it.init()
    
    #sit = get_sittings_by_speaker(speaker='αραμπατζη αθανασιου φωτεινη',Data=Data,index_dict=index_dict, tags_dict=tags_dict, member_dict=member_dict)
   # print(sit[::-1])
    sit = get_sittings_by_party(party='νεα δημοκρατια',Data=Data, index_dict=index_dict, tags_dict=tags_dict, party_dict=party_dict, member_dict=member_dict)
    print(len(sit))
"""