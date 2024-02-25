import data_processing as proc
import data_initialization as init
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ReadCSV as csv_reader

"""
This script generates a file with the top k similar speeches.

It uses cosine similarity.
"""

def preprocess_data(Data, stop_words_array):
    Data_list = Data['speech'].values.tolist()
    Data_length = len(Data_list)

    members = {}
    parties = {}
    documents = {}

    past_percentage = 0
    index = 0
    id = 0
    
    increment = 5

    if increment <= 0:
        print('Increment can\'t be less than 1. (Set automatically to 1)')
        increment = 1

    print ('Processing: 0%')
    for speech in Data_list:
        speech_list = speech.split(' ')
        if len(speech_list) > 100 and index % increment == 0:
            result, tags = proc.process(speech, stop_words_array)
            name = Data['member_name'][index]

            if type(result) != int and type(name) == str:
                if name in members.values():
                    index_id = list(members.keys())[list(members.values()).index(name)]
                    documents[index_id] = documents[index_id] + ' ' + ' '.join(result)
                else:
                    documents[id] = ' '.join(result)
                    members[id] = name
                    parties[name] = Data['political_party'][index]
                    id += 1
        
        index += 1    
        
        percentage = int(index / Data_length * 100)
        if past_percentage != percentage:
            print('Επεξεργασία: ' + str(percentage) + '%')
            past_percentage = percentage

    print('Preprocessing Done!')
    return members, parties, documents


def calculate_similarity(documents):
    print('Calculating Similarity...')
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(list(documents.values()))
    tfidf_matrix = tfidf_matrix.toarray()
    similarity_matrix = cosine_similarity(tfidf_matrix[:], tfidf_matrix)
    return similarity_matrix


def find_topk_similar(similarity_matrix, members, parties, k):
    topk_list = []
    topk_values = []
    for i in range(k):
        topk_list.append(0)
        topk_values.append(0)
    for i in range(len(similarity_matrix)):
        for j in range(len(similarity_matrix)):
            inserted = False
            if i != j and [j, i] not in topk_list:
                for r in range(k):
                    if not inserted and similarity_matrix[i][j] > topk_values[r]:
                        inserted = True
                        pos = r
                    elif inserted:
                        temp = topk_list[pos]
                        topk_list[pos] = topk_list[r]
                        topk_list[r] = temp

                        temp1 = topk_values[pos]
                        topk_values[pos] = topk_values[r]
                        topk_values[r] = temp1
                if inserted:
                    topk_list[pos] = [i, j]
                    topk_values[pos] = similarity_matrix[i][j]
    return topk_list, topk_values


def write_to_file(topk_list, topk_values, members, parties, k):
    file = open(".\output_files\TopKSimilar.txt", "w", encoding="utf-8")
    file.write('\n===============\nTop ' + str(k) + ' pairs:\n===============\n\n')
    counter = 0
    for pair in topk_list:
        file.write(members[pair[0]] + ' (' + str(parties[members[pair[0]]]) + ') ------- ' + 
        members[pair[1]] + ' (' + str(parties[members[pair[1]]]) + ')  (Score: ' + str(topk_values[counter]) + ')\n\n')
        counter += 1
    file.close()
    print('File made!')


def generate_topk_similar(k):
    Data, stop_words_array = csv_reader.readCSV()
    members, parties, documents = preprocess_data(Data, stop_words_array)
    similarity_matrix = calculate_similarity(documents)
    topk_list, topk_values = find_topk_similar(similarity_matrix, members, parties, k)
    write_to_file(topk_list, topk_values, members, parties, k)


generate_topk_similar(15)
