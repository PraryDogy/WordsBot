import string
import sqlalchemy
from database import Dbase, Users, Words


def sort_words(input: tuple):
    unic_words = set(i[0] for i in input)
    result = []
    for word in unic_words:
        counter = 0
        for w, c in input:
            counter += c if word == w else False
        result.append((word, counter))
    return tuple(reversed(sorted(result, key=lambda x: x[1])))


def my_words(msg_user_id, msg_chat_id):
    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.user_id==msg_user_id, Words.chat_id==msg_chat_id).order_by(-Words.count)
    db_words = Dbase.conn.execute(q).fetchall()[:10]
    rowed = ''.join([f'{word}: {count}\n' for word, count in db_words])
    return 'Ваш топ 10 слов:\n\n' + rowed


def chat_words(msg_chat_id):
    q = sqlalchemy.select(Words.word, Words.count).where(
        Words.chat_id==msg_chat_id).order_by(-Words.count)
    db_words = Dbase.conn.execute(q).fetchall()
    sorted = sort_words(db_words)[:10]
    rowed = ''.join([f'{word}: {count}\n' for word, count in sorted])
    return 'Топ 10 слов чата\n\n' + rowed


def remove_restricted(input):
    restricted = (
        'это', 'что', 'так', 'все', 'как', 'там', 'меня', 'уже', 'вот', 
        'где', 'если', 'есть', 'раз', 'нет', 'мне', 'для', 
        'кто', 'они', 'она', 'тоже', 'чем', 'тебя',
        'его', 'зачем', 'топ', 'или', 
        'ещё', 'тут', 'был', 'нас',  'про', 'еще', 'вас', 'чего'
    )

    new_words = []
    for word in input:
        new_words.append(word) if word not in restricted else False
    
    return new_words


def get_words(text: str):
    new = text.translate(text.maketrans('', '', string.punctuation))
    new = new.replace('\n', ' ')
    whitespaces_split = new.split(' ')
    rem_whitespaces = [i.replace(' ', '') for i in whitespaces_split]
    lower_cases = [i.lower() for i in rem_whitespaces]
    restricted = remove_restricted(lower_cases)
    return tuple(i for i in restricted if len(i) > 2)


def write_db(msg_user_id, msg_chat_id, msg_words):
    msg_words = get_words(msg_words)

    query = sqlalchemy.select(Words.word, Words.chat_id).where(Words.user_id==msg_user_id)
    db_user_words = Dbase.conn.execute(query).fetchall()

    for word in msg_words:
        if (word, msg_chat_id) not in db_user_words:
            vals = {'word': word, 'count': 1, 'user_id': msg_user_id, 'chat_id': msg_chat_id}
            q = sqlalchemy.insert(Words).values(vals)
            Dbase.conn.execute(q)
        else:
            q = sqlalchemy.select(Words.count).where(
                Words.word==word, Words.user_id==msg_user_id, Words.chat_id==msg_chat_id)
            db_word_count = Dbase.conn.execute(q).first()[0]

            vals = {'count': db_word_count+1}
            q = sqlalchemy.update(Words).where(
                Words.word==word, Words.user_id==msg_user_id, Words.chat_id==msg_chat_id).values(vals)
            Dbase.conn.execute(q)


def users_list(data):
    user_ids = []
    users = []
    for id, name, _ in tuple(reversed(data)):
        if id not in user_ids:
            user_ids.append(id)
            users.append((id, name))
    return users


def new_user(msg_user_id: int, msg_user_name: str):
    vals = {'user_id': msg_user_id, 'user_name': msg_user_name}
    new_user = sqlalchemy.insert(Users).values(vals)
    Dbase.conn.execute(new_user)


def update_name(input_user_id, new_user_name):
    print('update name')
    vals = {'user_name': new_user_name}
    new_name = sqlalchemy.update(Users).where(
        Users.user_id==input_user_id).values(vals)
    Dbase.conn.execute(new_name)


def check_user(msg_user_id: int, msg_user_name: str):
    get_user = sqlalchemy.select(
        Users.user_id, Users.user_name).filter(Users.user_id == msg_user_id)
    db_user = Dbase.conn.execute(get_user).first()
    
    if db_user is not None:
        db_usr_id, db_usr_name = db_user
        if db_usr_name != msg_user_name:
            update_name(db_usr_id, msg_user_name)
    else:
        new_user(msg_user_id, msg_user_name)


