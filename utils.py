import string
import sqlalchemy
from database import Dbase, Users, Words

def get_words(text: str):
    new = text.translate(text.maketrans('', '', string.punctuation))
    new = new.replace('\n', ' ')
    whitespaces_split = new.split(' ')
    rem_whitespaces = [i.replace(' ', '') for i in whitespaces_split]
    return tuple(i for i in rem_whitespaces if len(i) > 2)



def write_db(msg_user_id, msg_user_name, msg_words):
    words = get_words(msg_words)

    query = sqlalchemy.select(Words.word, Words.count).where(Words.user_id==msg_user_id)
    db_user_words = Dbase.conn.execute(query).fetchall()

    db_words = [i[0] for i in db_user_words]
    db_counts = [i[1] for i in db_user_words]

    for w in words:
        if w not in db_words:
            vals = {'word': 'second word', 'count': 1, 'user_id': msg_user_id}
            q = sqlalchemy.insert(Words).values(vals)
            Dbase.conn.execute(q)

        else:
            ind = db_words.index(w)
            db_counts[ind] += 1



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


