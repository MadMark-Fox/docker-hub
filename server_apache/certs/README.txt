Insertar los certificados SSL en esta carpeta para que el servidor Apache pueda utilizarlos.

# Crear un certificado autofirmado
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt

# Usaremos si no let's encrypt.
Comandos:
sudo apt install certbot python3-certbot-apache
sudo certbot certonly --manual --preferred-challenges dns -d tu_dominio.com 
