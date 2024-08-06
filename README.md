# 501webapp
*The VIP Code 501 CMS web app-as-package*

## Create the simple Linux install package for `501webapp`
This is a guide to create a web app-as-package installer for the 501 CMS from [Linux 501: PHP-XML Stack](https://github.com/inkVerb/VIP/blob/master/501/README.md) on:
1. Arch (Manjaro, Black Arch, et al)
2. Debian (Ubuntu, Kali, Mint, et al)
3. RPM (OpenSUSE supported; *RedHat/CentOS distros not supported due to no `pandoc` package*)

- This installer sets up a web app from a `git` a repository
  - The `501` web app folder is set up according to the instructions in the folder's `README.md`
  - Packages behave differently on each architecture
  - Each package is built in the simplest way possible
    - Changing the behavior of the `501` web app folder on remove/purge would require a much more complex process for any package manager
- In Arch, the files are part of the package
  - The `501` web app folder will be deleted on package removal
- In Debian & RPM, the files are not a part of the package, but are put in place after the install phase
  - The Debian package will remove the `501` web app folder only on purge
  - The RPM package will never remove the `501` web app folder

Working examples for each already resides in this repository

### Create and install the `501webapp` package directly from this repo

| **Arch** :$ (& Manjaro, Black Arch)

```console
git clone https://github.com/inkVerb/501webapp.git
cd 501webapp/arch
makepkg -si
```

| **Debian** :$ (& Ubuntu, Kali, Mint)

```console
git clone https://github.com/inkVerb/501webapp.git
cd 501webapp/deb
dpkg-deb --build 501webapp
sudo dpkg -i 501webapp.deb
```

| **RedHat/CentOS** :$ (& Fedora)

```console
git clone https://github.com/inkVerb/501webapp.git
sudo dnf update
sudo dnf install rpm-build rpmdevtools
cp -rf 501webapp/rpm/rpmbuild ~/
rpmbuild -ba ~/rpmbuild/SPECS/501webapp.spec
ls ~/rpmbuild/RPMS/noarch/
sudo rpm -i ~/rpmbuild/RPMS/noarch/501webapp-1.0.0-1.noarch.rpm  # Change filename if needed
rm -rf ~/rpmbuild
```

| **OpenSUSE** :$ (& Tumbleweed)

```console
git clone https://github.com/inkVerb/501webapp.git
cd 501webapp/rpm
sudo zypper update
sudo zypper install rpm-build rpmdevtools
cp -r rpmbuild ~/
rpmbuild -ba ~/rpmbuild/SPECS/501webapp.spec
ls ~/rpmbuild/RPMS/noarch/
sudo rpm -i ~/rpmbuild/RPMS/noarch/501webapp-1.0.0-1.noarch.rpm  # Change filename if needed
rm -rf ~/rpmbuild
```

## Detailed instructions per architecture
Instructions explain each in detail to create these packages from scratch...

### I. Arch Linux Package (`501webapp-1.0.0-1-any.pkg.tar.zst`)
*Arch package directory structure:*

| **`arch/`** :

```
arch/
└─PKGBUILD
```

- Create directory: `arch`
- In `arch/` create file: `PKGBUILD`

| **`arch/PKGBUILD`** :

```
pkgname=501webapp
pkgver=1.0.0
pkgrel=1
pkgdesc="The VIP Code 501 CMS web app-as-package"
url="https://github.com/inkVerb/501webapp"
arch=('any')
license=('GPL')
depends=('bash' 'apache' 'php' 'mariadb' 'libxml2' 'xmlstarlet' 'imagemagick' 'ffmpeg' 'lame' 'pandoc' 'texlive-core' 'texlive-latex' 'texlive-fontsrecommended' 'texlive-latexrecommended')  # Apache becuase we use rewrites
makedepends=('git')
source=('git+https://github.com/inkVerb/501.git')
sha256sums=('SKIP')

build() {
  cd "$srcdir/501"
}

package() {
  webuser=$(ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
  if [ -d "/srv/www" ]; then
    webdir="srv/www"
  elif [ -d "/var/www" ]; then
    webdir="var/www"
  else
    echo "No web folder found."
    exit 1
  fi
  cd "$srcdir/501"
  install -d "${pkgdir}/${webdir}"
  cp -r cms "${pkgdir}/${webdir}/501"

  cd ${pkgdir}/${webdir}/501
  mv htaccess .htaccess
  mkdir -p media/docs media/audio media/video media/images media/uploads media/original/images media/original/video media/original/audio media/original/docs media/pro

  chown -R $webuser:$webuser "${pkgdir}/${webdir}/501"
}
```

- You will need to have certain dependencies installed even before building the package
  - These should already be installed from [Linux 501](https://github.com/inkVerb/VIP/blob/master/501/README.md), but are here for reference if needed

| **Install dependencies** :$

```console
sudo pacman -Syy apache php mariadb libxml2 xmlstarlet imagemagick ffmpeg lame pandoc texlive-core texlive-latex texlive-fontsrecommended texlive-latexrecommended
```

- Build package:
  - Navigate to directory `arch/`
  - Run this, then the package will be built, then installed with `pacman`:

| **Build & install Arch package** :$ (in one command)

```console
makepkg -si
```

- Use this to build and install in two steps:

| **Build, *then* install Arch package** :$ (first line produces the `.pkg.tar.zst` file for repos or manual install)

```console
makepkg -s
sudo pacman -U 501webapp-1.0.0-1-any.pkg.tar.zst
```

- Special notes about Arch:
  - To resolve any dependencies, we use the `-s` flag with `makepkg` every time
    - This is necessary because this package has a long list of dependencies
  - The name of the directory containing the package files does not matter
  - `PKGBUILD` is the instruction file, not a directory as might be expected with other package builders
  - `makepkg` must be run from the same directory containing `PKGBUILD`
  - The `.pkg.tar.zst` file will appear inside the containing directory
  - When the package is removed, the `501` web directory is also removed

| **Remove Arch package** :$ (optional)

```console
sudo pacman -R 501webapp
```

### II. Debian Package (`501webapp.deb`)
*Debian package directory structure:*

| **`deb/`** :

```
deb/
└─501webapp/
  └─DEBIAN/
    ├─control
    └─postinst
```

- Create directories: `deb/501webapp/DEBIAN`
- In `DEBIAN/` create file: `control`

| **`deb/501webapp/DEBIAN/control`** :

```
Package: 501webapp
Version: 1.0.0
Section: web
Priority: optional
Architecture: all
Maintainer: inkVerb <501webapp@inkisaverb.com>
Depends: bash (>= 4.0), apache2, php, libxml2-utils, xmlstarlet, imagemagick, ffmpeg, libmp3lame0, pandoc, texlive-latex-base, texlive-fonts-recommended, texlive-latex-recommended
Build-Depends: git
Description: The VIP Code 501 CMS web app-as-package
```

- In `DEBIAN/` create file: `postinst`
  - Make it executable with :$ `chmod +x DEBIAN/postinst`

| **`deb/501webapp/DEBIAN/postinst`** :

```
#!/bin/bash

# exit from any errors
set -e

# Build (git clone)
rm -rf /tmp/501
git clone https://github.com/inkVerb/501 /tmp/501

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

# Move proper folder into place
mv /tmp/501/cms ${webdir}/501
chown -R $webuser:$webuser /${webdir}/501
rm -rf /tmp/501

# Set up the directory
cd ${webdir}/501
mv htaccess .htaccess
mkdir -p media/docs media/audio media/video media/images media/uploads media/original/images media/original/video media/original/audio media/original/docs media/pro

chown -R $webuser:$webuser ${webdir}/501
```

- In `DEBIAN/` create file: `postrm`
  - Make it executable with :$ `chmod +x DEBIAN/postrm`

| **`deb/501webapp/DEBIAN/postrm`** :

```
#!/bin/bash
set -e

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

if [ "$1" = "purge" ]; then
    rm -rf ${webdir}/501
fi
```

- You will need to have certain dependencies installed even before building the package
  - These should already be installed from [Linux 501](https://github.com/inkVerb/VIP/blob/master/501/README.md), but are here for reference if needed

| **Install dependencies** :$

```console
sudo apt-get install apache2 php libxml2-utils xmlstarlet imagemagick ffmpeg libmp3lame0 pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-recommended
```

- Build package:
  - Navigate to directory `deb/`
  - Run this, then the package will be built, then installed:

| **Build, *then* install Debian package** :$

```console
dpkg-deb --build 501webapp  # Create the .deb package
sudo dpkg -i 501webapp.deb  # Install the package
```

- Special notes about Debian
  - The directory of the package files (`501webapp/`) will be the same as the package installer's `.deb` basename
  - The package installer will appear at `501webapp.deb` in the same directory as (`501webapp/`) regardless of the PWD from where the `dpkg-deb --build` command was run
    - For `deb/501webapp` it will be at `deb/501webapp.deb`
  - The web app folder `/var/www/501/` remains after package removal, only deleted with a purge (which uses `postrm`)
    - That folder and its files do not reside inside the package, so they are not included in a remove operation
    - Workflow of `dpkg`:
      1. Files residing inside the package are automatically put in place (actual installation)
        - There is no script that defines or lists these, only the directory structure, such as `usr/...` or `etc/...` inside the package directory, in this case `deb/501webapp/`, which has no such resident contents
        - Any files listed in `conffiles` will be left in place on removal, but deleted in a purge
      2. `postinst` runs (*after* actual installation)
        - Things done here are only reversed via purge through the `postrm` script

| **Remove Debian package** :$

```console
sudo apt-get remove 501webapp
```

| **Purge Debian package** :$

```console
sudo apt-get remove --purge 501webapp
```

### III. RPM Package (`501webapp-1.0.0-1.noarch.rpm`)
*RPM package directory structure:*

***Note this is probably broken on RedHat distros because of the lacking `pandoc` package***

| **`rpm/`** :

```
rpm/
└─rpmbuild/
  └─SPECS/
    └─501webapp.spec
```

- Create directories: `rpm/rpmbuild/SPECS`
- In `SPECS/` create file: `501webapp.spec`

| **`rpm/rpmbuild/SPECS/501webapp.spec`** :

```
Name:           501webapp
Version:        1.0.0
Release:        1%{?dist}
Summary:        The VIP Code 501 CMS web app-as-package

License:        GPL
URL:            https://github.com/inkVerb/501webapp

BuildArch:      noarch
Requires:       bash, httpd, php, mariadb, libxml2, xmlstarlet, ImageMagick, ffmpeg, lame, pandoc, texlive-scheme-full
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

%install
# Everything is done post-install

%files
# None, since we are doing everything under %post

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
rm -rf /tmp/501

# Set up the directory
cd ${webdir}/501
mv htaccess .htaccess
mkdir -p media/docs media/audio media/video media/images media/uploads media/original/images media/original/video media/original/audio media/original/docs media/pro

chown -R $webuser:$webuser ${webdir}/501

%changelog
-------------------------------------------------------------------
Thu Jan 01 00:00:00 UTC 1970 501webapp@inkisaverb.com
- Something started, probably with v1.0.0
```

- Install the `rpm-build` and `rpmdevtools` packages

| **RedHat/CentOS** :$

```console
sudo dnf update
sudo dnf install rpm-build rpmdevtools
```

| **OpenSUSE** :$

```console
sudo zypper update
sudo zypper install rpm-build rpmdevtools
```

- You will need to have certain dependencies installed even before building the package
  - These were not normally installed from [Linux 501](https://github.com/inkVerb/VIP/blob/master/501/README.md) because `rpm` architectures (RedHat/CentOS & OpenSUSE) are not supported
  - But, these are here for reference if needed

| **Install dependencies on RedHat/CentOS** :$ (will break because `pandoc` is required, but not supported)

```console
sudo dnf update
sudo dnf install httpd php mariadb libxml2 xmlstarlet imagemagick ffmpeg lame pandoc texlive-scheme-full
```

| **Install dependencies on OpenSUSE** :$

```console
sudo zypper update
sudo zypper install httpd php mariadb libxml2 xmlstarlet ImageMagick ffmpeg lame pandoc texlive-scheme-full
```

- Build package:
  - Navigate to directory `rpm/`
  - Run the following commands:

| **Build, *then* install RPM package** :$

```console
cp -r rpmbuild ~/
rpmbuild -ba ~/rpmbuild/SPECS/501webapp.spec                     # Create the .rpm package
ls ~/rpmbuild/RPMS/noarch/                                       # Check the .rpm filename
sudo rpm -i ~/rpmbuild/RPMS/noarch/501webapp-1.0.0-1.noarch.rpm  # Install the package (filename may be different)
```

- Special notes about RPM:
  - RPM requires the build be done from `~/rpmbuild/`
  - The resulting `.rpm` fill will be at: `~/rpmbuild/RPMS/noarch/501webapp-1.0.0-1.noarch.rpm`
    - This file might actually have a different name, but should be in the same directory (`~/rpmbuild/RPMS/noarch/`)
  - `noarch` means it works on any architecture
    - This part of the filename was set in the `.spec` file with `BuildArch: noarch`
  - The web app folder `/srv/www/501/` remains after package removal
    - That folder and its files do not reside inside the package, so they are not included in a remove operation
    - The `501` directory was copied after a `git clone` under `%post`
  - The `%changelog` is for OpenSUSE's `zypper`
    - RedHat/CentOS will want the date line like this:
      - `* Thu Jan 01 1970 Jesse <501webapp@inkisaverb.com> - 1.0.0-1`

| **Remove RedHat/CentOS package** :$ (optional)

```console
sudo dnf remove 501webapp
```

| **Remove OpenSUSE package** :$ (optional)

```console
sudo zypper remove 501webapp
```