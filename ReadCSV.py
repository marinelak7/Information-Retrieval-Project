import pandas as pd

def readCSV():
    print("Reading CSV and StopWords file...")
    #Data_temp = pd.read_csv('Greek_Parliament_Proceedings_1989_2020.csv')
    # Load the CSV file into a DataFrame, filtering out rows with political party 'βουλη'
    Data_temp = pd.read_csv('Greek_Parliament_Proceedings_1989_2020_DataSample.csv')
    Data = Data_temp.loc[(Data_temp['political_party'] != 'βουλη')] #Φιλτράρει τις γραμμές από αυτό το DataFrame όπου η τιμή στη στήλη 'political_party' είναι 'βουλη'
    Data.reset_index(drop=True, inplace=True)  #Ο δείκτης του DataFrame μηδενίζεται έτσι ώστε να ξεκινάει από το 0 και να αυξάνεται κατά 1. Αυτό γίνεται με τη μέθοδο `reset_index()` με το όρισμα `drop=True`, το οποίο εμποδίζει την προσθήκη του παλιού δείκτη ως νέας στήλης στο DataFrame.

   
    stop_words_array = read_stop_words()
    
       
    print('Done!')
    return Data, stop_words_array 

def read_stop_words():
    stop_words_array = []
    with open(".\\app_files\stopwords.txt", "r", encoding="utf8") as file: #Ανοίγει ένα αρχείο με όνομα `stopwords.txt` που βρίσκεται στον κατάλογο ".\app_files\" σε κατάσταση ανάγνωσης με κωδικοποίηση utf-8.
        for stopword in file.readlines():
            stopword = stopword.strip() # Αφαιρέστε τον χαρακτήρα νέας γραμμής
            stop_words_array.append(stopword)
            
    return stop_words_array
