from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import data_processing as dp
import data_initialization as initiliaze
import ReadCSV as r


#Read data
Data, stop_words_array = r.readCSV()
Data_list = Data['speech'].values.tolist()
Data_length = len(Data_list)

processed_texts= []

stop_words_array = []
with open(".\\app_files\stopwords.txt", "r", encoding="utf8") as file:
    for stopword in file.readlines():
        stopword = stopword[:-1]
        stop_words_array.append(stopword)

#Preprocessing data

for speech in Data_list:
    speech_list = speech.split(' ')
    
    if (len(speech_list) > 100):
         text = dp.preprocess(speech, stop_words_array=stop_words_array)
         processed_texts.append(text)

#TF-IDF Matrix construction and dimensionality reduction with SVD
tfidf = TfidfVectorizer()
result = tfidf.fit_transform(processed_texts)
lsa = TruncatedSVD(n_components = 20, n_iter = 100, random_state = 42)
lsa.fit_transform(result)


# getting doc topic matrix
transformed_topics = lsa.transform(result)
for n in range(transformed_topics.shape[0]):
    topic_most_probable = transformed_topics[n].argmax()
    file = open(".\\output_files\stopwords.txt", "a") 
    file.write("doc: {} topic: {}\n".format(n, topic_most_probable))
    file.close()
