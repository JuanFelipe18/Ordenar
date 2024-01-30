
from tkinter import font, filedialog, messagebox
import tkinter as tk
import pandas as pd
import sys
import re
import os

class Orden:
    def __init__(self):
        self.ventana_bienvenida = tk.Tk()
        self.ventana_bienvenida.title("Codificador GCM")
        self.imagen = tk.PhotoImage(file=self.resolver_ruta("logo.png"))  # Reemplaza con la ruta de tu imagen
        #self.imagen = tk.PhotoImage(file="logo.png")  # Reemplaza con la ruta de tu imagen
        self.imagen = self.imagen.subsample(6)  # Ajusta el factor de submuestreo según sea necesario
        self.fuente_personalizada = font.Font(family="Cambria Math", size=16)
        self.fuente_personalizada2 = font.Font(family="Sitka Subheading", size=16)
        self.setup_interfaz()

    def setup_interfaz(self):
        label_imagen = tk.Label(self.ventana_bienvenida, image=self.imagen)
        label_imagen.pack()

        etiqueta_bienvenida = tk.Label(self.ventana_bienvenida, text="ORGANIZAR LOGS", font=self.fuente_personalizada)
        etiqueta_bienvenida.pack(padx=10, pady=0)

        texto_adicional_1 = tk.Label(self.ventana_bienvenida, text="Versión 1.0",
                                    font=font.Font(family="Courier New", size=12))
        texto_adicional_1.pack()

        texto_adicional_2 = tk.Label(self.ventana_bienvenida,
                                     text="Grupo de Acceso a la Informacion y \nProtección de Datos Personales",
                                     font=font.Font(family="Courier New", size=12))
        texto_adicional_2.pack()

        texto_adicional_3 = tk.Label(self.ventana_bienvenida, text="Autor: Juan Felipe Martín Martínez",
                                     font=font.Font(family="Courier New", size=12))
        texto_adicional_3.pack()

        texto_adicional_4 = tk.Label(self.ventana_bienvenida,
                                     text="PROGRAMA DE USO EXCLUSIVO \nREGISTRADURIA NACIONAL DEL \nESTADO CIVIL",
                                     font=self.fuente_personalizada2)
        texto_adicional_4.pack()

        texto_adicional_5 = tk.Label(self.ventana_bienvenida, text="2023",
                                     font=font.Font(family="Courier New", size=12))
        texto_adicional_5.pack()

        self.boton_iniciar = tk.Button(self.ventana_bienvenida, text="Seleccionar archivo CSV", command=self.expandir_filas)
        self.boton_iniciar.pack(pady=20)

    def resolver_ruta(self, archivo):
        if hasattr(sys, '_MEIPASS'):  # Verifica si estamos en el entorno empaquetado
            return os.path.join(sys._MEIPASS, archivo)
        else:
            return os.path.join(os.path.abspath('.'), archivo)

    def expandir_filas(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                data = pd.read_csv(file_path, delimiter=';')

                # Extraer los números dentro de los corchetes en la columna 'peticion'
                data['peticion'] = data['peticion'].apply(lambda x: re.findall(r'\[(.*?)\]', str(x))[0] if re.findall(r'\[(.*?)\]', str(x)) else '')

                data_expandida = data.assign(peticion=data['peticion'].str.split(','))
                data_expandida = data_expandida.explode('peticion')
                data_expandida.to_csv(f'ordenado_{file_name}.csv', sep=';', index=False)

                self.mostrar_ventana_final()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def mostrar_ventana_final(self):
        ventana_final = tk.Toplevel()
        ventana_final.title("Finalizo")

        label_imagen = tk.Label(ventana_final, image=self.imagen)
        label_imagen.pack()

        etiqueta_final = tk.Label(ventana_final, text="¡Proceso finalizado con éxito!", font=self.fuente_personalizada)
        etiqueta_final.pack(padx=10, pady=5)

        boton_aceptar = tk.Button(ventana_final, text="Aceptar", command=self.cerrar_programa)
        boton_aceptar.pack(pady=5)

        ventana_final.protocol("WM_DELETE_WINDOW", self.cerrar_programa)

    def cerrar_programa(self):
        self.ventana_bienvenida.quit()


if __name__ == "__main__":
    app = Orden()
    app.ventana_bienvenida.mainloop()
