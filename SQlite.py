import sqlite3

courses_information = [(1, 'python', '21.07.21', '21.08.21'), (2, 'java', '13.07.21', '16.08.21')]

students_information = [
(1, 'Max', 'Brooks', 24, 'Spb'),
(2, 'John', 'Stones', 15, 'Spb'),
(3, 'Andy', 'Wings', 45, 'Manhester'),
(4, 'Kate', 'Brooks', 34, 'Spb')]

student_courses_information = [
(1, 1),
(2, 1),
(3, 1),
(4, 2)]

class Table():
    def __init__(self, table_name, foreign = None, **settings):
        self.table_name = table_name
        self.settings = settings
        self.foreign = foreign

    def create(self, cursor):
        pie = ''.join('{} {},\n'.format(key, val) for key, val in self.settings.items())[:-2]
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}({pie})''')

    def is_empty(self, cursor):
        cursor.execute(f"SELECT count(*) FROM (select 1 from {self.table_name} limit 1);")
        option = cursor.fetchall()[0][0]
        if option == 0:
            return True
        else:
            False

    def add(self, cursor, data):
        for i in data:
            for k in data:
                if len(i)!=len(k):
                    print('Ошибка в заполнении данных')
                    break
        values = ('?, '*len(data[0]))[:-2]
        cursor.executemany(f'''INSERT INTO {self.table_name} VALUES({values})''', data)

    def request(self, cursor, term):
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE {term}")
        return cursor.fetchall()

students = Table(table_name='Students', id='INT UNIQUE', name='TEXT', surname='TEXT', age='INT', city='TEXT')
course = Table(table_name='Course', id='INT UNIQUE', name='TEXT NOT NULL', time_start='datetime', time_end='datetime')
students_courses = Table(table_name='Students_courses', student_id='INT', course_id='INT')

try:
    connection = sqlite3.connect('sqlite_database.db')
    cursor = connection.cursor()

    print("База данных создана и успешно подключена к SQLite")
    students.create(cursor)
    course.create(cursor)

    students_courses.create(cursor)
    if students.is_empty(cursor):
        students.add(cursor, students_information)
    if course.is_empty(cursor):
        course.add(cursor, courses_information)
    if students_courses.is_empty(cursor):
        students_courses.add(cursor, student_courses_information)
    connection.commit()

    students = students.request(cursor, term='age>30')
    print('Список студентов, старше 30:')
    for i in students:
        print(i[1]+' '+ i[2])
    cursor.close()
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (connection):
        connection.close()
        print("Соединение с SQLite закрыто")