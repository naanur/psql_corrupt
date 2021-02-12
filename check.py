import psycopg2



# целевая Таблица
target_table = ""
# target_table = ""
target_database = ""
# ШАГ ЧТЕНИЯ
step = 100
password = ""
host = "localhost"

def get_conn():
    # Новое подключение. После ошибки чтения коннект закрывается, приходится открывать новое
    # Настройка подключения к базе данных
    return psycopg2.connect(database=target_database, 
        user="postgres", 
        password=password, 
        host=host)


def get_id(offset):
    # Получаем id битой строки
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(f"""SELECT id FROM {target_table} ORDER BY id ASC LIMIT 1 OFFSET {offset}""")
        id = cur.fetchone()[0]
        print(id)
        return id


def delete_by(id):
    # Удаляем битую строку
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(f"""DELETE FROM {target_table} WHERE id = '{id}'""")
        conn.commit()
        print(id, 'deleted')


def select(limit, offset):
    # Запрос на чтение (лимит, откуда отсчёт)
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            cursor.execute(f"""SELECT * FROM {target_table} ORDER BY id ASC LIMIT {limit} OFFSET {offset}""")
            result = cursor.fetchone()
            print(limit, offset)
            return True
    except psycopg2.errors.InternalError_:
        return False


def get_max_objects():
    # Считаем сколько всего строк в таблице
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.execute(f"""SELECT count(*) FROM {target_table}""")
        maximum = cursor.fetchone()[0]
        
        return int(maximum)


if __name__ == '__main__':
    print(f"Начинаем перебор {target_table} из {target_database}")

    offset = 0
    limit = step
    
    m = get_max_objects()
    print('MAX: ', m)
    # Начинаем перебор
    while offset < m:
        
        if select(limit, offset):
            # Если доступно на чтение, то добавляем к офсету лимит, и проверяем следующие
            offset += limit
        else:
            # Если не доступно, лимит разбиваем на два и ищем битую строку до limit == 1
            limit = int(limit / 2)
            print('уменьшаем лимит', limit)
            
            if limit == 1:
                # строука нашлась, удаляем.
                id = get_id(offset)
                delete_by(id)
                limit = step
            
