# save pdf file
import requests, os, re, json

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
login_url = 'https://moodle.boun.edu.tr/login/index.php'

credentials_path = f'{THIS_DIR}/moodle_credentials.json'
if not os.path.exists(credentials_path):
    print('Your credentials were not found.')
    should_exit = True
    response = input('If you would like to provide them now, enter y; otherwise n: ')
    username, password = 'Username', 'Password'
    if response == 'n':
        print('You need to add your credentials in "credentials.json" in the script folder.')
    elif response == 'y':
        username = input('Please enter your username: ')
        password = input('Please enter your password: ')
        should_exit = False
    else:
        print('Not a valid input. You need to add your credentials in "credentials.json" in the script folder.')
    with open(credentials_path, 'w', encoding='utf-8') as f:
        f.write('{"username": "%s", "password": "%s"}' % (username, password))
    if should_exit: exit()
with open(credentials_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    if data['username'] == 'Username' or data['password'] == 'Password':
        print('You need to add your credentials in "credentials.json" in the script folder.'); exit()

folder_path = f'{THIS_DIR}/Moodle Resources'
if not os.path.exists(folder_path): os.mkdir(folder_path)

with requests.session() as sess:
    login_post = sess.post(login_url, data=data)
    course_req = sess.get(input('Please provide the course URL: '))
    pdf_pattern = 'href="(https://moodle.boun.edu.tr/mod/resource.*?)".*?class="instancename">(.*?)<span'
    for pdf in re.findall(pdf_pattern, course_req.text):
        pdf_url, pdf_name = pdf
        pdf_req = sess.get(pdf_url)
        with open(f'{folder_path}/{pdf_name}.pdf', 'wb') as f:
            f.write(pdf_req.content)
