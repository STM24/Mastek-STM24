from flask import Flask, Response, request, jsonify, render_template
from final_summary import *
from Meeting_duration import *
from PyPDF2 import PdfReader
import PyPDF2
from transformers import pipeline
import docx
import webvtt
import csv
import pandas as pd
import io
import random
import string
import os


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

meet_attendee_list = []
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

        global meet_attendee_list
        meet_attendee_list = list(meet_attendees)

        S = ', '.join(meet_attendees)
        # file = open("Active_Attendees.txt","w")

        # file.write("Total Active attendees: ")
        # file.write(str(len(meet_attendees)))

        # file.write("\nTotal Active attendees Name: \n")

        # file.write(str(S))
        # file.close()

        # ***************************Download file********************
        # column_name = "Active_Attendees"
        # with open('example.csv', mode='a', newline='') as file:

        #     # Create a writer object
        #     writer = csv.writer(file)

        #     # Write the data to the CSV file
        #     writer.writerow([column_name])

        
        # df = pd.read_csv('example.csv')
        # # Create a new list of values to insert into the column
        # new_column_data = list(meet_attendees)

        # # Append the new data to the desired column
        # df[column_name] = df[column_name].append(pd.Series(new_column_data))

        # # Write the updated DataFrame to a new CSV file
        # df.to_csv('updated_example.csv', index=False)
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
summary_string = ""
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

        #convert list into string
        global summary_string
        summary_string = ' '.join(Summary)    
    return render_template('summary_result.html',
                               text_summary=summary_string,
                            #    lines_original = original_length,
                            #    lines_summary = "numOfLines",
                               file_name = text.filename)

        # ******************END************************



@app.route('/download_csv')
def download_csv():
    # Define the data to be included in the CSV file
    # data = [['Name'],
    #         ['COMP_TY_B_63_MOHAMMED_ADIL_KHATRI'],
    #         ['COMP_TY_B_66_SHUBHAM_KANOJIYA'],
    #         ['COMP_SY_B_60_HARSH_CHOTALIYA'],
    #         ['Samantha']
    #         ]
    
    insert_data = ["Active_attendees"]
    insert_data.extend(meet_attendee_list)

    insert_names= [[x] for x in insert_data]

    # Create a buffer to write the CSV data to
    output = io.StringIO()

    # Use the csv module to write the data to the buffer
    writer = csv.writer(output)
    for row in insert_names:
        writer.writerow(row)

    # Set the appropriate response headers
    response = Response(output.getvalue(), mimetype='text/csv')

    # *******Generate random file name***
    # Generate a sequence of 8 random characters (4 letters and 4 numbers)
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

    # Insert an underscore after every 4 characters
    result = '_'.join([random_chars[i:i+4] for i in range(0, len(random_chars), 4)])
    file_name = "Attendance_" + result +".csv"
 
    # ************************
    response.headers.set("Content-Disposition", "attachment", filename=file_name)

    return response


# ***********************Download Summary***************************
@app.route('/download_summary')
def download_summary():
    # Add a summary in the file
    
    # Delete a file
    os.remove('summary.txt')

    with open('summary.txt', 'a') as f:
        f.write(summary_string + '\n')
    # return 'Data added successfully!'

    with open('summary.txt', 'r') as f:
        data = f.read()
    return Response(
        data,
        mimetype="text/plain",
        headers={"Content-disposition":
                 "attachment; filename=summary.txt"})
# ****************************************************************
if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
    
