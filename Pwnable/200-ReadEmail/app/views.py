from django.shortcuts import render, redirect

from hashlib import sha1
import random
import string

VICTIM_USERNAME = 'bruce'  # ccbf1fb417b28a6ea609d57af60f725d320e50bb
ATTACKER_USERNAME = 'pjsmith'
ATTACKER_PASSWORD = 'freire7f1'
EMAILS = {
    VICTIM_USERNAME: [('Your VHS Bank Account', 'answer_email.html')],
    ATTACKER_USERNAME: [('Good News Paul!', 'teste_email.html')    ],
}
KEY = '8760159ee5c703625c715d9ba0ec9219abc072915d25f6fcc67048e533f8bf3a'

SESSION_ID_COOKIE_NAME = 'sessionid'


def index(request):
    username = get_session_username(request)
    if username:
        subjects = [pair[0] for pair in EMAILS[username]]
        context = {'username': username, 'subjects': subjects}
        return render(request, 'email_list.html', context)
    return render(request, 'login.html')


def get_session_username(request):
    session_id = request.COOKIES.get(SESSION_ID_COOKIE_NAME, None)
    if session_id and ':' in session_id:
        username, token = session_id.rsplit(':', 1)
        if username in [VICTIM_USERNAME, ATTACKER_USERNAME]:
            correct_token = generate_session_token(username)
            if token == correct_token:
                return username
    return None


def generate_session_token(username):
    user_hash = sha1(username).digest()
    return stream_cipher(user_hash).encode('hex')


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    for c in username + password:
        if c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':
            return render(request, 'debug_error.html')
    if username == ATTACKER_USERNAME and password == ATTACKER_PASSWORD:
        session_cookie = '{0}:{1}'.format(username, generate_session_token(username))
        response = redirect('app.views.index')
        response.set_cookie(SESSION_ID_COOKIE_NAME, session_cookie)
        return response
    else:
        return redirect('app.views.error_auth')


def logout(request):
    response = redirect('app.views.index')
    username = get_session_username(request)
    if username:
        response.delete_cookie(SESSION_ID_COOKIE_NAME)
    return response


def stream_cipher(user_hash):
    key_hash = sha1(KEY).digest()
    return string_xor(key_hash,  user_hash)


def string_xor(s1, s2):
    result_list = []
    for c1, c2 in zip(s1, s2):
        result_list.append(chr(ord(c1) ^ ord(c2)))
    return ''.join(result_list)

def viewmail(request, email_id):
    username = get_session_username(request)
    if not username:
        return render_error(request, 'This page can only be seen if you login.')
    return render_email(request, username, email_id)


def render_email(request, username, email_id):
    try:
        email_id_int = int(email_id)
    except ValueError:
        return render_error(request, 'Mail with id {0} does not exist.'.format(email_id))

    if 0 < email_id_int <= len(EMAILS[username]):
        email_pair = EMAILS[username][email_id_int - 1]
        return render(request, email_pair[1], {'subject': email_pair[0], 'username': username})
    else:
        return render_error(request, 'Mail with id {0} does not exist.'.format(email_id))


def error_auth(request):
    return render_error(request, 'Bad Credentials!')


def render_error(request, error_message, context=None):
    if context is None:
        context = {}
    username = get_session_username(request)
    if username:
        context['username'] = username
    context['referer'] = request.META.get('HTTP_REFERER')
    context['error_message'] = error_message
    return render(request, 'error.html', context)
