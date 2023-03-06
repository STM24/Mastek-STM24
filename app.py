import nltk
from flask import Flask, request, jsonify, render_template
# from textsummarizer import *
from final_summary import *
from PyPDF2 import PdfReader
from transformers import pipeline
import docx
import webvtt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summary_page',methods=['GET','POST'])
def summary_page():
    return render_template('summary_page.html')



# Route for Summarization
@app.route('/summarize',methods=['POST'])
def summarize():
    
    if request.method == 'POST':
        
        #fetching file from html form
        text = request.files['myfile']
        text.save(text.filename)

        #for getting file extension
        find_file = text.filename
        x = find_file.split(".")
        extension = x[1]


        if extension == "pdf":
            reader = PdfReader(text.filename)

            # page = reader.pages[0] for single page
            # getting a all pages from the pdf file
            page = len(reader.pages)
            
            # extracting text from page
            file_text = page.extract_text()

        elif extension == "docx":
            # f = open(text.filename, "r")
            # file_text = f.read()

            # Load the docx file
            doc = docx.Document(text.filename)

            # Extract the text from the document
            file_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

        elif extension == "vtt":
            # Load VTT file
            captions = webvtt.read(text.filename)

            # Iterate through captions and extract text
            file_text = ''
            for caption in captions:
                file_text += caption.text + '\n'   

        else:
            #for txt file
            f = open(text.filename, "r")
            file_text = f.read()


        if not request.form['numOfLines']:
            numOfLines = 3
        else:
            numOfLines = int(request.form['numOfLines'])            

        # Calling function for summarzation
        Summary = generate_summary(file_text)
        
    return render_template('result.html',
                               text_summary=Summary,
                            #    lines_original = original_length,
                               lines_summary = numOfLines,
                               file_name = text.filename)

        # ******************END************************

#Route for total active attendees
@app.route('/attendance',methods=['POST'])
def attendance():
    if request.method == 'POST':

        #fetching file from html form
        text = request.files['myfile1']
        text.save(text.filename)

        f = open(text.filename, "r")
        string = f.read()
        # Stores the indices and attendees
        dels = []
        namee = []
        # ans = ""
        for i in range(len(string)):
            
            # If opening delimiter
            # is encountered
            if (string[i] == '<') :
                dels.append(i + 2);

            # If closing delimiter
            # is encountered
            elif (string[i] == '>' and len(dels) != 0) :

                # Extract the position
                # of opening delimiter
                pos = dels[-1];
                dels.pop();

                # Length of substring
                length = i - 1 - pos;

                # Extract the substring
                ans = string[pos + 1 : pos + 1 + length]
                
                #replacing blank space between names with _
                names = ans.replace(" ", "_")
                
                namee.append(names)
                
        meet_attendees = set(namee)
        meet_attendees.remove("")

        S = ', '.join(meet_attendees)
        file = open("Active_Attendees.txt","w")

        file.write("Total Active attendees: ")
        file.write(str(len(meet_attendees)))

        file.write("\nTotal Active attendees Name: \n")

        file.write(str(S))
        file.close()

    return render_template('attendance.html',
                               meet_attendees_name=meet_attendees,                           
                               total_att = len(meet_attendees),
                               file_name = text.filename
                               )
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    