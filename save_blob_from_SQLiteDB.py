#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import locale
from argparse import ArgumentParser
import re
import progressbar2

__author__    = "Dennis Schreiber"
__version__   = "20231126"
__date__      = "26.11.2023"
__copyright__ = "Copyright (c) Dennis Schreiber [4n6linux@gmail.com]"
__license__   = "GNU LGPL version 3"

p = ArgumentParser()
p.add_argument('-d', '--database', help='auszulesende SQLite-Datenbank', required=True)
p.add_argument('-t', '--table', help='Tabelle mit den binären Daten', required=True)
p.add_argument('-b', '--blob', help='Spalte mit den binären Daten', required=True)
p.add_argument('-1', '--dateiname', help='Spalte mit dem Dateinamen', required=True)
p.add_argument('-2', '--dateiname2', help='Spalte mit einem weiteren Bestandteil für den Dateinamen', required=False)
p.add_argument('-o', '--outdir', help='Ausgabeverzeichnis', required=True)
args = p.parse_args()

DB = args.database
TABLE = args.table
BLOBFIELD = args.blob
FNAME1 = args.dateiname
FNAME2 = args.dateiname2
ABLAGE = args.outdir


locale.setlocale(locale.LC_ALL, locale.getlocale())
LANG = locale.getlocale()[0]

def write_blob(PFAD,  NAME, BLOB):
    FOBJ = open(os.path.join(PFAD, NAME), 'wb')
    FOBJ.write(BLOB)
    FOBJ.close()

def main():
    # Prüfen, ob Zielverzeichnis vorhanden ist und ggfs. anlegen
    if not os.path.exists(ABLAGE):
        os.makedirs(ABLAGE)
    #testanzahl = 10
    counter = 0
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    # alle Zeilen durchlaufen
    # SQL für Dateinamen aus zwei Feldern
    if FNAME2:
        SQL = '''SELECT %s  || '_' || %s AS DATEINAME, %s AS BLOB FROM %s''' % (FNAME1, FNAME2, BLOBFIELD, TABLE)
    else:
        # SQL für Dateinamen aus einem Feld
        SQL = '''SELECT %s AS DATEINAME, %s AS BLOB FROM %s'''  % (FNAME1, BLOBFIELD, TABLE)
    #print(SQL)
    ANZ_ZEILEN = cursor.execute("SELECT COUNT() FROM %s" % TABLE).fetchone()[0]
    ZEILEN = cursor.execute(SQL)
    pbar = progressbar2.ProgressBar(max_value=ANZ_ZEILEN)

    for ZEILE in ZEILEN:
        #if counter > testanzahl:
        #    break
        PPFADTMP, PBLOB = ZEILE
        # für Dateisystem reservierte Zeichen entfernen
        PPFAD = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", PPFADTMP)
        write_blob(ABLAGE, PPFAD, PBLOB)
        counter += 1
        pbar.update(counter)
    pbar.finish()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
