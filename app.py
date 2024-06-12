from flask import Flask, request, render_template
import requests, smtplib, json, os
from dotenv import load_dotenv 

# Loading environment variables
load_dotenv('.env')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def load_form():
    return render_template('form.html')

@app.route('/sendEmail', methods=['POST'])
def sendEmail():
    emailid = request.form['email']
    inputs = f'Token Name: {request.form["name"]}; Project Description: {request.form["desc"]}; Problem Statement & Solution: {request.form["prob"]}.'
    print(inputs)
    prompt = "You are an expert in the web3 space. You will now be given details of a token, and you must analyze each piece of data separately, and also give a score to each of them between 1 to 10."
    URL = "https://api.openai.com/v1/chat/completions"
    apiKey = os.getenv('api')
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f'{inputs+prompt}'}],
        "temperature" : 1.0,
        "top_p":1.0,
        "n" : 1,
        "stream": False,
        "presence_penalty":0,
        "frequency_penalty":0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {apiKey}"
    }

    response = requests.post(URL, headers=headers, json=payload, stream=False).json()
    print(response)
    if 'error' in response.keys():
        return response['error']
    elif 'choices' in response.keys():
        result = response['choices'][0]['message']['content'].strip()
        print(result)

        #Email
        s = smtplib.SMTP('smtp.gmail.com', 587)           # Starting session
        s.starttls()                                      # Starting TLS for security
        s.login(os.getenv('gmail'), os.getenv('gpw'))      # Authentication
        s.sendmail(os.getenv('gmail'), emailid, result)  # Sending
        s.quit()    
    return 'Response sent!'

# Running the application
if __name__ == '__main__':
    #port = int(sys.argv[1])
    app.run(debug=True) #, host="0.0.0.0", port=port