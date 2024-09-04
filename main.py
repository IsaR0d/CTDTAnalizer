import sys
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtCore import QThread, pyqtSignal
from analizer import analizar_jugador
import math

class HiloAnalisis(QThread):
    result = pyqtSignal(dict)
    progress = pyqtSignal(int)

    def __init__(self, diccionario_jugador):
        super().__init__()
        self.diccionario_jugador = diccionario_jugador

    def run(self):
        result = analizar_jugador(self.progress, self.diccionario_jugador)
        self.result.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('analisis.ui', self)
        self.show()
        self.resultado_analisis = None
        self.calcular_btn.clicked.connect(self.calcular)

    def onTaskFinished(self, result):
        for key in ['remate', 'pase', 'regate', 'entrada', 'bloqueo', 'intercepcion']:
            getattr(self, f"{key[:3]}_visual").setText(str(math.ceil(result['statsVisuales'][key])))
            getattr(self, f"{key[:3]}_total").setText(str(math.ceil(result['statsDuelo'][key])))

        self.cab_total.setText(str(math.ceil(result['statsDuelo']['cabeceo'])))
        self.vol_total.setText(str(math.ceil(result['statsDuelo']['volea'])))
        self.balto_total.setText(str(math.ceil(result['statsDuelo']['bloqueoAlto'])))
        self.bbajo_total.setText(str(math.ceil(result['statsDuelo']['bloqueoBajo'])))

    def onProgress(self, progress):
        self.progressBar.setValue(progress)

    def calcular(self):   
        stats = {
            'regate': self.reg_st.value(), 
            'remate': self.rem_st.value(), 
            'pase': self.pas_st.value(), 
            'entrada': self.ent_st.value(), 
            'bloqueo': self.blo_st.value(), 
            'intercepcion': self.int_st.value(), 
            'rapidez': self.rap_st.value(), 
            'potencia': self.pot_st.value(), 
            'tecnica': self.tec_st.value()
        }

        tecnicas = {
            'regate': self.reg_tc.value(), 
            'remate': self.rem_tc.value(), 
            'pase': self.pas_tc.value(), 
            'entrada': self.ent_tc.value(), 
            'bloqueo': self.blo_tc.value(), 
            'intercepcion': self.int_tc.value(), 
            'bajo': self.baj_tc.value(), 
            'alto': self.alt_tc.value()
        }

        extras = {
            'regate': 1 + (self.reg_ex.value() + self.ex_tec.value()) / 100, 
            'remate': 1 + (self.rem_ex.value() + self.ex_tec.value()) / 100, 
            'pase': 1 + (self.pas_ex.value() + self.ex_tec.value()) / 100, 
            'entrada': 1 + (self.ent_ex.value() + self.ex_tec.value()) / 100, 
            'bloqueo': 1 + (self.blo_ex.value() + self.ex_tec.value()) / 100, 
            'intercepcion': 1 + (self.int_ex.value() + self.ex_tec.value()) / 100, 
            'bajo': 1 + (self.baj_ex.value() + self.ex_tec.value()) / 100, 
            'alto': 1 + (self.alt_ex.value() + self.ex_tec.value()) / 100
        }

        extra_stat = {
            'regate': 1 + (self.reg_ex_stat.value() + self.ex_stat.value()) / 100, 
            'remate': 1 + (self.rem_ex_stat.value() + self.ex_stat.value()) / 100, 
            'pase': 1 + (self.pas_ex_stat.value() + self.ex_stat.value()) / 100, 
            'entrada': 1 + (self.ent_ex_stat.value() + self.ex_stat.value()) / 100, 
            'bloqueo': 1 + (self.blo_ex_stat.value() + self.ex_stat.value()) / 100, 
            'intercepcion': 1 + (self.int_ex_stat.value() + self.ex_stat.value()) / 100, 
            'rapidez': 1 + (self.rap_ex_stat.value() + self.ex_stat.value()) / 100, 
            'potencia': 1 + (self.pot_ex_stat.value() + self.ex_stat.value()) / 100, 
            'tecnica': 1 + (self.tec_ex_stat.value() + self.ex_stat.value()) / 100
        }

        otros = {
            'ts': 1 + self.ts.value() / 100, 
            'bond': 1 + self.bond.value() / 100, 
            'parametros': 1 + self.parametros.value() / 100, 
            'potencia': 1 + self.potencia.value() / 100, 
            'cabeceo': self.cab_sel.currentText(), 
            'volea': self.vol_sel.currentText(), 
            'formacion': self.for_sel.currentText(), 
            'lb': self.lb_sel.currentText(), 
            'color': self.col_sel.isChecked(), 
            'bb4': self.bb4_cb.isChecked()
        }

        diccionario_jugador = {'stats': stats, 'tecnicas': tecnicas, 'extras': extras, 'otros': otros, 'exStats': extra_stat}

        # Crear el hilo y pasar el diccionario como argumento
        self.hilo = HiloAnalisis(diccionario_jugador)
        self.hilo.progress.connect(self.onProgress)
        self.hilo.result.connect(self.onTaskFinished)
        self.hilo.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    sys.exit(app.exec())
