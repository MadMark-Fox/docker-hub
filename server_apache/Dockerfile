FROM ubuntu:26.04

RUN apt-get update && apt-get install -y apache2

COPY index.html /var/www/html/index.html
COPY proyectos.html /var/www/html/proyectos.html
COPY contacto.html /var/www/html/contacto.html
COPY style.css /var/www/html/style.css
COPY certs /etc/apache2/ssl

EXPOSE 80
EXPOSE 443

CMD ["apache2ctl", "-D", "FOREGROUND"]