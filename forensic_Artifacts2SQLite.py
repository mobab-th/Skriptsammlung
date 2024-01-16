#!/usr/bin/env python
# coding: utf-8

import yaml
import sqlite3
import os.path, os

'''
https://github.com/ForensicArtifacts/artifacts
https://artifacts.readthedocs.io/en/latest/
'''

__version__ = '20231231'
__author__ = 'Dennis Schreiber'
__description__ = 'ForensicArtifacts in SQLite-DB schreiben'


print(f'{__description__} \nVersion: {__version__}\nAutor: {__author__}')
print('\nErstelle Datenbank ...')

if os.path.exists('forensic_artifacts.sqlite'):
    os.remove('forensic_artifacts.sqlite')

db = sqlite3.connect('forensic_artifacts.sqlite')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE tbl_artifact(id INTEGER PRIMARY KEY, name TEXT, beschreibung TEXT)
''')
cursor.execute('''
    CREATE TABLE tbl_os(id INTEGER PRIMARY KEY, aid INTEGER, sid INTEGER, osname TEXT)
''')
cursor.execute('''
    CREATE TABLE tbl_sources(id INTEGER PRIMARY KEY, aid INTEGER, typ TEXT, pfade TEXT)
''')
cursor.execute('''
    CREATE TABLE tbl_url(id INTEGER PRIMARY KEY, aid INTEGER, url TEXT)
''')

db.commit()

artefakt_counter = 0
quellen_counter = 0

for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".yaml"):
            #print(os.path.join(root, file))
            with open(os.path.join(root, file), 'r') as file:
                docs = yaml.safe_load_all(file)

                for data in docs:
                    artefakt_counter +=1
                    DESCR = data['doc']
                    NAME = data['name']
                    # Artefakt und Beschreibung eintragem
                    cursor.execute('''INSERT INTO tbl_artifact(name, beschreibung)
                                VALUES(?,?)''', (NAME, DESCR))
                    aid = cursor.lastrowid
                    # URL's ermitteln und in Tabelle eintragen
                    if 'urls' in data:
                        for u in data['urls']:
                            cursor.execute('''INSERT INTO tbl_url(aid, url)
                                VALUES(?,?)''', (aid, u))

                    # eintragen, in welchem OS Artefakt zu finden ist
                    if 'supported_os' in data:
                        for aos in data['supported_os']:
                            cursor.execute('''INSERT INTO tbl_os(aid, osname)
                                VALUES(?,?)''', (aid, aos))
                    # Quellen ermitteln und in DB eintragen
                    for source in data['sources']:
                        #print source
                        TYP=source.get('type')
                        PFADE = ''
                        COMMAND = ''
                        if TYP == 'COMMAND':
                            COMMAND = source.get('attributes').get('cmd')
                            for a in source.get('attributes').get('args'):
                                COMMAND = COMMAND + ' ' + a
                            # Fundstellen eintragen
                            cursor.execute('''INSERT INTO tbl_sources(aid, typ, pfade)
                                VALUES(?,?,?)''', (aid, TYP, COMMAND))
                            # ID des Eintrags
                            sid = cursor.lastrowid
                            # OS der Fundstellen eintragen
                            if 'supported_os' in source:
                                for o in source.get('supported_os'):
                                    cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, o))
                            else:
                                # OS aus Oberrubrik eintragen, wenn kein OS-Eintrag zu einzlnen Quellen
                                cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, aos))

                        if TYP == 'WMI':
                            PFADE = 'Abfrage: %s' % source.get('attributes').get('query')
                            if not source.get('attributes').get('base_object') is None:
                               PFADE = PFADE + '\nBase-Object: %s' % source.get('attributes').get('base_object')
                            # Fundstellen eintragen
                            cursor.execute('''INSERT INTO tbl_sources(aid, typ, pfade)
                                VALUES(?,?,?)''', (aid, TYP, PFADE))
                            # ID des Eintrags
                            sid = cursor.lastrowid
                            # OS der Fundstellen eintragen
                            if 'supported_os' in source:
                                for o in source.get('supported_os'):
                                    cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, o))
                            else:
                                # OS aus Oberrubrik eintragen, wenn kein OS-Eintrag zu einzlnen Quellen
                                cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, aos))

                        # Registry-Keys
                        if not source.get('attributes').get('keys') is None:
                            for p in source.get('attributes').get('keys'):
                                # Fundstellen eintragen
                                cursor.execute('''INSERT INTO tbl_sources(aid, typ, pfade)
                                VALUES(?,?,?)''', (aid, TYP, p))
                                # ID des Eintrags
                                sid = cursor.lastrowid
                                # OS der Fundstellen eintragen
                                if 'supported_os' in source:
                                    for o in source.get('supported_os'):
                                        cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, o))
                                else:
                                    # OS aus Oberrubrik eintragen, wenn kein OS-Eintrag zu einzlnen Quellen
                                    cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, aos))

                        # Registry-Values
                        if not source.get('attributes').get('key_value_pairs') is None:
                            for p in source.get('attributes').get('key_value_pairs'):
                                p = 'Key: %s, Value: %s' % (p.get('key'), p.get('value'))
                                # Fundstellen eintragen
                                cursor.execute('''INSERT INTO tbl_sources(aid, typ, pfade)
                                VALUES(?,?,?)''', (aid, TYP, p))
                                # ID des Eintrags
                                sid = cursor.lastrowid
                                # OS der Fundstellen eintragen
                                if 'supported_os' in source:
                                    for o in source.get('supported_os'):
                                        cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, o))
                                else:
                                    # OS aus Oberrubrik eintragen, wenn kein OS-Eintrag zu einzlnen Quellen
                                    cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, aos))
                        # Pfade
                        if not source.get('attributes').get('paths') is None:
                            for p in source.get('attributes').get('paths'):
                                # Fundstellen eintragen
                                cursor.execute('''INSERT INTO tbl_sources(aid, typ, pfade)
                                VALUES(?,?,?)''', (aid, TYP, p))
                                # ID des Eintrags
                                sid = cursor.lastrowid
                                # OS der Fundstellen eintragen
                                if 'supported_os' in source:
                                    for o in source.get('supported_os'):
                                        cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, o))
                                else:
                                    # OS aus Oberrubrik eintragen, wenn kein OS-Eintrag zu einzlnen Quellen
                                    cursor.execute('''INSERT INTO tbl_os(sid, osname) VALUES(?,?)''', (sid, aos))

                        db.commit()
db.close()
print(f'{aid} Artefakte mit {sid} Quellen in Datenbank eingetragen.')
