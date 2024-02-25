
from unittest import result
from flask import Flask, render_template, request, redirect
import result as res
import data_processing as dp
import data_initialization as initialize

# Δημιουργία μιας web εφαρμογής Flask
app = Flask(__name__)

# Αρχικοποιήστε τις global μεταβλητές καλώντας τη συνάρτηση init() από την ενότητα 'initialize.py'
Data, index_dict, words_dict, stop_words_array, member_dict, party_dict, tags_dict = initialize.init()
fs = 0  # Αρχικοποίηση fs


# Ορίστε μια διαδρομή για τη ριζική διεύθυνση URL ('/') και καθορίστε τις μεθόδους GET και POST
@app.route('/', methods=['GET', 'POST'])
def index():
    global uquery, fs, squery
    
    # Ελέγξτε αν η μέθοδος αίτησης είναι POST (υποβολή φόρμας)
    if request.method == 'POST':
        # Πάρτε το ερώτημα αναζήτησης από τη φόρμα
        squery = request.form.get('query')
        # Επεξεργαζόμαστε το ερώτημα χρησιμοποιώντας τη συνάρτηση 'process' από το 'data_processing.py'
        uquery, query_tags = dp.process(squery, stop_words_array)
        fs = 1 # Set flag fs to 1
        
        
        # Ανακατεύθυνση σε μια σελίδα 404 αν το ερώτημα δεν είναι έγκυρο
        if (type(uquery) is int):
            return redirect('Error.html')
        
        # Ανακατεύθυνση στη σελίδα αποτελεσμάτων αν η επεξεργασία του ερωτήματος είναι επιτυχής
        return redirect('/result')
        
    return render_template('index.html') # Εκτέλεση του προτύπου index.html αν η μέθοδος αίτησης είναι GET

# Σελίδα αποτελεσμάτων 
@app.route('/result', methods=['GET', 'POST'])
def queries():
    global sitting_id, data, speaker_name, party_name, squery, uquery, querries, fs

    if fs == 1: # Αποκτήστε τα δεδομένα του αποτελέσματος με βάση το επεξεργασμένο ερώτημα
        data = res.retrieve_sitting(uquery, Data, index_dict, words_dict, tags_dict)
        querries = render_template('result.html', queryDetails = data, uquery = squery)
        
        

    # αίτημα για περισσότερες πληροφορίες σχετικά με τη συνεδρίαση, τον ομιλητή ή το πολιτικό κόμμα
    # Χειρισμός αίτησης POST
    if request.method == 'POST':
        # Ελέγξτε ποια ενέργεια ζήτησε ο χρήστης (συνεδρίαση, ομιλητής ή πάρτι)
        if "sitting" in request.form:
            sitting_id = request.form.get('sitting')   
            return redirect('/sitting')
        elif "speaker" in request.form:
            speaker_name = request.form.get('speaker')
            return redirect('/speaker')
        elif "party" in request.form:
            party_name = request.form.get('party')
            return redirect('/party')
            
    return querries

#Σελίδα συνεδρίασης
@app.route('/sitting', methods=['GET', 'POST'])
def sitting():
    global sitting_id, data, speaker_name, party_name, Data, tags_dict, fs
    data = res.retrieve_sitting__information(sitting_id, Data, index_dict, tags_dict)
    fs += 1

    # αίτημα για περισσότερες πληροφορίες σχετικά με τον ομιλητή ή το πολιτικό κόμμα
    if request.method == 'POST':
        if "speaker" in request.form:
            speaker_name = request.form.get('speaker')
            return redirect('/speaker')
        elif "party" in request.form:
            party_name = request.form.get('party')
            return redirect('/party')

    # Εκτέλεση του προτύπου sitting.html με τα δεδομένα που ανακτήθηκαν
    return render_template('sitting.html', toPrint = data)


#Σελίδα ομιλητή
@app.route('/speaker', methods=['GET', 'POST'])
def speaker():
    global sitting_id, data, speaker_name, party_name, Data, tags_dict, member_dict, fs
    sittings = res.retrieve_sittings_for_speaker(speaker_name, Data, index_dict, tags_dict, member_dict)
    fs += 1

    # αίτημα για περισσότερες πληροφορίες σχετικά με τη συνεδρίαση ή το πολιτικό κόμμα
    if request.method == 'POST':
        if "sitting" in request.form:
            sitting_id = request.form.get('sitting')   
            return redirect('/sitting')
        elif "party" in request.form:
            party_name = request.form.get('party')
            return redirect('/party')

    # Εκτέλεση του προτύπου speaker.html με τα δεδομένα που ανακτήθηκαν
    return render_template('speaker.html', sittings = sittings, speaker_name = speaker_name), 404

@app.route('/party', methods=['GET', 'POST'])
def party():
    global sitting_id, data, speaker_name, party_name, Data, tags_dict, party_dict, member_dict, fs
    data = res.retrieve_sittings_for_party(party_name, Data, index_dict, tags_dict, party_dict, member_dict)
    fs += 1

    # αίτημα για περισσότερες πληροφορίες σχετικά με τη συνεδρίαση ή τον ομιλητή
    if request.method == 'POST':
        if "sitting" in request.form:
            sitting_id = request.form.get('sitting')   
            return redirect('/sitting')
        elif "speaker" in request.form:
            speaker_name = request.form.get('speaker')
            return redirect('/speaker')

    # Εκτέλεση του προτύπου party.html με τα δεδομένα που ανακτήθηκαν
    return render_template('party.html', sittings = data, party_name = party_name)

# Χειριστής σφαλμάτων για σφάλματα 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('Error.html'), 404


