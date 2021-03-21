from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from design import Ui_MainWindow
import sys
import random

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.dur_cb.activated.connect(self.division_enabled)
        self.ui.Generate_Button.clicked.connect(self.Generate)
        self.ui.Reset_Button.clicked.connect(self.Reset)

    def division_enabled(self):
        if self.ui.dur_cb.currentIndex() == 0 or self.ui.dur_cb.currentIndex() == 4:
            self.ui.div_chb.setEnabled(False)
            self.ui.div_chb.setChecked(False)
            self.ui.unreg_chb.setEnabled(False)
            self.ui.unreg_chb.setChecked(False)
            self.ui.groupBox_2.setEnabled(False)
            self.ui.groupBox_3.setEnabled(False)
        else:
            if self.ui.dur_cb.currentIndex() == 3:
                self.ui.div_chb.setEnabled(True)
                self.ui.unreg_chb.setEnabled(True)
            else:
                self.ui.div_chb.setEnabled(True)
                self.ui.unreg_chb.setEnabled(False)
                self.ui.unreg_chb.setChecked(False)
                self.ui.groupBox_3.setEnabled(False)

    def Generate(self):
        main_dur_s = self.ui.dur_cb.currentIndex()
        def get_dur(x):
            durs = {0 : 16, 1 : 8, 2 : 4, 3 : 2,
                4 : 24, 5 : 12, 6 : 6, 7 : 3}
            x = durs.get(x)
            return x
        main_dur = get_dur(main_dur_s)
        
        measure_s = self.ui.measure_line.text().split()
        if not len(measure_s) > 0:
            QMessageBox.critical(self,
                                 "Error", "Measure line is empty",
                                 QMessageBox.Ok)
            sys.exit(1)
        def get_measure(measure_s):
            measure_l = [ ]
            try:
                for i, item in enumerate(measure_s):
                    measure_s[i] = int(item)
                    measure_l.append(measure_s[i])
            except Exception:
                QMessageBox.critical(self,
                                     "Error", "Measure line has not digits",
                                     QMessageBox.Ok)
                sys.exit(1)
            else:
                return measure_l
        measure_l = get_measure(measure_s)

        dur_count = int(main_dur/measure_l[1]*measure_l[0])

        num_of_tacts = int(self.ui.num_of_tacts_sb.value()) 
        if not num_of_tacts != 0:
            QMessageBox.critical(self,
                                     "Error", "Number of tacts equals 0",
                                     QMessageBox.Ok)
            sys.exit(1)

        if self.ui.div_chb.isChecked():
            div_enabled = True
            if self.ui.unreg_chb.isChecked():
                div_unreg_enabled = True
            else:
                div_unreg_enabled = False
        else:
            div_enabled = False
            div_unreg_enabled = False
            
        if self.ui.rests_chb.isChecked():
            rests_enabled = True
        else:
            rests_enabled = False

        array = [ ]

        def divide(dur_count):
            div_perc = self.ui.div_perc_sb.value()
            div_count = div_perc*dur_count//100
            beats = [ ]
            j = 1
            while j <= dur_count-div_count:
                beats.append([1])
                j += 1
            z = 1
            while z <= div_count:
                micro_beats = [ ]
                y = 1
                while y <= random.randint(2, 6):
                    micro_beats.append(1)
                    y += 1
                beats.append(micro_beats)
                z += 1
            random.shuffle(beats)
            return beats

        def divide_unreg(dur_count):
            div_perc = self.ui.div_perc_sb.value()
            div_parts = self.ui.div_parts_sb.value()
            media_beats_count = dur_count*div_parts
            div_count = div_perc*media_beats_count//100
            def group(lst, n):
                return [lst[i:i + n] for i in range(0, len(lst), n)]
            beats = [ ]
            j = 1
            while j <= media_beats_count-div_count:
                beats.append(random.randint(1, 4))
                j += 1
            z = 1
            while z <= div_count:
                micro_beats = [ ]
                y = 1
                while y <= random.randint(2, 6):
                    micro_beats.append(1)
                    y += 1
                beats.append([random.randint(1, 4), micro_beats])
                z += 1
            random.shuffle(beats)
            return group(beats, div_parts)

        def add_rests(beats, div_unreg_enabled):
            rests_perc = self.ui.rests_perc_sb.value()
            if beats.count(1) == 0 and div_unreg_enabled is False:
                arr_for_rests = [j for i in beats for j in i]
                rests_count = rests_perc*len(arr_for_rests)//100
                i = 0
                while i < rests_count:
                    arr_for_rests[i] = arr_for_rests[i]*(-1)
                    i += 1
                random.shuffle(arr_for_rests)
                meter = 0
                for x in beats:
                    for j, item in enumerate(x):
                        meter += 1
                        x[j] = arr_for_rests[meter-1]
            else:
                if beats.count(1) == 0 and div_unreg_enabled is True:
                    arr_for_rests = [ ]
                    for a in beats:
                        for b in a:
                            if type(b) == int:
                                arr_for_rests.append(b)
                            else:
                                c = b[1]
                                for d in c:
                                    arr_for_rests.append(d)
                    rests_count = rests_perc*len(arr_for_rests)//100
                    index_arr = random.sample([n for n in range(len(arr_for_rests))], rests_count)
                    for x in index_arr:
                        arr_for_rests[x] = arr_for_rests[x]*(-1)
                    meter = 0
                    for a in beats:
                        for i, b in enumerate(a):
                            if type(b) == int:
                                meter += 1
                                a[i] = arr_for_rests[meter-1]
                            else:
                                c = b[1]
                                for j, d in enumerate(c):
                                    meter += 1
                                    c[j] = arr_for_rests[meter-1]
                else:
                    rests_count = rests_perc*len(beats)//100
                    i = 0
                    while i < rests_count:
                        beats[i] = beats[i]*(-1)
                        i += 1
                    random.shuffle(beats)
            return beats

        j = 1
        while j <= num_of_tacts:
            tact = [ ]
            tact.append(measure_l)
            if div_enabled is True and div_unreg_enabled is False:
                beat_data = divide(dur_count)
            else:
                if div_enabled is True and div_unreg_enabled is True:
                    beat_data = divide_unreg(dur_count)
                else:
                    beat_data = [1 for n in range(dur_count)]

            if rests_enabled is True:
                final_beat_data = add_rests(beat_data, div_unreg_enabled)
            else:
                final_beat_data = beat_data
            beats = [ ]
            for x in final_beat_data:
                if type(x) == int:
                    beats.append(x)
                else:
                    if len(x) == 1:
                        for i, item in enumerate(x):
                            x[i] = int(item)
                            beats.append(item)
                    else:
                        beats.append([1, x])
            tact.append(beats)
            array.append(tact)
            j += 1

        def parse_to_lisp(x):
            x1 = ' '.join(str(n) for n in x)
            x2 = x1.replace('[', '(')
            x3 = x2.replace(']', ')')
            x4 = x3.replace(',', '')
            return x4
        
        QMessageBox.information(self, "Ready", "Rhythm has been generated",
                                     QMessageBox.Ok)
        options = QFileDialog.Options()
        name = QFileDialog.getSaveFileName(self, 'Save File',
                                           '', 'Text files (*.txt)',
                                           options = options) [0]
        file = open(name,'w')
        data = parse_to_lisp(array)
        file.write(data)
        file.close()

    def Reset(self):
        self.ui.dur_cb.setCurrentIndex(0)
        self.ui.measure_line.clear()
        self.ui.num_of_tacts_sb.setValue(0)
        self.ui.div_chb.setChecked(False)
        self.ui.div_perc_sb.setValue(0)
        self.ui.unreg_chb.setChecked(False)
        self.ui.div_parts_sb.setValue(0)
        self.ui.rests_chb.setChecked(False)
        self.ui.rests_perc_sb.setValue(0)
        
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
 
sys.exit(app.exec())
