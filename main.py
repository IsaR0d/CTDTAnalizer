import sys
from PyQt6.QtWidgets import *
from PyQt6.uic import *
from PyQt6.QtCore import QThread, pyqtSignal
from controler import analizar_jugador
import math

class HiloAnalisis(QThread):
    result = pyqtSignal(dict)
    progress = pyqtSignal(int)
    def __init__(self, diccionario_jugador):
        super().__init__()
        self.diccionario_jugador = diccionario_jugador
    
    #comienza a correr el hilo
    def run(self):
        print(self.diccionario_jugador)
        result = analizar_jugador(self.progress, self.diccionario_jugador)
        self.result.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('analisis.ui', self)
        self.show()
        self.resultado_analisis = None
        self.calcular_btn.clicked.connect(self.calcular)

    def onTaskFinished(self, result):
        self.resultado_analisis = result
        print(result)

    def onProgress(self, progress):
        self.progressBar.setValue(progress)

    def calcular(self):   
        stats ={'regate': self.reg_st.value(), 'remate': self.rem_st.value(), 'pase': self.pas_st.value(), 'entrada': self.ent_st.value(), 'bloqueo': self.blo_st.value(), 'interceptacion': self.int_st.value(), 'rapidez': self.rap_st.value(), 'potencia': self.pot_st.value(), 'tecnica': self.tec_st.value()}
        tecnicas = {'regate': self.reg_tc.value(), 'remate': self.rem_tc.value(), 'pase': self.pas_tc.value(), 'entrada': self.ent_tc.value(), 'bloqueo': self.blo_tc.value(), 'interceptacion': self.int_tc.value(), 'bajo': self.baj_tc.value(), 'alto': self.alt_tc.value()}
        extras = {'regate': 1+self.reg_ex.value()/100, 'remate': 1+self.rem_ex.value()/100, 'pase': 1+self.pas_ex.value()/100, 'entrada': 1+self.ent_ex.value()/100, 'bloqueo': 1+self.blo_ex.value()/100, 'interceptacion': 1+self.int_ex.value()/100}
        otros = {'ts': 1+self.ts.value()/100, 'bond': 1+self.bond.value()/100, 'parametros': self.parametros.value(), 'potencia': self.potencia.value(), 'cabeceo': self.cab_sel.currentText(), 'volea': self.vol_sel.currentText(), 'formacion': self.for_sel.currentText(), 'lb': self.lb_sel.currentText(), 'color': self.col_sel.currentText(), 'bb4': self.bb4_cb.isChecked()}
        diccionario_jugador = {'stats': stats, 'tecnicas': tecnicas, 'extras': extras, 'otros': otros}
        print(diccionario_jugador)

        # Crear el hilo y pasar el diccionario como argumento
        self.hilo = HiloAnalisis(diccionario_jugador)
        self.hilo.progress.connect(self.onProgress)
        self.hilo.result.connect(self.onTaskFinished)
        self.hilo.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())    