
echo "-> Data Entry System Installer for Debian based distros <-"
echo "Data Entry System v2.1b"
echo "2019-2022 (c) Javier Garcia Gonzalez <javiergarcia@mykolab.com>"
echo "GPL-3-0-or-later"

echo "Installing updates to base image"

apt-get update -y && apt-get upgrade -y 
apt-get install -y bash libzbar-dev python-pip python nginx-full python-gunicorn systemd vim runit-systemd procps lsof net-tools default-mysql-server default-mysql-client supervisor varnish python-dev default-libmysqlclient-dev libcairo2-dev icu-devtools libgirepository1.0-dev redis-server rsyslog unzip p7zip unrar-free
apt-get install -y tesseract-ocr "tesseract-ocr-*" pkg-config libicu-dev python-mysqldb libglib2.0-dev gunicorn
mkdir -p /var/log/gunicorn /var/log/celery
cp -v *.tgz /
cp -v start.sh config.sh init.sql /
cd /
tar zxvf webapp.tgz 
chown -R www-data:www-data /webapp
tar zxvf cert.tgz -C /
tar zxvf supervisor.tgz -C /
tar zxvf varnish.tgz -C /etc/
tar zxvf nginx.tgz -C /etc/
rm /webapp.tgz /cert.tgz /supervisor.tgz /varnish.tgz /nginx.tgz 
update-rc.d -f mysql defaults
update-rc.d -f supervisor defaults
update-rc.d -f redis-server defaults
chmod +x config.sh
service mysql start && service supervisor start && bash /config.sh
export DJANGO_SETTINGS_MODULE=DataEntry_v2.settings
export PYTHONPATH=/usr/bin:/usr/local/bin:/usr/lib:/usr/local/lib
python2 -m pip install --upgrade pip
python2 -m pip install mysqlclient
python2 -m pip install -r /webapp/DataEntry_v2/requirements.txt
service mysql start && service supervisor start 
cd /webapp/DataEntry_v2/
python2 manage.py migrate
python2 manage.py migrate --run-syncdb
python2 manage.py loaddata user.json
cd /webapp/DataEntry_v2 ; service mysql restart ; sleep 5s ; python2 manage.py dbshell < props.sqldump
cp /start.sh /sbin/
chmod +x /sbin/start.sh
echo "\nsource /sbin/start.sh\n" >> /etc/rc.local
echo "export DJANGO_SETTINGS_MODULE=DataEntry_v2.settings\nexport PYTHONPATH=/usr/bin:/usr/local/bin:/usr/lib:/usr/local/lib\n" > /etc/profile.d/des.sh
chmod +x /etc/profile.d/des.sh
chmod +x /etc/rc.local
systemctl stop varnish.service
systemctl mask varnish.service
systemctl stop nginx
systemctl mask nginx
touch /var/log/gunicorn/gunicorn.err.log
touch /var/log/gunicorn/gunicorn.out.log
echo "done install. Starting..."
source /start.sh

