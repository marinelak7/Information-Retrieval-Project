import data_processing as dp
import ReadCSV as r
from collections import Counter

def preprocess_speeches(Data, stop_words_array, increment):
    date_dict_member = {}
    date_dict_party = {}
    Data_list = Data['speech'].values.tolist()  # Moved inside the function
    Data_length = len(Data_list)
    past_percentage = 0
    index = 0

    print('Επεξεργασία: 0%')
    for speech in Data_list:
        speech_list = speech.split(' ')
        if len(speech_list) > 100 and index % increment == 0:
            result = dp.preprocess(speech, stop_words_array)
            name = Data['member_name'][index]
            party = Data['political_party'][index]

            if result and isinstance(name, str) and isinstance(party, str):
                date_temp = Data['sitting_date'][index]
                date = date_temp[-4:]

                if date in date_dict_member:
                    date_dict_member[date][name] = date_dict_member[date].get(name, '') + ' ' + result
                else:
                    date_dict_member[date] = {name: result}

                if date in date_dict_party:
                    date_dict_party[date][party] = date_dict_party[date].get(party, '') + ' ' + result
                else:
                    date_dict_party[date] = {party: result}

        index += 1
        percentage = int(index / Data_length * 100)
        if past_percentage != percentage:
            print('Επεξεργασία: ' + str(percentage) + '%')
            past_percentage = percentage

    print('Η επεξεργασία ολοκληρώθηκε!')
    return date_dict_member, date_dict_party


def write_keywords_to_file(date_dict, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for date, data in date_dict.items():
            file.write('Year: ' + str(date) + '\n============================\n============================\n')
            for key, value in data.items():
                file.write(key + ':\n')
                dict_list = value.split(' ')
                word_frequency = Counter(dict_list)
                tags = word_frequency.most_common(15)
                tags1 = [tag[0] for tag in tags]
                file.write(', '.join(tags1))
                file.write('\n-------------\n')
    print('File made!')


def find_KeyWords():
    Data, stop_words_array = r.readCSV()
    increment = 5

    if increment <= 0:
        print('Increment can\'t be less than 1. (Set automatically to 1)')
        increment = 1

    date_dict_member, date_dict_party = preprocess_speeches(Data, stop_words_array, increment)

    write_keywords_to_file(date_dict_member, ".\\output_files\MemberKeywordsAnalysis.txt")
    write_keywords_to_file(date_dict_party, ".\\output_files\PartyKeywordsAnalysis.txt")


find_KeyWords()
