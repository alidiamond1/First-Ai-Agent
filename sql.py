import sqlite3


conn = sqlite3.connect('student.db')

#cursor
cursor = conn.cursor()

#create table
table_info = """
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SELECTION VARCHAR(25), MARKS INT);
"""
cursor.execute(table_info)

cursor.execute("insert into STUDENT(NAME, CLASS, SELECTION, MARKS) values('John', '10th', 'Science', 90)")
cursor.execute("insert into STUDENT(NAME, CLASS, SELECTION, MARKS) values('Jane', '10th', 'Science', 90)")
cursor.execute("insert into STUDENT(NAME, CLASS, SELECTION, MARKS) values('Jim', '10th', 'Science', 90)")
cursor.execute("insert into STUDENT(NAME, CLASS, SELECTION, MARKS) values('Jill', '10th', 'Science', 90)")
cursor.execute("insert into STUDENT(NAME, CLASS, SELECTION, MARKS) values('Jack', '10th', 'Science', 90)")
cursor.execute("insert into STUDENT(NAME, CLASS, SELECTION, MARKS) values('Jill', '10th', 'Science', 90)")
cursor.execute("insert into STUDENT(NAME, CLASS, SELECTION, MARKS) values('Jill', '10th', 'Science', 90)")

#display
print("the inserted data is:")
data = cursor.execute('select * from STUDENT')
for row in data:
    print(row)

#commit the changes
conn.commit()

#close the connection
conn.close()

