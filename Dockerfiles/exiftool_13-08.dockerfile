FROM  docker.io/perl:stable-slim-threaded-bookworm

ARG ExifToolVersion=13.08
ARG GeoLocation=https://exiftool.org/Geolocation500-20241021.zip
WORKDIR /tmp

RUN apt-get update && apt-get install -y wget libarchive-tools nano \
    && wget https://exiftool.org/Image-ExifTool-${ExifToolVersion}.tar.gz \
    && gzip -dc Image-ExifTool-${ExifToolVersion}.tar.gz | tar -xf - \
    && cd Image-ExifTool-${ExifToolVersion} \
    && perl Makefile.PL \
    && make test \
    && make install \
    && cp config_files/example.config /root/.ExifTool_config \
    && sed  's/1;  #end/\$Image::ExifTool::Geolocation::geoDir = "\/opt\/Geolocation500\/";\n1;/' /root/.ExifTool_config \
    && cd .. \
    && rm -Rf Image-ExifTool-${ExifToolVersion} \
    && rm -f Image-ExifTool-${ExifToolVersion}.tar.gz \
    && cd /opt/ \
    && wget -qO- {GeoLocation} | bsdtar -xvf-

WORKDIR /data
ENTRYPOINT ["exiftool"]
