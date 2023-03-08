import nltk
from flask import Flask, request, jsonify, render_template
# from textsummarizer import *
from final_summary import *
from Meeting_duration import *
from PyPDF2 import PdfReader
import PyPDF2
from transformers import pipeline
import docx
import webvtt
import csv
import pandas as pd


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summary_page',methods=['GET','POST'])
def summary_page():
    return render_template('summary_page.html')


@app.route('/attendees_page',methods=['GET','POST'])
def attendees_page():
    return render_template('attendees_page.html')


@app.route('/attendees_result',methods=['GET','POST'])
def attendees_result():
    if request.method == 'POST':
        transcript = request.files['myfile']
        transcript.save(transcript.filename)

        with open(transcript.filename, 'r') as f:
            vtt_lines = f.readlines()
        timestamps = []
        for line in vtt_lines:
            if regex.match(r'^\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}$', line.strip()):
                timestamps.append(line.strip())

        formatted_timestamps = []
        for ts in timestamps:
            start, end = ts.split(' --> ')
            start = datetime.strptime(start, '%H:%M:%S.%f')
            end = datetime.strptime(end, '%H:%M:%S.%f')
            formatted_timestamps.append((start, end))

        # print(type(end))
        # print(start,"----",end)
        # print(formatted_timestamps)

        lenn = len(formatted_timestamps) 
        # print(formatted_timestamps[lenn - 1])

        dt = formatted_timestamps[lenn - 1]

        last_len = len(dt)

        aaa = dt[last_len - 1]
        aaa
        minutes = aaa.minute

        hours = aaa.hour

        secs = aaa.second

        f = open(transcript.filename, "r")
        string = f.read()
        # Stores the indices and attendees
        dels = []
        namee = []

        # ans = ""
        for i in range(len(string)):
            
            # If opening delimiter
            # is encountered
            if (string[i] == '<') :
                dels.append(i + 2)

            # If closing delimiter
            # is encountered
            elif (string[i] == '>' and len(dels) != 0):

                # Extract the position
                # of opening delimiter
                pos = dels[-1]
                dels.pop()

                # Length of substring
                length = i - 1 - pos

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

        # *****Download file*****
        column_name = "Active_Attendees"
        with open('example.csv', mode='a', newline='') as file:

            # Create a writer object
            writer = csv.writer(file)

            # Write the data to the CSV file
            writer.writerow([column_name])

        
        df = pd.read_csv('example.csv')
        # Create a new list of values to insert into the column
        new_column_data = list(meet_attendees)

        # Append the new data to the desired column
        df[column_name] = df[column_name].append(pd.Series(new_column_data))

        # Write the updated DataFrame to a new CSV file
        df.to_csv('updated_example.csv', index=False)
        # **********************

    return render_template('attendees_result.html',
                            hour = hours,
                            minutes = minutes,
                            sec = secs,
                            meet_attendees_name =str(S),                           
                            total_att = len(meet_attendees),
                            file_name = transcript.filename
                           )

# Route for TextField Summarization
@app.route('/summarize_text',methods=['POST'])
def summarize_text():
    if request.method == 'POST':
        text_summary = request.form['text_summary']

        Summary = generate_summary(text_summary)

    return render_template('summary_result.html', 
                           text_summary=Summary)

# Route for File upload Summarization
@app.route('/summarize',methods=['POST'])
def summarize():
    
    if request.method == 'POST':
        
        #fetching file from html form
        text = request.files['fileUpload']
        text.save(text.filename)

        #for getting file extension
        find_file = text.filename
        x = find_file.split(".")
        extension = x[1]


        if extension == "pdf":
            reader = PdfReader(text.filename)

            page = reader.pages[0] #for single page
            # getting a all pages from the pdf file
            # page = len(reader.pages)

            # pdfReader = PyPDF2.PdfFileReader(text.filename)
            # # totalPages = pdfReader.numPages
  
            # # count number of pages
            # totalPages = len(pdfReader.pages)
            
            # print("hhhhhhhhhhhhhhhhhhhh", totalPages)

        
            # extracting text from page
            file_text = page.extractText()

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


        # if not request.form['numOfLines']:
        #     numOfLines = 3
        # else:
        #     numOfLines = int(request.form['numOfLines'])            

        # Calling function for summarzation
        Summary = generate_summary(file_text)
        
    return render_template('summary_result.html',
                               text_summary=Summary,
                            #    lines_original = original_length,
                            #    lines_summary = "numOfLines",
                               file_name = text.filename)

        # ******************END************************

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
    