# Εκτελέστε την εφαρμογή Flask
if __name__ == '__main__':
    #global Data, index_dict, words_dict, member_dict, party_dict, tags_dict, stop_words_array, fs
    #Data, index_dict, words_dict, stop_words_array, member_dict, party_dict, tags_dict = init.init()
    #fs = 0
    app.run(debug=False)
# Δημιουργία μιας web εφαρμογής Flask
app = Flask(__name__)

# Αρχικοποιήστε τις global μεταβλητές καλώντας τη συνάρτηση init() από την ενότητα 'initialize.py'
Data, index_dict, words_dict, stop_words_array, member_dict, party_dict, tags_dict = initialize.init()
fs = 0  # Αρχικοποίηση fs


# Ορίστε μια διαδρομή για τη ριζική διεύθυνση URL ('/') και καθορίστε τις μεθόδους GET και POST
@app.route('/', methods=['GET', 'POST'])
def index():
    global uquery, fs, squery
    
    # Ελέγξτε αν η μέθοδος αίτησης είναι POST (υποβολή φόρμας)
    if request.method == 'POST':
        # Πάρτε το ερώτημα αναζήτησης από τη φόρμα
        squery = request.form.get('query')
        # Επεξεργαζόμαστε το ερώτημα χρησιμοποιώντας τη συνάρτηση 'process' από το 'data_processing.py'
        uquery, query_tags = dp.process(squery, stop_words_array)
        fs = 1 # Set flag fs to 1
        
        
        # Ανακατεύθυνση σε μια σελίδα 404 αν το ερώτημα δεν είναι έγκυρο
        if (type(uquery) is int):
            return redirect('Error.html')
        
        # Ανακατεύθυνση στη σελίδα αποτελεσμάτων αν η επεξεργασία του ερωτήματος είναι επιτυχής
        return redirect('/result')
        
    return render_template('index.html') # Εκτέλεση του προτύπου index.html αν η μέθοδος αίτησης είναι GET

# Σελίδα αποτελεσμάτων 
@app.route('/result', methods=['GET', 'POST'])
def queries():
    global sitting_id, data, speaker_name, party_name, squery, uquery, querries, fs

    if fs == 1: # Αποκτήστε τα δεδομένα του αποτελέσματος με βάση το επεξεργασμένο ερώτημα
        data = res.retrieve_sitting(uquery, Data, index_dict, words_dict, tags_dict)
        querries = render_template('result.html', queryDetails = data, uquery = squery)
        
        

    # αίτημα για περισσότερες πληροφορίες σχετικά με τη συνεδρίαση, τον ομιλητή ή το πολιτικό κόμμα
    # Χειρισμός αίτησης POST
    if request.method == 'POST':
        # Ελέγξτε ποια ενέργεια ζήτησε ο χρήστης (συνεδρίαση, ομιλητής ή πάρτι)
        if "sitting" in request.form:
            sitting_id = request.form.get('sitting')   
            return redirect('/sitting')
        elif "speaker" in request.form:
            speaker_name = request.form.get('speaker')
            return redirect('/speaker')
        elif "party" in request.form:
            party_name = request.form.get('party')
            return redirect('/party')
            
    return querries

#Σελίδα συνεδρίασης
@app.route('/sitting', methods=['GET', 'POST'])
def sitting():
    global sitting_id, data, speaker_name, party_name, Data, tags_dict, fs
    data = res.retrieve_sitting__information(sitting_id, Data, index_dict, tags_dict)
    fs += 1

    # αίτημα για περισσότερες πληροφορίες σχετικά με τον ομιλητή ή το πολιτικό κόμμα
    if request.method == 'POST':
        if "speaker" in request.form:
            speaker_name = request.form.get('speaker')
            return redirect('/speaker')
        elif "party" in request.form:
            party_name = request.form.get('party')
            return redirect('/party')

    # Εκτέλεση του προτύπου sitting.html με τα δεδομένα που ανακτήθηκαν
    return render_template('sitting.html', toPrint = data)


#Σελίδα ομιλητή
@app.route('/speaker', methods=['GET', 'POST'])
def speaker():
    global sitting_id, data, speaker_name, party_name, Data, tags_dict, member_dict, fs
    sittings = res.retrieve_sittings_for_speaker(speaker_name, Data, index_dict, tags_dict, member_dict)
    fs += 1

    # αίτημα για περισσότερες πληροφορίες σχετικά με τη συνεδρίαση ή το πολιτικό κόμμα
    if request.method == 'POST':
        if "sitting" in request.form:
            sitting_id = request.form.get('sitting')   
            return redirect('/sitting')
        elif "party" in request.form:
            party_name = request.form.get('party')
            return redirect('/party')

    # Εκτέλεση του προτύπου speaker.html με τα δεδομένα που ανακτήθηκαν
    return render_template('speaker.html', sittings = sittings, speaker_name = speaker_name)

@app.route('/party', methods=['GET', 'POST'])
def party():
    global sitting_id, data, speaker_name, party_name, Data, tags_dict, party_dict, member_dict, fs
    data = res.retrieve_sittings_for_party(party_name, Data, index_dict, tags_dict, party_dict, member_dict)
    fs += 1

    # αίτημα για περισσότερες πληροφορίες σχετικά με τη συνεδρίαση ή τον ομιλητή
    if request.method == 'POST':
        if "sitting" in request.form:
            sitting_id = request.form.get('sitting')   
            return redirect('/sitting')
        elif "speaker" in request.form:
            speaker_name = request.form.get('speaker')
            return redirect('/speaker')

    # Εκτέλεση του προτύπου party.html με τα δεδομένα που ανακτήθηκαν
    return render_template('party.html', sittings = data, party_name = party_name), 404

# Χειριστής σφαλμάτων για σφάλματα 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('Error.html'), 404


# Εκτελέστε την εφαρμογή Flask
if __name__ == '__main__':
    app.run(debug=False)