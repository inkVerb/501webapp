Name:           501webapp
Version:        1.0.0
Release:        1%{?dist}
Summary:        The VIP Code 501 CMS web app-as-package

License:        GPL
URL:            https://github.com/inkVerb/501webapp

BuildArch:      noarch
Requires:       bash, httpd, php, mariadb, libxml2, xmlstarlet, imagemagick, ffmpeg, lame, pandoc, texlive-scheme-full

%description
501 CMS web app created in VIP Code: Linux 501 PHP-XML Stack, in /srv/www/

%prep
echo "####################################################
We are creating the 501 web app-as-package RPM installer...
Other commands could go here...
####################################################"

%build
# We could put some commands here if we needed to build from source

%install
# Determine web user and folder
webuser=$(ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
if [ -d "/srv/www" ]; then
  webdir="srv/www"
elif [ -d "/var/www" ]; then
  webdir="var/www"
else
  echo "No web folder found."
  exit 1
fi

# git clone and move proper folder into place
git clone https://github.com/inkVerb/501 /tmp/501
mv /tmp/501/cms %{buildroot}/$webdir/501
rm -rf /tmp/501

%files
/$webdir/501

%post
chown -R $webuser:$webuser /$webdir/501

%changelog
* Thu Jan 01 1970 Jesse <501webapp@inkisaverb.com> - 1.0.0-1
- Something started