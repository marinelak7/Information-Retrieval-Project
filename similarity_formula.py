from math import log
from heapq import nsmallest
import numpy as np


def doc_query_similarity(words_dictionary, query):
    index_dictionary = {} # Λεξικό για την αντιστοίχιση δεικτών σε αναγνωριστικά εγγράφων
    index = 0
    Tf_idf_dict = {} # Λεξικό για την αποθήκευση της βαθμολογίας tf-idf για κάθε έγγραφο

    # Εύρεση σχετικών εγγράφων (έγγραφα που περιέχουν τουλάχιστον μία λέξη από το ερώτημα)
    Docs_To_Search = []
    for word in query:
        if word in words_dictionary:
            for id in words_dictionary[word]:
                if id not in index_dictionary:
                    Docs_To_Search.append(id)
                    Tf_idf_dict[id] = []
                    index_dictionary[index] = id
                    index += 1

    # Υπολογισμός της βαθμολογίας tf-idf για κάθε έγγραφο και λέξη στο ερώτημα
    query_vector = []
    for word in query:
        if word in words_dictionary:
            
            #Idf υπολογισμός
            N = len(Tf_idf_dict) + 1 # Συνολικός αριθμός εγγράφων
            Nt = len(words_dictionary[word]) + 1 # Αριθμός εγγράφων που περιέχουν τη λέξη
            Idf = log(1 + N/Nt) # Υπολογισμός αντίστροφης συχνότητας εγγράφων (idf)

            # Υπολογισμός της βαθμολογίας tf-idf για τη λέξη στο ερώτημα
            query_vector.append((1 + log(query.count(word))) * Idf)

            # Υπολογισμός της βαθμολογίας tf-idf για τη λέξη σε κάθε σχετικό έγγραφο
            for id in Tf_idf_dict:
                if id not in words_dictionary[word]:

                    Tf_idf_dict[id].append(0.0)

                else:

                    #Tf υπολογισμός
                    Tf = 1 + log(words_dictionary[word][id]) # Υπολογισμός συχνότητας όρων (tf)

                    #Tf_Idf υπολογισμός
                    Tf_idf_dict[id].append(Tf * Idf) # Υπολογισμός της βαθμολογίας Tf-idf για τη λέξη στο έγγραφο

        else:
            # Αν η λέξη δεν υπάρχει στο words_dict, αναθέστε μια προεπιλεγμένη τιμή στη βαθμολογία tf-idf
            query_vector.append((1 + log(query.count(word))) * log(2))
            for id in Tf_idf_dict:
                Tf_idf_dict[id].append(0.0)

    Docs_matrix = np.array([Tf_idf_dict[id] for id in Tf_idf_dict])
    query_vector = np.array(query_vector)                

    # Υπολογίστε την ομοιότητα συνημίτονου μεταξύ του ερωτήματος και κάθε εγγράφου
    similarity_dict = {}
    for i in range (0, len(Docs_matrix)-1):
       
        if (len(Docs_matrix[i]) > 1):
            sim_value = sum(Docs_matrix[i])/(np.linalg.norm(Docs_matrix[i]) * np.linalg.norm(query_vector))
        else:
            sim_value = sum(Docs_matrix[i])
        similarity_dict[index_dictionary[i]] = sim_value

    # Ταξινόμηση του λεξικού ομοιότητας και εξαγωγή των 5 πιο σχετικών εγγράφων
    heap = [(-value, key) for key, value in similarity_dict.items()]
    sim_list = nsmallest(5, heap)
    
    # Μετατρέψτε τα 5 κορυφαία έγγραφα σε λεξικό με κλειδιά τα αναγνωριστικά και τιμές τις βαθμολογίες ομοιότητας
    sim_dict = {}
    for tuple in sim_list:
        sim_dict[tuple[1]] = -1 * tuple[0]
    
    return sim_dict
