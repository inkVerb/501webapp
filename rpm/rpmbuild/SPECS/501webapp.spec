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
# Verify web user and folder & create any needed symlink
webuser=$(ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
if [ -d "/var/www" ]; then
  webdir="/var/www"
  mkdir -p "/srv/"
  ln -sfn "/var/www" "/var/"
elif [ -d "/srv/www" ]; then
  webdir="/srv/www"
else
  mkdir -p "/srv/www"
  webdir="/srv/www"
fi

# Check if conf file already exists, then save
if [ -f "${webdir}/501/in.conf.php" ]; then
  mkdir ${webdir}/501.tmp
  mv ${webdir}/501/in.conf.php ${webdir}/501.tmp/
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

# Set up the web directory
cd ${webdir}/501
mv htaccess .htaccess
mkdir -p media/docs media/audio media/video media/images media/uploads media/original/images media/original/video media/original/audio media/original/docs media/pro

# Move any saved conf file back into place
if [ -f "${webdir}/501.tmp/in.conf.php" ]; then
  mkdir ${webdir}/501.tmp
  mv ${webdir}/501.tmp/in.conf.php ${webdir}/501/
fi
if [ -d "${webdir}/501.tmp" ]; then
  rm -f ${webdir}/501.tmp
fi

# Own web directory
chown -R $webuser:$webuser ${webdir}/501

# Make sure the SQL server is running
systemctl start mariadb

# Create the database
mariadb -e "
CREATE DATABASE IF NOT EXISTS blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON blog_db.* TO 'blog_db_user'@'localhost' IDENTIFIED BY 'blogdbpassword';
FLUSH PRIVILEGES;"

# Export the current database (such as upgrade)
mkdir -p /var/501webapp
rm -f /etc/501webapp/blog_db.sql
mariadb-dump blog_db > /var/501webapp/blog_db.sql

%preun
if [ $1 -eq 0 ]; then
  echo "Uninstalling 501 web app..."
fi

%postun
if [ $1 -eq 0 ]; then
  # Determine web user and folder
  webuser=$(ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
  if [ -d "/srv/www" ]; then
    webdir="/srv/www"
    # Remove /var/www only if it is a symlink
    [ -L "/var/www" ] && rm "/var/www"
  elif [ -d "/var/www" ]; then
    webdir="/var/www"
  else
    echo "No web folder found, attempting uninstall anyway."
  fi
  rm -rf ${webdir}/501
  rm -rf /etc/501webapp
  rm -rf /var/501webapp

  # Make sure the SQL server is running before dropping database
  systemctl start mariadb
  mariadb -e "
  DROP USER IF EXISTS 'blog_db_user'@'localhost';
  DROP DATABASE IF EXISTS blog_db;
  FLUSH PRIVILEGES;"
fi

%files
# None, since we are doing everything under %post

%config(noreplace)
# Can't put this conf file here because it is not under %files
#/etc/501webapp/in.conf.php

%changelog
* Thu Jan 01 1970 Ink Is A Verb <codes@inkisaverb.com> - 1.0.0-1
- Something started, probably with v1.0.0