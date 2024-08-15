Name:           501webapp
Version:        1.0.0
Release:        1%{?dist}
Summary:        The VIP Code 501 CMS web app-as-package

License:        GPL
URL:            https://github.com/inkVerb/501webapp

BuildArch:      noarch
Requires:       bash, httpd, php, mariadb, libxml2, xmlstarlet, lame, ImageMagick, ffmpeg, pandoc, texlive-scheme-full
PreReq:         git

%description
501 CMS web app created in VIP Code: Linux 501 PHP-XML Stack, in /srv/www/

%prep
echo "####################################################
We are creating the 501 web app-as-package RPM installer...
Other commands could go here...
####################################################"

%build
# We could put some commands here if we needed to build from source

%pre
if [ $1 -eq 0 ]; then
  # Create the database
  mariadb -e "
  CREATE DATABASE IF NOT EXISTS blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  GRANT ALL PRIVILEGES ON blog_db.* TO 'blog_db_user'@'localhost' IDENTIFIED BY 'blogdbpassword';
  FLUSH PRIVILEGES;"
fi

%install
# Everything is done post-install

%post
# Determine web user and folder
webuser=$(ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
if [ -d "/srv/www" ]; then
  webdir="/srv/www"
elif [ -d "/var/www" ]; then
  webdir="/var/www"
else
  echo "No web folder found."
  exit 1
fi

# git clone
rm -rf /tmp/501
git clone https://github.com/inkVerb/501 /tmp/501

# Move proper folder into place
mv /tmp/501/cms ${webdir}/501
mkdir -p /etc/501webapp
mv ${webdir}/501/in.conf.php /etc/501webapp/
rm -rf /tmp/501

# Export the current database
rm -f /etc/501webapp/blog_db.sql
mariadb-dump blog_db > /etc/501webapp/blog_db.sql

# Set up the web directory
cd ${webdir}/501
mv htaccess .htaccess
mkdir -p media/docs media/audio media/video media/images media/uploads media/original/images media/original/video media/original/audio media/original/docs media/pro
chown -R $webuser:$webuser ${webdir}/501

%preun
if [ $1 -eq 0 ]; then
  rm -f /etc/501webapp/blog_db.sql
  mariadb-dump blog_db > /etc/501webapp/blog_db.sql
fi

%postun
if [ $1 -eq 0 ]; then
  # Determine web user and folder
  webuser=$(ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
  if [ -d "/srv/www" ]; then
    webdir="/srv/www"
  elif [ -d "/var/www" ]; then
    webdir="/var/www"
  else
    echo "No web folder found, attempting uninstall anyway."
  fi
  rm -rf ${webdir}/501
  mariadb -e "
  DROP USER IF EXISTS 'blog_db_user'@'localhost';
  DROP DATABASE IF EXISTS blog_db;
  FLUSH PRIVILEGES;"
fi

%files
# None, since we are doing everything under %post

%config(noreplace)
/etc/501webapp/in.conf.php
/etc/501webapp/blog_db.sql

%changelog
-------------------------------------------------------------------
Thu Jan 01 00:00:00 UTC 1970 codes@inkisaverb.com
- Something started, probably with v1.0.0