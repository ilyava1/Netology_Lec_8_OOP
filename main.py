# Домашнее задание к лекции «Объекты и классы.
# Инкапсуляция, наследование и полиморфизм»

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        """Добавляет курс в список курсов, находящихся в процессе изучения
           студента."""

        self.courses_in_progress.append(course_name)

    def rate_lecturer(self, lecturer, course, grade):
        """Реализует выставление оценки лектору за курс."""

        if (isinstance(lecturer, Lecturer)
            and course in lecturer.courses_attached
                and course in self.courses_in_progress):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_hw_grade(self):
        """Реализует расчет средней оценки студента по всем домашним заданиям
           по всем курсам.

           Вычисленная оценка округляется до 1-го знака после запятой."""

        grades_quantity = 0
        grades_sum = 0
        for course in self.grades:
            for grade in self.grades[course]:
                grades_quantity += 1
                grades_sum += grade
        ahwg = round(grades_sum/grades_quantity, 1)
        return ahwg

    def courses_in_prog(self):
        """Реализует формирование строки с перечнем курсов, находящихся
           в процессе изучения студентом."""

        cinp = ''
        for course in self.courses_in_progress:
            if cinp != '':
                cinp += ', '
            cinp += course
        if cinp == '':
            cinp = 'нет'
        return(cinp)

    def finish_courses(self):
        """Реализует формирование строки с перечнем завершенных студентом
           курсов."""

        fc = ''
        for course in self.finished_courses:
            if fc != '':
                fc += ', '
            fc += course
        if fc == '':
            fc = 'нет'
        return(fc)

    def __str__(self):
        return (f'Имя: {self.name} \n'
                f'Фамилия: {self.surname} \n'
                f'Средняя оценка за домашние задания: '
                f'{self.average_hw_grade()} \n'
                f'Курсы в процессе изучения: {self.courses_in_prog()} \n'
                f'Завершенные курсы: {self.finish_courses()}')

    def __eq__(self, other):
        return (self.average_hw_grade() == other.average_hw_grade())

    def __gt__(self, other):
        return (self.average_hw_grade() > other.average_hw_grade())


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def add_courses(self, course_name):
        """Добавляет курс в список курсов ментора"""

        self.courses_attached.append(course_name)


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.average_grade = 0

    def average_lec_rating(self):
        """Вычисляет среднюю оценку лектора по всем его курсам.

           Метод суммирует все оценки лектора по всем его курсам
           и вычисляет среднюю."""

        grades_quantity = 0
        grades_sum = 0
        for course in self.grades:
            for grade in self.grades[course]:
                grades_quantity += 1
                grades_sum += grade
        alr = round(grades_sum/grades_quantity, 1)
        return alr

    def __str__(self):
        return (f'Имя: {self.name} \n'
                f'Фамилия: {self.surname} \n'
                f'Средняя оценка за лекции: {self.average_lec_rating()}')

    def __eq__(self, other):
        return (self.average_lec_rating() == other.average_lec_rating())

    def __gt__(self, other):
        return (self.average_lec_rating() > other.average_lec_rating())


class Reviewer(Mentor):

    def rate_hw(self, student, course, grade):
        """Реализует выставление оценки студенту за домашнее задание
           по курсу."""

        if (isinstance(student, Student)
            and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f'Имя: {self.name} \n'
                f'Фамилия: {self.surname}')


def compare_lecturers(lecturers):
    """Реализует формирование и вывод на печать рейтинга лекторов на основании

       На вход метод получает список лекторов.
       Формирует словарь Лектор - средняя оценка.
       Формирует отсортированный по возрастанию список средних оценок.
       Формирует новый словарь Лектор - средняя оценка отсортированный
       по возрастанию средней оценки.
       Выводит полученный словарь на печать в обратном порядке (по уменьшению
       средней оценки лекторов."""

    unsorted_lecturers = {}
    sorted_lecturers = {}
    for lecturer in lecturers:
        unsorted_lecturers[lecturer.name + ' '
                           + lecturer.surname] = lecturer.average_lec_rating()
    sorted_grades = sorted(unsorted_lecturers.values())
    for grade in sorted_grades:
        for lecturer in unsorted_lecturers.keys():
            if unsorted_lecturers[lecturer] == grade:
                sorted_lecturers[lecturer] = unsorted_lecturers[lecturer]
    print('Рейтинг лекторов по средним оценкам за лекции:')
    place = 1
    for lecturer, grade in reversed(sorted_lecturers.items()):
        print(f'{place}. {lecturer} - {grade}')
        place += 1
    return


def compare_students(students):
    """Реализует формирование и вывод на печать рейтинга лекторов на основании

       На вход метод получает список студентов.
       Формирует словарь Студент - средняя оценка.
       Формирует отсортированный по возрастанию список средних оценок.
       Формирует новый словарь Студент - средняя оценка, отсортированный
       по возрастанию средней оценки.
       Выводит полученный словарь на печать в обратном порядке (по уменьшению
       средней оценки студентов."""

    unsorted_students = {}
    sorted_students = {}
    for student in students:
        unsorted_students[student.name + ' '
                          + student.surname] = student.average_hw_grade()
    sorted_grades = sorted(unsorted_students.values())
    for grade in sorted_grades:
        for student in unsorted_students.keys():
            if unsorted_students[student] == grade:
                sorted_students[student] = unsorted_students[student]
    print('Рейтинг студентов по средним оценкам за ДЗ:')
    place = 1
    for student, grade in reversed(sorted_students.items()):
        print(f'{place}. {student} - {grade}')
        place += 1
    return


