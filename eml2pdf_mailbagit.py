#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import mimetypes
from pypdf import PdfWriter
import os
import requests
import tempfile
from dirwalker import DATEIEN
import sys
from argparse import ArgumentParser
import locale
from sys import argv, stderr, exit

__version__ = '20240118'
__author__ = 'Dennis Schreiber'
__description__ = 'Erstellt aus PDF-Mails, welche mit mailbagit erstellt wurden, PDF mit "ausgedruckten" Anhängen. Die Anhänge werden zusätzlich im Orignal in das PDF eingebettet.'

locale.setlocale(locale.LC_ALL, '')
sys.getdefaultencoding()


headers = {
    'accept': '*/*',
}

p = ArgumentParser(
    description=__description__
    )
p.add_argument('-i', '--indir', help='MailBag-Verzeichnis', required=True)
p.add_argument('-s', '--server', help='Host des Strirling-PDF-Server (Vorgabe: http://localhost)', default='http://localhost')
p.add_argument('-p', '--port', help='Port des Strirling-PDF-Server (Vorgabe: 8080)', default='8080')



args = p.parse_args()
url = f'{args.server}:{args.port}/api/v1/convert/file/pdf'
tmpdir = tempfile.gettempdir()
SUCHPFAD=args.indir
# gesuchte Dateiendung für alle einfach '' setzen
ENDUNG='pdf'

PDFdir = os.path.join(SUCHPFAD, 'data' ,'pdf')
ATTACHdir = os.path.join(SUCHPFAD, 'data' ,'attachments')
alleDateien=DATEIEN(PDFdir, ENDUNG)
anzahl = len(list(alleDateien))
counter = 1
for DATEI in DATEIEN(PDFdir, ENDUNG):
    merger = PdfWriter()
    print(f'Bearbeite {counter} von {anzahl}: {DATEI}')
    mailfile = os.path.splitext(os.path.basename(DATEI))
    if os.path.exists(os.path.join(ATTACHdir, mailfile[0])):
        # Mail-PDF öffnen, um Anhänge hinzuzufügen
        basefile=open(DATEI, 'rb')
        merger.append(basefile)
        for a in DATEIEN(os.path.join(ATTACHdir, mailfile[0]),''):
            mime = mimetypes.guess_type(a)
            filename = os.path.basename(a)
            # Anhänge hinzufügen, aber nicht die attachments.csv
            if filename.lower() != 'attachments.csv':
                print(f'\tFüge Anhang {filename} hinzu.')
                if mime[0].split('/')[1].lower() == ' pdf':
                    try:
                        # PDF-Anhang anhängen
                        merger.append(a)
                        # PDF-Anhang einbetten
                        merger.add_attachment(filename, a)
                    except Exception as err:
                        print(f'Fehler beim Bearbeiten des Anhangs {filename}: {str(err)}')
                        continue
                else:
                    # nicht PDF-Datei konvertieren
                    try:
                        files = {
                            'fileInput': (filename,
                                        open(a, 'rb'),
                                        mime[0]),
                                }
                        r = requests.post(url, files=files, headers=headers)
                        if r.status_code == 200:
                            #print(r.content)
                            with tempfile.TemporaryFile() as fp:
                                fp.write(r.content)
                                merger.append(fp, 'rb')
                            # Orignaldatei einbetten
                            merger.add_attachment(filename, r.content)
                            # Anlage wieder löschen
                    except Exception as err:
                        print(f'Fehler beim Bearbeiten des Anhangs {filename}: {str(err)}')
                        continue

        # Write to an output PDF document
        output = open(DATEI, "wb")
        merger.write(output)

        basefile.close()
        merger.close()
        output.close()
        counter +=1


