# Features

* reine Textsteuerung (nur Eingabefeld) oder interaktive Menüs mit Buttons, scrollbaren Listen, etc?
  * standard menü steuerung kann auch über textbefehle angesprochen werden, z.B. "inventory" um in ein Inventar fenster mit einer Liste von Items zu gelangen
  * übersichtskarte der bisher besuchten räume?
* 4 oder 6 seitige Räume?
* Item Kombination um neue Items zu erzeugen oder benutzen (z.B. Feuerzeug + Kerze)
  * limit auf 2 oder unbegrenzt?
* Items müssen explizit mit Gegenstand in Raum verwendet werden (z.B. richtiger Schlüssel mit Tür)
* unbegrenzte Inventargröße
  * Sinn besprechen -> benötigt u.U. suchfunktion? Items abwerfbar oder zerstörbar?
* welche Events muss eventengine beherrschen?
  * z.B. onOpenDoor X, onUseItem Y, onEnterRoom, etc.
* welche Aktionen für events verfügbar?
  * z.B. createItem X, destroyItem Y, loseGame, lockDoor Z, etc.
* definition der Räume in YAML oder JSON? (https://wiki.python.org/moin/YAML)
  * JSON in standard python enthalten
  * PyYAML ist C based, Kompilierung mit pip?
