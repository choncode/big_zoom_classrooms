import csv
import re
import os, os.path

def sem_pair_converter(sem_pair_file):
    '''
    Opens the sem_*.csv, iterates through each row to remove 
    the line break `\t`, adds a delimiter and returns a list that Python can use.
    '''
    # could add argument in func to change the file path dynamically
    with open(f'./data/sem_pairs/{sem_pair_file}', encoding='utf-8') as c:
        reader = csv.reader(c, delimiter=',')
        mentee_data_list = []
        for row in reader:
            mentee_data_list.append(row)

        formatted_mentee_data_list = []
        
        for mentees in mentee_data_list:
            mentees[0] = re.sub(r'null@null.com', ', null@null.com', mentees[0])
            mentees[0] = re.sub('\t', '', mentees[0])
            mentees = mentees[0].split(', ')
            formatted_mentee_data_list.append(mentees)

    return formatted_mentee_data_list


def create_mega_classroom_csv():

    print('type the number of seminars to combine')
    sem_count = int(input())
    print('checking if you have sufficient sem csvs in sem_pairs dir...')
    sem_dir = './data/sem_pairs/'
    file_count = len([name for name in os.listdir(sem_dir) if os.path.isfile(f'{sem_dir}{name}')])

    if sem_count != file_count:
        print('you do not have the correct matching amount of files in ./data/sem_pairs')
        print(f'you have said {sem_count} seminars but there are {file_count} files in the dir')
        print('please add/delete to have matching number of files in the format of "sem_1.csv", "sem_2.csv"...')
        return
    
    print('sufficient sem csvs found!')
    
    print('type a name for your tutor room')
    tutor_room_name = input()
    mega_classroom_list = [
        ['Pre-assign Room Name', 'Email Address'],
        [tutor_room_name, 'null@null.com']
    ]
    for i in range(1, file_count + 1):
        print(f'converting data for seminar {i}...')
        mega_classroom_list.append([f'Seminar {i}', 'null@null.com'])
        sem_students_list = sem_pair_converter(f'sem_{i}.csv')
        for student in sem_students_list:
            sem_prefix = f'S{i} - {student[0]}'
            mega_classroom_list.append([sem_prefix, student[1]])
    print('how many tutor rooms do you need?')
    tutor_room_count = int(input())
    for i in range(1, tutor_room_count + 1):
        if i < 10:
            mega_classroom_list.append([f'Room 10{i}', 'null@null.com'])
        else: mega_classroom_list.append([f'Room 1{i}', 'null@null.com'])

    with open(f'./output/mega_classroom.csv', 'a', encoding='utf-8') as c:
        writer_obj = csv.writer(c)
        for room_name in mega_classroom_list:
            writer_obj.writerow(room_name)
        print('creating output csv file...')
        print('done! please check the output directory for mega_classroom.csv')

create_mega_classroom_csv()
