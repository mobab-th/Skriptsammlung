# Dockerfiles
Hier landen ein paar selbst erstellte Dockerfiles, welche ich ganz nützlich finde.
* exiftool.dockerfile  \
  Exiftool in Version 12.84 mit GeoNames500-Datenbank zur Ermittlung des Namens der Region/Ortschaft, in welcher das Bild aufgenommen wurde. Möglicher Aufruf beispielsweise direkt im Verzeichnis mit Bildern:  \
  <code>docker run -ti --rm -v '$(pwd)':'$(pwd)' exiftool exiftool -api geolocation "-geolocation*" -lang de example.jpg</code>
