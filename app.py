#import required library

from flask import Flask, render_template, request
import openai

app = Flask(__name__, template_folder='templates')
openai.api_key = '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'

#create prompt for feedback
resume_prompt = """
Prompt: Provide feedback on the following resume:
Resume:
{{resume}}
Feedback:
"""


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return "No file part"

    resume_file = request.files['resume']

    if resume_file.filename == '':
        return "No selected file"

    def read_resume_content(resume_file):
        encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
        for encoding in encodings:
            try:
                resume_content = resume_file.read().decode(encoding)
                return resume_content
            except UnicodeDecodeError:
                pass
        # if no encoding works,raise an error or handle it accordingly
        raise UnicodeDecodeError("Unable to decode file using supported encodings")
    resume_content = read_resume_content(resume_file)

    #generate feedback
    feedback = generate_feedback(resume_content)
    return feedback

def generate_feedback(resume_content):
    prompt = resume_prompt.replace('{{resume}}', resume_content)
    response = openai.Completion.create(
        engine="text-embedding-ada-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=200
    )
    feedback = response.choices[0].text.strip()
    return feedback

if __name__ == '__main__':
    app.run(debug=True)
