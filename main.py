import sys
from PyQt6.QtWidgets import *
from PyQt6.uic import *
from PyQt6.QtCore import QThread, pyqtSignal

class HiloPrueba(QThread):
    result = pyqtSignal(dict)
    progress = pyqtSignal(int)
    def __init__(self):
        super().__init__()
    
    #comienza a correr el hilo
    def run(self):
        result = analizar_jugador(self.progress)
        self.result.emit(result)




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('analisis.ui', self)
        self.show()
        self.calcular_btn.clicked.connect(self.prueba)
        self.calcular_btn.clicked.connect(self.calcular)

    def prueba(self):
        self.hilo = HiloPrueba()
        self.hilo.result.connect(self.onTaskFinished)
        self.hilo.start()


    def onTaskFinished(self, result):
        print(result)
        print('Task finished')
        


    def calcular(self):
        
        
        diccionario_jugador = {
            'regate_stat' : self.reg_st.value(),
            'remate_stat' : self.rem_st.value(),
            'pase_stat' : self.pas_st.value(),
            'entrada_stat' : self.ent_st.value(),
            'bloqueo_stat' : self.blo_st.value(),
            'interceptacion_stat' : self.int_st.value(),
            'rapidez_stat' : self.rap_st.value(),
            'potencia_stat' : self.pot_st.value(),
            'tecnica_stat' : self.tec_st.value(),
            'regate_tec' : self.reg_tc.value(),
            'remate_tec' : self.rem_tc.value(),
            'pase_tec' : self.pas_tc.value(),
            'entrada_tec' : self.ent_tc.value(),
            'bloqueo_tec' : self.blo_tc.value(),
            'interceptacion_tec' : self.int_tc.value(),
            'bajo_tec' : self.baj_tc.value(),
            'alto_tec' : self.alt_tc.value(),
            'regate_ex' : self.reg_ex.value(),
            'remate_ex' : self.rem_ex.value(),
            'pase_ex' : self.pas_ex.value(),
            'entrada_ex' : self.ent_ex.value(),
            'bloqueo_ex' : self.blo_ex.value(),
            'interceptacion_ex' : self.int_ex.value(),
            'bajo_ex' : self.baj_ex.value(),
            'alto_ex' : self.alt_ex.value(),
            'ts' : self.ts.value(),
            'bond' : self.bond.value(),
            'parametros' : self.parametros.value(),
            'potencia' : self.potencia.value(),
            'cab_sel' : self.cab_sel.currentText(),
            'vol_sel' : self.vol_sel.currentText(),
            'for_sel' : self.for_sel.currentText(),
            'lb_sel' : self.lb_sel.currentText(),
            'col_sel' : self.col_sel.currentText(),
            'bb4_cb' : self.bb4_cb.isChecked(),
        }

        print(diccionario_jugador)
    def update_progressbar(self, new_value):
        self.progressbar.setValue(new_value)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())    