def average_hw_grade_for_all_students(students, course_1):
    """Реализует подсчет средней оценки за домашние задания по всем студентам
       в рамках конкретного курса.

       На вход метод получает список экземпляров класса Студент и курс."""

    grades_quantity = 0
    grades_sum = 0
    for student in students:
        for course in student.grades:
            if course == course_1:
                for grade in student.grades[course]:
                    grades_quantity += 1
                    grades_sum += grade
    if grades_quantity != 0:
        ahwg_allst = round(grades_sum / grades_quantity, 1)
    else:
        ahwg_allst = None
    return ahwg_allst


def average_grade_for_all_lecturers(lecturers, course_1):
    """Реализует подсчет средней оценки за лекции по всем лекторам
       в рамках конкретного курса.

       На вход метод получает список экземпляров класса Лектор и курс."""

    grades_quantity = 0
    grades_sum = 0
    for lecturer in lecturers:
        for course in lecturer.grades:
            if course == course_1:
                for grade in lecturer.grades[course]:
                    grades_quantity += 1
                    grades_sum += grade
    if grades_quantity != 0:
        ag_alllec = round(grades_sum / grades_quantity, 1)
    else:
        ag_alllec = None
    return ag_alllec


# Согласно Заданию №4 создаем по 2 экз каждого класса
# (студенты, лекторы, проверяющие):
first_student = Student('Ivan', 'Susanin', 'male')
first_student.courses_in_progress += ['Python', 'Git']
first_student.finished_courses += ['SQL']

second_student = Student('Petr', 'Tolstoy', 'male')
second_student.courses_in_progress += ['Python', 'Git']

cool_lecturer = Lecturer('Guido', 'van Rossum')
cool_lecturer.courses_attached += ['Python']

hot_lecturer = Lecturer('Pavel', 'Durov')
hot_lecturer.courses_attached += ['Git', 'Python']

cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached += ['Python', 'Git']

hot_reviewer = Reviewer('Strange', 'Buddy')
hot_reviewer.courses_attached += ['Python', 'Git']

# Проверяющие ставят оценки студентам за ДЗ (Задание №2):
cool_reviewer.rate_hw(first_student, 'Python', 8)
cool_reviewer.rate_hw(first_student, 'Python', 9)
cool_reviewer.rate_hw(first_student, 'Python', 10)

hot_reviewer.rate_hw(first_student, 'Git', 8)
hot_reviewer.rate_hw(first_student, 'Git', 10)
hot_reviewer.rate_hw(first_student, 'Git', 9)

hot_reviewer.rate_hw(second_student, 'Python', 8)
hot_reviewer.rate_hw(second_student, 'Python', 9)
hot_reviewer.rate_hw(second_student, 'Python', 10)

cool_reviewer.rate_hw(second_student, 'Git', 8)
cool_reviewer.rate_hw(second_student, 'Git', 10)
cool_reviewer.rate_hw(second_student, 'Git', 10)

# Студенты ставят оценки лекторам за лекции (Задание №2):
first_student.rate_lecturer(cool_lecturer, 'Python', 8)
first_student.rate_lecturer(cool_lecturer, 'Python', 10)
first_student.rate_lecturer(cool_lecturer, 'Python', 10)

second_student.rate_lecturer(hot_lecturer, 'Git', 8)
second_student.rate_lecturer(hot_lecturer, 'Git', 10)
second_student.rate_lecturer(hot_lecturer, 'Python', 10)

# Проверяем работу метода __str__ у всех классов
# согласно требованиям п.1 Задания №3
print('Проверяющие:')
print(cool_reviewer)
print()

print('Лекторы:')
print(cool_lecturer)
print()
print(hot_lecturer)
print()

print('Студенты:')
print(first_student)
print()
print(second_student)
print()

# Сравниваем лекторов по средней оценке за лекции:
# строим рейтинг по убыванию средней (опционально, нет в задании)
lecturers = [cool_lecturer, hot_lecturer]
compare_lecturers(lecturers)

# Сравниваем лекторов через оператор сравнения, как требуется в п.2 Задания №3
# с использованием магических методов __gt__ и __eq__
if cool_lecturer > hot_lecturer:
    print(f'{cool_lecturer.name} {cool_lecturer.surname}'
          f' - лидирует в рейтинге!')
elif cool_lecturer == hot_lecturer:
    print('Наши лекторы не уступают друг другу!')
else:
    print(f'{hot_lecturer.name} {hot_lecturer.surname} - лидирует в рейтинге!')
print()

# Сравниваем студентов по средней оценке за ДЗ
# строим рейтинг по убыванию средней (опционально, нет в задании)
students = [first_student, second_student]
compare_students(students)

# Сравниваем студентов через оператор сравнения, согласно п.2 Задания №3
# с использованием магических методов __gt__ и __eq__
if first_student > second_student:
    print(f'{first_student.name} {first_student.surname}'
          f' - лидирует в рейтинге!')
elif first_student == second_student:
    print('Наши студенты не уступают друг другу!')
else:
    print(f'{second_student.name} {second_student.surname}'
          f' - лидирует в рейтинге!')
print()

# Расчет средней оценки студентов за ДЗ и лекторов в рамках конкретного курса
# (п. 1-2 Задания №4):
print()
course = input('Введите курс чтобы узнать средние оценки студентов \
и лекторов: ')
result_for_students = average_hw_grade_for_all_students(students, course)
if result_for_students is not None:
    print(f'Средняя оценка студентов за ДЗ в рамках курса {course}:')
    print(result_for_students)
else:
    print('Ошибка. У студентов нет такого курса в плане!')

result_for_lecturers = average_grade_for_all_lecturers(lecturers, course)
if result_for_lecturers is not None:
    print(f'Средняя оценка лекторов за лекции в рамках курса {course}:')
    print(result_for_lecturers)
else:
    print('Ошибка. У лекторов нет такого курса в плане!')
