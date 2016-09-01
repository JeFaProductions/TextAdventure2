# Features

* interaktive Menüs mit Buttons, scrollbaren Listen, etc
  * mausbedienung disabled
  * alles menüs durch text commands erreichen
  * evtl. hauptfenster splitten -> Eingabefeld, Textfelf, Inventarliste?
  * übersichtskarte der bisher besuchten räume, über map befehle -> scrallbare ascii karte?
* 4 seitige Räume
* Item Kombination um neue Items zu erzeugen oder benutzen (z.B. Feuerzeug + Kerze)
  * limit auf 2, aber kettenkombinationen möglich
  * z.b leere Lampe + Öl = volle Lampe, volle Lampe + Feuerzeug = leuchtende Lampe
  * items zu benutzen verbraucht diese (vernichtet)
* unbegrenzte Inventargröße
* Items müssen explizit mit Gegenstand in Raum verwendet werden (z.B. richtiger Schlüssel mit Tür)
  * z.B. use key x with door y
  * man muss in dem entsprechenden raum sein
* welche Events muss eventengine beherrschen?
  * z.B. onOpenDoor X, onUseItem Y (sonderfall: item mit raumgegenstand), onEnterRoom, onCombine x + y
  * alle events sollen default handler haben, wenn kein handler für sie angemeldet ist
* welche Aktionen für events verfügbar?
  * z.B. createItem X, destroyItem Y, loseGame, lockDoor Z, openDoor X, writeText "x" etc.
* definition der Räume in YAML (pyyaml)

