import sys
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtCore import QThread, pyqtSignal, QStandardPaths, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QByteArray
from funcionalidades.analyzer import analizar_jugador
from dataExtractor import extractor, extraer_imagen
from mhtmlConverter import converter
import math

class HiloAnalisis(QThread):
    result = pyqtSignal(dict)

    def __init__(self, diccionario_jugador):
        super().__init__()
        self.diccionario_jugador = diccionario_jugador
        self.player = None

    def run(self):
        result = analizar_jugador(self.diccionario_jugador)
        self.result.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('analisis.ui', self)
        self.show()
        self.resultado_analisis = None

        self.calcular_btn.clicked.connect(self.calcular)

        self.subir_btn.clicked.connect(self.subirJugador)

        self.subir_imagen.clicked.connect(self.subirImagen)

        self.reiniciar_btn.clicked.connect(self.reiniciar)

        self.tutorial.setText('<a href="https://es.stackoverflow.com/">Tutorial</a>')
        self.tutorial.setOpenExternalLinks(True)

        self.q_ex_stat_todas.setToolTip("""
        <table>
        <tr><td style='text-align:justify;'padding:0; margin:0;'>
            <p style='margin:0; padding:0;'>Aumenta el valor de todas las <br>estadisticas a la vez en un porcentaje</p>
        </td></tr>
        <tr><td style='text-align:center; 'padding:0; margin:0;'>
            <img src='img/ej1.jpg' style='margin:0; padding:0; '/>
        </td></tr>
        </table>
        """)
        self.q_ex_stat_todas.setToolTipDuration(5000)

        self.q_ex_stat.setToolTip("""
        <table>
        <tr><td style='text-align:justify;'padding:0; margin:0;'>
            <p style='margin:0; padding:0;'>Aumenta el valor de una estadisticas<br> a la vez en un porcentaje</p>
        </td></tr>
        <tr><td style='text-align:center; 'padding:0; margin:0;'>
            <img src='img/ej2.jpg' style='margin:0; padding:0;'/>
        </td></tr>
        </table>
        """)
        self.q_ex_stat.setToolTipDuration(5000)

        self.q_ex_tec.setToolTip("""
        <table>
        <tr><td style='text-align:justify;'padding:0; margin:0;'>
            <p style='margin:0; padding:0;'>Aumenta la potencia de una<br> tecnica a la vez en un porcentaje</p>
        </td></tr>
        <tr><td style='text-align:center; 'padding:0; margin:0;'>
            <img src='img/ej3.jpg' style='margin:0; padding:0;'/>
        </td></tr>
        </table>
        """)
        self.q_ex_tec.setToolTipDuration(5000)

        self.q_ext_tec_todas.setToolTip("""
        <table>
        <tr><td style='text-align:justify;'padding:0; margin:0;'>
            <p style='margin:0; padding:0;'>Aumenta la potencia de todas las<br> tecnicas a la vez en un porcentaje</p>
        </td></tr>
        <tr><td style='text-align:center; 'padding:0; margin:0;'>
            <img src='img/ej4.jpg' style='margin:0; padding:0;'/>
        </td></tr>
        </table>
        """)
        self.q_ext_tec_todas.setToolTipDuration(5000)

    def onTaskFinished(self, result):
        for key in ['remate', 'pase', 'regate', 'entrada', 'bloqueo', 'intercepcion']:
            getattr(self, f"{key[:3]}_visual").setText(str(math.ceil(result['statsVisuales'][key])))
            getattr(self, f"{key[:3]}_total").setText(str(math.ceil(result['statsDuelo'][key])))
        getattr(self, "par_visual").setText(str(math.ceil(result['statsVisuales']['pase'])))    
        getattr(self, "par_total").setText(str(math.ceil(result['statsDuelo']['pared'])))    

        self.cab_total.setText(str(math.ceil(result['statsDuelo']['cabeceo'])))
        self.vol_total.setText(str(math.ceil(result['statsDuelo']['volea'])))
        self.balto_total.setText(str(math.ceil(result['statsDuelo']['bloqueoAlto'])))
        self.bbajo_total.setText(str(math.ceil(result['statsDuelo']['bloqueoBajo'])))



    def reiniciar(self):
        self.reg_st.setValue(0)
        self.rem_st.setValue(0)
        self.pas_st.setValue(0)
        self.ent_st.setValue(0)
        self.blo_st.setValue(0)
        self.int_st.setValue(0)
        self.rap_st.setValue(0)
        self.pot_st.setValue(0)
        self.tec_st.setValue(0)
        self.reg_tc.setValue(0)
        self.rem_tc.setValue(0)
        self.pas_tc.setValue(0)
        self.par_tc.setValue(0)
        self.ent_tc.setValue(0)
        self.blo_tc.setValue(0)
        self.int_tc.setValue(0)
        self.baj_tc.setValue(0)
        self.alt_tc.setValue(0)
        self.jug_img.clear()

        for key in ['remate', 'pase', 'regate', 'entrada', 'bloqueo', 'intercepcion']:
            getattr(self, f"{key[:3]}_visual").setText(str(0))
            getattr(self, f"{key[:3]}_total").setText(str(0))
        getattr(self, "par_visual").setText(str(0))    
        getattr(self, "par_total").setText(str(0))    
        self.cab_total.setText(str(0))
        self.vol_total.setText(str(0))
        self.balto_total.setText(str(0))
        self.bbajo_total.setText(str(0))

    def subirJugador(self):
        options = (QFileDialog.Option.DontUseNativeDialog)
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DownloadLocation
        )
        file_types = "Archivos MHTML (*.mhtml);;Archivos HTML (*.html)"
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", initial_dir, file_types, options=options)
        if file_name:
            if file_name.endswith('.html'):
                self.player = extractor(file_name)
                self.actualizar_ui()
            elif file_name.endswith('.mhtml'):
                img = extraer_imagen(file_name)
                if img:
                    self.actualizar_imagen(img)
                else:
                    pass
                archivo_html = converter(file_name)
                self.player = extractor(archivo_html)
                self.actualizar_ui()

    def subirImagen(self):
        options = (QFileDialog.Option.DontUseNativeDialog)
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DownloadLocation
        )
        file_types = "Archivo JPG (*.jpg);;Archivo PNG (*.png);;Archivo GIF (*.gif)"
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", initial_dir, file_types, options=options)
        if file_name:
            self.actualizar_imagen(file_name)


    def actualizar_imagen(self, img):
        
        # Convertir _io.BytesIO a QByteArray
        img.seek(0)  # Asegurarse de que el puntero esté al inicio
        byte_array = QByteArray(img.read())

        # Crear el QPixmap desde QByteArray
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)

        # Escalar el QPixmap
        scaled_pixmap = pixmap.scaled(161, pixmap.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.jug_img.setPixmap(scaled_pixmap)


    def actualizar_ui(self):
        self.reg_st.setValue(self.player['stats']['regate'])
        self.rem_st.setValue(self.player['stats']['remate'])
        self.pas_st.setValue(self.player['stats']['pase'])
        self.ent_st.setValue(self.player['stats']['entrada'])
        self.blo_st.setValue(self.player['stats']['bloqueo'])
        self.int_st.setValue(self.player['stats']['intercepcion'])
        self.rap_st.setValue(self.player['stats']['rapidez'])
        self.pot_st.setValue(self.player['stats']['potencia'])
        self.tec_st.setValue(self.player['stats']['tecnica'])
        self.reg_tc.setValue(self.player['tecnicas']['regate'])
        self.rem_tc.setValue(self.player['tecnicas']['remate'])
        self.pas_tc.setValue(self.player['tecnicas']['pase'])
        self.par_tc.setValue(self.player['tecnicas']['pared'])
        self.ent_tc.setValue(self.player['tecnicas']['entrada'])
        self.blo_tc.setValue(self.player['tecnicas']['bloqueo'])
        self.int_tc.setValue(self.player['tecnicas']['intercepcion'])
        self.baj_tc.setValue(self.player['tecnicas']['bajo'])
        self.alt_tc.setValue(self.player['tecnicas']['alto'])
        self.cab_sel.setCurrentText(self.player['otros']['cabeceo'])
        self.vol_sel.setCurrentText(self.player['otros']['volea'])



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
            'pared': self.par_tc.value(),
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
        self.hilo.result.connect(self.onTaskFinished)
        self.hilo.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    sys.exit(app.exec())
