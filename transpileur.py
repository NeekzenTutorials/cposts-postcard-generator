import yaml
import subprocess
import re
from env import htmltoimage
import datetime
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSlot

def sanitize_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = filename[:250]
    return filename

def html_to_png(input_html_path, output_image_path):
    lien = r'' + htmltoimage 
    command = [lien, '--format', 'png', input_html_path, output_image_path]
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de la conversion du fichier HTML en PNG : {e}")

html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Carte de Projet</title>
                <style>
                    body {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background-color: #1b294e;
                    }}

                    .card {{
                        width: 400px;
                        background-color: white;
                        border-radius: 8px;
                        padding: 20px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}

                    .header {{
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        background-color: {header_color};
                        color: white;
                        padding: 10px;
                        border-radius: 4px;
                    }}

                    .title {{
                        font-size: 18px;
                        font-weight: bold;
                    }}

                    .content {{
                        margin-top: 20px;
                    }}

                    .tabs {{
                        margin-top: 20px;
                    }}

                    .tab {{
                        display: inline-block;
                        padding: 8px 12px;
                        background-color: #f2f2f2;
                        border-radius: 4px;
                        cursor: pointer;
                        margin-right: 10px;
                    }}

                    .author {{
                        margin-top: 20px;
                        font-size: 14px;
                        color: gray;
                    }}

                    .datetime {{
                        float: right;
                        color: gray;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="header">
                        <span class="type">{formatted_type}:</span>
                        <div class="title">{titre}</div>
                    </div>
                    <div class="content">
                        <h2>{objet}</h2>
                        <div class="tabs">
                            <div class="tab">Contexte</div>
                                <p>{contexte}</p>
                            <div class="tab">Corps</div>
                                <p>{corps}</p>  
                            <div class="tab">Résultats</div>
                                <p>{resultats}</p>
                        </div>
                    </div>
                    <div class="author">{auteur}</div>
                    <div class="datetime">{date}</div>
                </div>
            </body>
            </html>
            """

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'CPost Converter'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Choisir le fichier .cpost:", self)
        layout.addWidget(self.label)
        
        self.button = QPushButton('Ouvrir', self)
        self.button.clicked.connect(self.openFileNameDialog)
        layout.addWidget(self.button)
        
        self.savePathLabel = QLabel("Dossier de sauvegarde:", self)
        layout.addWidget(self.savePathLabel)
        
        self.savePathInput = QLineEdit(self)
        self.savePathInput.setText("./posts")
        layout.addWidget(self.savePathInput)
        
        self.saveButton = QPushButton('Sauvegarder', self)
        self.saveButton.clicked.connect(self.saveFiles)
        layout.addWidget(self.saveButton)
        
        self.setLayout(layout)
    
    @pyqtSlot()
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CPost Files (*.cpost);;All Files (*)", options=options)
        if fileName:
            self.label.setText(f"File: {fileName}")
            self.cpost_file_path = fileName
    
    @pyqtSlot()
    def saveFiles(self):
        save_path = self.savePathInput.text()
        if hasattr(self, 'cpost_file_path') and save_path:
            os.makedirs(save_path, exist_ok=True)
            with open(self.cpost_file_path, 'r', encoding="utf-8") as file:
                lines = (line for line in file if not line.strip().startswith('#'))
                data = yaml.safe_load(''.join(lines))
            
            header_color_mapping = {
                'test': 'red',
                'fix': 'green',
                'post': 'blue'
            }
            header_color = header_color_mapping.get(data['type'], 'gray')  

            formatted_type = data['type'].capitalize()
            formatted_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            html_result = html_template.format(
                titre=data['titre'],
                objet=data['objet'],  
                contexte=data['contexte'],
                corps=data['corps'],
                resultats=data['resultats'],
                auteur=data['auteur'],
                header_color=header_color,
                formatted_type=formatted_type,
                date=formatted_date
            )
      
            print(f"Sauvegarde des fichiers dans {save_path}")
            
            with open(self.cpost_file_path, 'r', encoding="utf-8") as file:
                data = yaml.safe_load(file)
            formatted_type = data['type'].capitalize()
            safe_title = sanitize_filename(data['titre'])
            base_filename = f"{formatted_type}({safe_title})"
            
            output_html_path = os.path.join(save_path,f'{base_filename}.html')
            with open(output_html_path, 'w') as file:
                file.write(html_result)
            print("Fichier HTML créé :", output_html_path)
            
            output_image_path = os.path.join(save_path,f'{base_filename}.png')
            html_to_png(output_html_path, output_image_path)
            print("Image créée :", output_image_path)
        else:
            print("Erreur: Fichier .cpost non sélectionné ou chemin de sauvegarde non spécifié.")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())