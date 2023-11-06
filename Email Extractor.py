import csv
import requests
import re
import os
from PyQt5 import QtWidgets, QtGui

class EmailExtractorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle('Email Extractor')

        layout = QtWidgets.QVBoxLayout()

        url_label = QtWidgets.QLabel('Enter the website URL:')
        self.url_entry = QtWidgets.QLineEdit()
        layout.addWidget(url_label)
        layout.addWidget(self.url_entry)

        output_label = QtWidgets.QLabel('Enter the output filename (without extension):')
        self.output_entry = QtWidgets.QLineEdit()
        layout.addWidget(output_label)
        layout.addWidget(self.output_entry)

        extract_button = QtWidgets.QPushButton('Extract Emails')
        extract_button.clicked.connect(self.extract_and_display)
        layout.addWidget(extract_button)

        self.status_label = QtWidgets.QLabel('')
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def extract_data(self, url, output_filename):
        response = requests.get(url)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        emails = re.findall(email_pattern, response.text)
        unique_emails = list(set(emails))

        modified_data = []

        for email in unique_emails:
            email_without_numeric = re.sub(r'\d+', '', email)
            parts = email_without_numeric.split('@')

            if len(parts) == 2:
                email_without_domain = parts[0]
                modified_data.append([email, email_without_domain])

        download_folder = os.path.expanduser("~") + "/Downloads"
        output_path = os.path.join(download_folder, output_filename + '.csv')

        with open(output_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(['Email', 'Modified Name'])
            writer.writerows(modified_data)

        return output_path

    def extract_and_display(self):
        website_url = self.url_entry.text()
        output_filename = self.output_entry.text()

        if website_url and output_filename:
            output_path = self.extract_data(website_url, output_filename)
            self.status_label.setText(f'Emails and modified names extracted and saved to {output_path}')
        else:
            self.status_label.setText('Please enter a valid URL and output filename.')

def main():
    app = QtWidgets.QApplication([])
    window = EmailExtractorApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

