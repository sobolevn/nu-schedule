#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TODO: linking

# built-in
from collections import defaultdict
from itertools import groupby, product, chain, combinations
from logging import basicConfig, DEBUG, info
from re import compile as compiles
from sys import exit, argv
from time import strptime
from datetime import datetime

# imports
from tabulate import tabulate
import xlrd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QComboBox, QDesktopWidget,
                             QDialogButtonBox, QFileDialog, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QFrame)
from PyQt5.QtCore import Qt

# Simple logging suite
basicConfig(
    filename='main.log',
    level=DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p')

# Regex expression to manage course sections
reg = compiles('(?:\d+)([a-zA-Z]+)')
# Enumeration of days
table = {'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4, 'S': 5, '*': 6}

###############################################################################


class Course():

    """Models courses as a class"""

    def __init__(self, abbr, st, title, credit, days, timing, teacher, room):
        self.abbr = str(abbr)
        self.st = str(st)
        self.title = str(title)
        self.credit = str(credit)
        self.days = str(days)
        self.timing = str(timing)
        self.teacher = str(teacher)
        self.room = str(room)

        if self.timing != '*':
            a, b = self.timing.split('-')
            self.start, self.end = strptime(
                a, "%I:%M %p"), strptime(b, "%I:%M %p")
        else:
            self.start, self.end = str(), str()
        self.dayslist = [table.get(i) for i in table if i in self.days]

    def __repr__(self):
        return str(self.abbr + ' | ' + self.st + ' | ' + self.title +
                   ' | ' + self.credit + ' | ' + self.days + ' | ' + self.timing + ' | ' +
                   self.teacher + ' | ' + self.room)

    def __and__(self, other):
        """ Intersection check """

        if 6 in set(self.dayslist) or 6 in set(other.dayslist):
            return False

        if not set.intersection(set(self.dayslist), set(other.dayslist)):
            return False
        else:
            return self.start <= other.end and self.end >= other.start

###############################################################################


class UI(QWidget):

    """Simple Qt UI"""

    coursesconnector = list()
    finallist = list()

    def __init__(self, parent=None):
        """ Initializing """

        super(UI, self).__init__(parent)
        self.initui()

    def center(self):
        """ Centering magick """

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_about_clicked(self):
        """ About pop-up """

        d = QDialog()
        l1 = QLabel(
            "nu-schedule\n\nA course schedule generator for the Nazarbayev University\nHomepage: https://github.com/ac130kz/nu-schedule\nApache 2.0 License\n\n© Mikhail Krassavin, 2018")
        b1 = QPushButton('Ok', d)
        vbox = QVBoxLayout()
        vbox.addWidget(l1)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(b1)
        hbox.addStretch()
        vbox.addItem(hbox)
        d.setWindowIcon(QIcon('res/logo.ico'))
        d.setWindowTitle("About")
        d.setLayout(vbox)
        b1.clicked.connect(d.accept)
        d.exec_()

    def on_help_clicked(self):
        """ Help pop-up """

        d = QDialog()
        l1 = QLabel("1. Get a clearly formatted xlsx/xls with courses\nfor this I recommend a program called PDF2XL,\nhave a look at the sample lists in the /samples/ folder.\n\n2. Select your prepared xlsx/xls file with the |Open| button,\nto load the courses into the app\n\n3. With |Edit| button access the selection menu,\nadded courses will appear on the Main window.\n\n4. Use |Generate| button to generate and\n save your schedule as result<unixtimestamp>.txt")
        b1 = QPushButton("Ok", d)
        vbox = QVBoxLayout()
        vbox.addWidget(l1)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(b1)
        hbox.addStretch()
        vbox.addItem(hbox)
        d.setWindowIcon(QIcon('res/logo.ico'))
        d.setWindowTitle("Help")
        d.setLayout(vbox)
        b1.clicked.connect(d.accept)
        d.exec_()

    def on_edit_clicked(self):
        """ Editing course selection """

        if self.coursesconnector:
            d = QDialog()
            add = QPushButton("Add", d)
            delete = QPushButton("Delete", d)
            cmb1 = QComboBox()
            cmb1.addItems(sorted([t[0] for t in self.coursesconnector]))
            hbox = QHBoxLayout()
            hbox.addWidget(cmb1)
            hbox.addStretch()
            hbox.addWidget(add)
            hbox.addWidget(delete)
            hbox.addStretch()
            d.setWindowIcon(QIcon('res/logo.ico'))
            d.setWindowTitle("Adding courses")
            d.setLayout(hbox)
            add.clicked.connect(
                lambda: self.on_add_clicked(cmb1.currentText()))
            delete.clicked.connect(
                lambda: self.on_delete_clicked(cmb1.currentText()))
            d.exec_()

    def get_finallistsize(self):
        """ Updating the info on the selection list """

        if not self.finallist:
            data = "empty"
        else:
            data = str(set(y[0].abbr for y in self.finallist))
        self.label.setText("Your selection is: \n" + data)

    def fail_dialog(self):
        """ Is triggered if schedules cannot be created """

        d = QDialog()
        b1 = QPushButton("Ok", d)
        lbl1 = QLabel("Cannot create a schedule with these subjects")
        vbox = QVBoxLayout()
        vbox.addWidget(lbl1)
        vbox.addStretch()
        vbox.addWidget(b1)
        vbox.addStretch()
        d.setWindowTitle("Failed")
        d.setLayout(vbox)
        b1.clicked.connect(d.accept)
        d.setWindowIcon(QIcon('res/logo.ico'))
        self.get_finallistsize()
        d.exec_()

    def success_dialog(self, desc):
        """ Is triggered if schedules were created """

        d = QDialog()
        b1 = QPushButton("Ok", d)
        lbl1 = QLabel('Results successfully saved as result' + desc + '.txt')
        vbox = QVBoxLayout()
        vbox.addWidget(lbl1)
        vbox.addStretch()
        vbox.addWidget(b1)
        vbox.addStretch()
        d.setWindowTitle("Success")
        d.setLayout(vbox)
        b1.clicked.connect(d.accept)
        d.setWindowIcon(QIcon('res/logo.ico'))
        self.get_finallistsize()
        d.exec_()

    def empty_dialog(self):
        """ Is triggered if course selection is empty """

        d = QDialog()
        b1 = QPushButton("Ok", d)
        lbl1 = QLabel('Your selection of courses is empty')
        vbox = QVBoxLayout()
        vbox.addWidget(lbl1)
        vbox.addStretch()
        vbox.addWidget(b1)
        vbox.addStretch()
        d.setWindowTitle("Selection empty")
        d.setLayout(vbox)
        b1.clicked.connect(d.accept)
        d.setWindowIcon(QIcon('res/logo.ico'))
        d.exec_()

    def on_add_clicked(self, text):
        """ Course addition functionality """

        if not any(text == x[0].abbr for x in self.finallist):
            for k, v in self.coursesconnector:
                if k == text:
                    for i in v:
                        self.finallist.append(i)

            self.get_finallistsize()

    def on_delete_clicked(self, text):
        """ Course deletion functionality """

        self.finallist = [x for x in self.finallist if text != x[0].abbr]
        self.get_finallistsize()

    def on_open_clicked(self):
        """ File openning procedure """

        try:
            self.label.setText('Loading... Please wait')
            name = QFileDialog.getOpenFileName(self, 'Open File')

            book = xlrd.open_workbook(str(name[0]))
            sheet = book.sheet_by_index(0)

            if self.checkxl(sheet):
                info('Input file ' + str(name[0]) + ' was successfully read.')

                courses = list()

                for i in range(1, sheet.nrows):
                    courses.append(Course(
                        sheet.cell_value(i, 0), sheet.cell_value(
                            i, 1), sheet.cell_value(i, 2), sheet.cell_value(i, 4),
                        sheet.cell_value(i, 7), sheet.cell_value(i, 8), sheet.cell_value(i, 11), sheet.cell_value(i, 12)))

                self.label.setText('File successfully loaded')
                courses = self.groupabbr(courses)
                self.coursesconnector = courses

        except FileNotFoundError:
            self.label.setText('Problems with the input file')
            info('Problems with the input file')
        except Exception as e:
            print(str(e))
            info('Caught the following exception ' + str(e))

    def on_gen_clicked(self):
        """ Results output """

        if self.finallist:
            self.label.setText('Generating schedule...')
            info('Generating schedule for ' + str(self.finallist))
            outlist = [p for p in product(
                *self.finallist) if not any(one & two for one, two in combinations(p, 2))]
            temp = 1
            d = str(datetime.utcnow().timestamp())

            if outlist:
                with open('result' + d + '.txt', 'w') as file:
                    for k in outlist:
                        file.write('Schedule #' + str(temp) + '\n')
                        headers = ['Abbreviation', 'Section', 'Title',
                                   'ECTS Credits', 'Days', 'Time', 'Teacher', 'Room']

                        file.write(tabulate([[elem.__dict__['abbr'], elem.__dict__['st'], elem.__dict__['title'], elem.__dict__['credit'], elem.__dict__['days'],
                                              elem.__dict__['timing'], elem.__dict__['teacher'], elem.__dict__['room']] for elem in list(k)], headers, tablefmt="grid"))
                        file.write('\n\n')
                        temp = temp + 1
                self.success_dialog(d)
                info('Results are ' + str(outlist))
                info('Results successfully saved as result' + d + '.txt')
            else:
                self.fail_dialog()
                info('Cannot create a schedule with these courses')
        else:
            self.empty_dialog()
            info('List to generate schedule is assumed to be zero and it is currently ' +
                 str(self.finallist))

    def checkxl(self, sheet):
        """ A simple check to compare the input file's properties to the "standard's" """

        return str(sheet.cell_value(0, 0)) == 'Course Abbr' and sheet.ncols == 13

    def groupabbr(self, inlist):
        """ Forms a list of course lists based on the course abbreviation and section (s/t) """

        result = defaultdict(lambda: defaultdict(list))

        for obj in inlist:
            result[obj.abbr][reg.search(obj.st).group(1)].append(obj)

        inlist = [(list(r.values())[0][0].abbr, list(r.values()))
                  for r in result.values()]
        info('Courses were sorted')

        return inlist

    def initui(self):
        """ Main window UI """

        # Defining labels
        # -------------------------------------
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        if not self.finallist:
            self.label.setText('File is not loaded')

        # Defining buttons
        # -------------------------------------
        info('Defining buttons')
        open_button = QPushButton("Open xlsx/xls and load it")
        edit_button = QPushButton("Edit needed courses")
        help_button = QPushButton("Help")
        about_button = QPushButton("About")
        gen_button = QPushButton("Generate!")
        gen_button.setStyleSheet(
            'QPushButton {background-color: #c7f439; color: red; font-size: 50px;}')

        # Dealing with the interface of the app
        # -------------------------------------
        grid = QGridLayout()
        grid.addWidget(open_button)
        grid.addWidget(edit_button)
        grid.addWidget(help_button)
        grid.addWidget(about_button)
        grid.addWidget(self.label)
        grid.addWidget(gen_button)
        self.setLayout(grid)

        # Slot calls
        # ------------------------------------
        help_button.clicked.connect(self.on_help_clicked)
        edit_button.clicked.connect(self.on_edit_clicked)
        about_button.clicked.connect(self.on_about_clicked)
        open_button.clicked.connect(self.on_open_clicked)
        gen_button.clicked.connect(self.on_gen_clicked)

        # Setting window properties
        # ------------------------------------
        self.setGeometry(600, 300, 500, 270)
        self.center()
        self.setWindowTitle('nu-schedule')
        self.setWindowIcon(QIcon('res/logo.ico'))
        self.show()
        info('Main window loaded')


def main():
    info('Starting the app')
    app = QApplication(argv)
    widget = UI()
    return app.exec_()


if __name__ == '__main__':
    exit(main())
