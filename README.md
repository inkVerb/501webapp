# 501webapp
*The VIP Code 501 CMS web app-as-package*

## Create the simple Linux install package for `501webapp`
This is a guide to create a web app-as-package installer for the 501 CMS from [Linux 501: PHP-XML Stack](https://github.com/inkVerb/VIP/blob/master/501/README.md) on:
1. Arch (Manjaro, Black Arch, et al)
2. Debian (Ubuntu, Kali, Mint, et al)
3. RPM (OpenSUSE supported; *RedHat/CentOS distros not supported due to missing `ImageMagick`, `ffmpeg`, `pandoc` & `texlive-scheme-full` packages*)

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
- These packages are only a most-basic way to get a simple Git repo installed, updated, or removed with SQL database on a prepared server through the package manager
- About updates
  - Advantages of these packages:
    - Works on a simple GitHub repo, using the most current commit, without needing to publish [releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
    - Whether used from the Arch AUR, local Arch, Debian, or RPM package, it will install the most current version of the [501](https://github.com/inkVerb/501) web app in the repo
    - Can use the package manager to cleanly install or uninstall
    - The SQL database is created by web app defaults, then backed up and removed on package install, update, remove, and purge operations
    - Theoretically, this package could update the web app (via pachless refresh) by only changing the version in the package configs
  - A web app should have an update patch workflow written into the app's server side language
  - A web app production package should depend on GitHub [releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) as done in [`gophersay-git`](https://github.com/JesseSteele/gophersay-git)
    - The proper way would be for the package to run the web updater with something like `su www -c 'php 501/updater.php`
  - This has neither
  - Only the Arch package checks for current versions (by Git commit, not release) and would list available updates
    - Only by replaceing all files except `in.conf.php` (more of a refresh, not an update patch)

Working examples for each already resides in this repository

### Create and install the `501webapp` package directly from this repo

| **Arch** :$ (& Manjaro, Black Arch)

```console
git clone https://github.com/inkVerb/501webapp.git
cd 501webapp/arch
makepkg -si
```

| **Debian** :$ (& Ubuntu, Kali, Mint)

(install build tools if not already)

```console
sudo apt-get update
sudo apt-get install dpkg-dev debhelper
```

(install dependencies for this package - will receive error if not)

```console
sudo apt-get install apache2 php mariadb-server libxml2-utils xmlstarlet imagemagick ffmpeg libmp3lame0 pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-recommended
```

```console
git clone https://github.com/inkVerb/501webapp.git
cd 501webapp/deb/build
sudo dpkg-buildpackage -us -uc
cd debian
dpkg-deb --build 501webapp
sudo dpkg -i 501webapp.deb
```

| **RedHat/CentOS** :$ (& Fedora)

(install build tools if not already)

```console
sudo dnf update
sudo dnf install rpm-build rpmdevtools
```

(dependency packages may not be available on RedHat distro repos; package will not install)

```console
git clone https://github.com/inkVerb/501webapp.git
cp -rf 501webapp/rpm/rpmbuild ~/
rpmbuild -ba ~/rpmbuild/SPECS/501webapp.spec
ls ~/rpmbuild/RPMS/noarch/
sudo rpm -i ~/rpmbuild/RPMS/noarch/501webapp-1.0.0-1.noarch.rpm  # Change filename if needed
rm -rf ~/rpmbuild
```

| **OpenSUSE** :$ (& Tumbleweed)

(install build tools if not already)

```console
sudo zypper update
sudo zypper install rpm-build rpmdevtools
```

(install dependencies for this package - will receive error if not)

```console
sudo zypper update
sudo zypper install httpd php mariadb libxml2 xmlstarlet ImageMagick ffmpeg lame pandoc texlive-scheme-full
```

```console
git clone https://github.com/inkVerb/501webapp.git
cd 501webapp/rpm
cp -r rpmbuild ~/
rpmbuild -ba ~/rpmbuild/SPECS/501webapp.spec
ls ~/rpmbuild/RPMS/noarch/
sudo rpm -i ~/rpmbuild/RPMS/noarch/501webapp-1.0.0-1.noarch.rpm  # Change filename if needed
rm -rf ~/rpmbuild
```

## Detailed instructions per architecture
Instructions explain each in detail to create these packages from scratch...

### Architecture Package Differences
The Arch package builder is very different from Debian and RPM in its capability of building a package automatically

This Arch `PKGBUILD` script will download and place all the files for PHP web app inside the actual package itself

But, Debian and RPM packages require so much work, especially RPM, that it would be easier, faster, and have less risk of mistake to download the package and manually place the web app's files inside the package without automation

Because of the Arch structure, we use a function for `pkgver=`, so that the `git` repo with the PHP web app will reflect the latest version on `git`, but this `PKGBUILD` file never needs to be updated

*This gets into **[the Arch Way](https://wiki.archlinux.org/title/Arch_terminology#The_Arch_Way)** — the basic philosophy & [principles behind Arch Linux](https://wiki.archlinux.org/title/Arch_Linux#Principles) being easier to manage as a bleeding edge distro, which the [gophersay-git](https://github.com/JesseSteele/gophersay-git) package instructions discuss at greater length*

If you want the PHP web app inside the Debian or RPM installers, you will need to do the heavy lifting yourself; you could write a script to automate the in-package wep app creation, but that would be even heavier lifting

This page demonstrates simple automated scripts to create packages to install a web app from `git` automatically; Arch makes it simple to place that app inside the actual package, while the Debian and RPM packages—being more complex—are better off with a package that merely contains a script for the machine to download the web app from `git` directly

### I. Arch Linux Package (`501webapp-1.0.0-1-any.pkg.tar.zst`)
*Arch package directory structure:*

| **`arch/`** :

```
arch/
├─ PKGBUILD
└─ structure.install
```

- Create directory: `arch`
- In `arch/` create file: `PKGBUILD`

| **`arch/PKGBUILD`** :

```
# Maintainer: Ink Is A Verb <codes@inkisaverb.com>
pkgname=501webapp
pkgver=1  # Must not be empty (can be anything), later replaced with the pkgver() function, getting the version from git so this does not need to be re-written on every release
pkgrel=1
pkgdesc="The VIP Code 501 CMS web app-as-package"
url="https://github.com/inkVerb/501webapp"
arch=('any')
license=('GPL')
depends=('bash' 'apache' 'php' 'mariadb' 'libxml2' 'xmlstarlet' 'imagemagick' 'ffmpeg' 'lame' 'pandoc' 'texlive-core' 'texlive-latex' 'texlive-fontsrecommended' 'texlive-latexrecommended')  # Apache becuase we use rewrites
makedepends=('git')
source=('git+https://github.com/inkVerb/501.git')
sha256sums=('SKIP')
install=('structure.install')
# Preserve when uninstalled, delete when purged
backup=("/etc/${pkgname}/in.conf.php" "/etc/${pkgname}/blog_db.sql")

# Dynamically set pkgver= variable based on unique source versioning
# Can go anywhere in PKGBUILD file, but usually variables are first, then functions after
pkgver() {
  cd "$pkgdir" # Same as "$srcdir/501"
    ( set -o pipefail
      git describe --long --tags --abbrev=7 2>/dev/null | sed 's/\([^-]*-g\)/r\1/;s/-/./g' ||
      git describe --long --abbrev=7 2>/dev/null | sed 's/\([^-]*-g\)/r\1/;s/-/./g' ||
      printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short=7 HEAD)"
  )
}

build() {
  cd "$pkgdir" # Same as "$srcdir/501"
}

package() {
  # Figure out the web user
  webuser=$(ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
  if [ -d "/srv/www" ]; then
    webdir="srv/www"
  elif [ -d "/var/www" ]; then
    webdir="var/www"
  else
    echo "No web folder found."
    exit 1
  fi

  # Move files in place
  cd "$pkgdir" # Same as "$srcdir/501"
  install -d "${pkgdir}/${webdir}"
  cp -r cms "${pkgdir}/${webdir}/501"
  
  # Protect the config file
  install -d "${pkgdir}/etc/${pkgname}"
  mv "${pkgdir}/${webdir}/501/in.conf.php" "${pkgdir}/etc/${pkgname}/"
  ln -s "/etc/${pkgname}/in.conf.php" "${pkgdir}/${webdir}/501/in.conf.php"
  
  # Web directory structure
  cd "${pkgdir}/${webdir}/501"
  mv htaccess .htaccess
  mkdir -p media/docs media/audio media/video media/images media/uploads media/original/images media/original/video media/original/audio media/original/docs media/pro

  # Own web directory
  chown -R $webuser:$webuser "${pkgdir}/${webdir}/501"
}
```

- In `arch/` create file: `structure.install`
  - This file is referenced in `PKGBUILD` by `install=('structure.install')`, but could have any name with the extension `.install`
  - Learn more about `.install` files on [Arch Wiki: PKGBUILD](https://wiki.archlinux.org/title/PKGBUILD#install)
  - This leaves notes and unused, available functions from the [prototype demo file](https://gitlab.archlinux.org/pacman/pacman/raw/master/proto/proto.install)

| **`arch/structure.install`** :

```
## arg 1:  the new package version
#pre_install() {
	# do something here
#}

## arg 1:  the new package version
post_install() {
  echo "See README.md inside the 501/ directory for further install instructions
}

## arg 1:  the new package version
## arg 2:  the old package version
#pre_upgrade() {
	# do something here
#}

## arg 1:  the new package version
## arg 2:  the old package version
#post_upgrade() {
	# do something here
#}

## arg 1:  the old package version
#pre_remove() {
	# do something here
#}

## arg 1:  the old package version
#post_remove() {
	# do something here
#}
```

...the above `structure.install` file would work just the same if it only contained...

```
post_install() {
  echo "See README.md inside the 501/ directory for further install instructions
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
  - Arch runs `PKGBUILD` and any `.install` scripts as `chroot`
    - This is different from Debian or RPM
    - Being done in `chroot`, [the SQL database can't be](https://serverfault.com/questions/217127/) created, removed, backed up, or otherwise handled during install/update/remove operations
    - This relates to the same `chroot` environment as in the [**`toplogger`**](https://github.com/inkVerb/toplogger) package
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
└─ build/
   └─ debian/
      ├─ control
      ├─ conffiles
      ├─ preinst
      ├─ postinst
      ├─ prerm
      ├─ postrm
      ├─ compat
      ├─ changelog
      ├─ copyright
      ├─ install
      └─ rules
```

#### Create Mainainer Package Director Structure
- Create directories: `deb/build/debian`
- In `debian/` create file: `control`

| **`deb/build/debian/control`** :

```
Source: 501webapp
Section: web
Priority: optional
Maintainer: Ink Is A Verb <codes@inkisaverb.com>
Homepage: https://github.com/inkverb/501webapp
Vcs-Git: https://github.com/inkverb/501
Build-Depends: debhelper (>= 10)
Standards-Version: 3.9.6

Package: 501webapp
#Version: 1.0.0 # No! Inherited from `debian/changelog`
Architecture: all
Depends: bash (>= 4.0), apache2, php, mariadb-server, libxml2-utils, xmlstarlet, imagemagick, ffmpeg, libmp3lame0, pandoc, texlive-latex-base, texlive-fonts-recommended, texlive-latex-recommended
Description: The VIP Code 501 CMS web app-as-package
```

- In `debian/` create file: `conffiles`
  - This file technically isn't needed because all files in `etc/` are automatically included as `conffiles`; this is here for example

| **`deb/build/debian/conffiles`** :

```
/etc/501webapp/in.conf.php
```

- In `debian/` create file: `preinst`
  - Make it executable with :$ `chmod +x debian/preinst`

| **`deb/build/debian/preinst`** :

```
#!/bin/bash

# exit from any errors
set -e

# Determine web user and folder & create any needed symlink
webuser=$(ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
if [ -d "/srv/www" ]; then
  webdir="/srv/www"
  mkdir -p "/var/"
  ln -sfn "/srv/www" "/var/"
elif [ -d "/var/www" ]; then
  webdir="/var/www"
else
  mkdir -p "/var/www"
  webdir="/var/www"
fi
```

- In `debian/` create file: `postinst`
  - Make it executable with :$ `chmod +x debian/postinst`
  - We want the database and web directory addressed here, *after* the dependency checks during install

| **`deb/build/debian/postinst`** :

```
#!/bin/bash

# exit from any errors
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

# Export the current database
mkdir -p /var/501webapp
rm -f /var/501webapp/blog_db.sql
mariadb-dump blog_db > /var/501webapp/blog_db.sql
ln -sfn /var/501webapp/blog_db.sql /etc/501webapp/

# Web directory structure
cd ${webdir}/501
mv htaccess .htaccess
mkdir -p media/docs media/audio media/video media/images media/uploads media/original/images media/original/video media/original/audio media/original/docs media/pro

# Own web directory
chown -R $webuser:$webuser ${webdir}/501

# Create the database
mariadb -e "
CREATE DATABASE IF NOT EXISTS blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON blog_db.* TO 'blog_db_user'@'localhost' IDENTIFIED BY 'blogdbpassword';
FLUSH PRIVILEGES;"
```

- In `debian/` create file: `prerm`
  - Make it executable with :$ `chmod +x debian/prerm`

| **`deb/build/debian/prerm`** :

```
#!/bin/bash
set -e

# Example of something
echo "Removing the 501 web app..."
```

- In `debian/` create file: `postrm`
  - Make it executable with :$ `chmod +x debian/postrm`

| **`deb/build/debian/postrm`** :

```
#!/bin/bash
set -e

# Determine web user and folder
webuser=$(ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
if [ -d "/srv/www/501" ]; then
  webdir="/srv/www"
  # Remove /var/www only if it is a symlink
  [ -L "/var/www" ] && rm "/var/www"
elif [ -d "/var/www/501" ]; then
  webdir="/var/www"
else
  echo "No web folder found."
  exit 0
fi

# Drop database on purge
if [ "$1" = "purge" ]; then
  rm -rf ${webdir}/501
  rm -rf /etc/501webapp
  rm -rf /var/501webapp
  mariadb -e "
  DROP USER IF EXISTS 'blog_db_user'@'localhost';
  DROP DATABASE IF EXISTS blog_db;
  FLUSH PRIVILEGES;"
else
  # Dump database on simple remove
  mkdir -p /var/501webapp
  rm -f /var/501webapp/blog_db.sql
  mariadb-dump blog_db > /var/501webapp/blog_db.sql
  ln -sfn /var/501webapp/blog_db.sql /etc/501webapp/
fi
```

- In `debian/` create file: `compat`

| **`deb/build/debian/compat`** : (`debhelper` minimum version)

```
10
```

- In `debian/` create file: `changelog`

| **`deb/build/debian/changelog`** : (optional, for listing changes)

```
501webapp (1.0.0-1) stable; urgency=low

  * First release

 -- Ink Is A Verb <codes@inkisaverb.com>  Thu, 1 Jan 1970 00:00:00 +0000
```

- In `debian/` create file: `copyright`

| **`deb/build/debian/copyright`** : (optional, may be legally wise)

```
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: 501webapp
Source: https://github.com/inkverb/501webapp

Files: *
Copyright: 2024, Ink Is A Verb <codes@inkisaverb.com>
License: GPL-3+
```

- In `debian/` create file: `rules`
  - Make it executable with :$ `chmod +x debian/rules`

| **`deb/build/debian/rules`** : (build, but no compiled binaries)

```
#!/usr/bin/make -f

%:
	dh $@

override_dh_auto_build:
	git clone https://github.com/inkVerb/501
```

- In `debian/` create file: `install`

| **`deb/build/debian/install`** : (places files in the `.deb` directory structure)

```
501/cms/* var/www/501/
501/cms/in.conf.php etc/501webapp/
```

#### Build the Package Directories
- Install the `dpkg-dev` & `debhelper` packages

| **Install Debian `dpkg-dev` package** :$

```console
sudo apt-get update
sudo apt-get install dpkg-dev debhelper
```

- Prepare package builder:
  - Navigate to directory `deb/build/`
  - Run this, then the package builder & repo packages will be created:

| **Prepare the Debian package builder** :$

```console
sudo dpkg-buildpackage -us -uc  # Create the package builder
```

- Note what just happened
  - Everything just done to this point is called "**maintainer**" work in the Debian world
  - Basic repo packages *and also* the package `DEBIAN/` builder structure were greated
  - At this point, one could navigate up one directory to `deb/` and run `sudo dpkg -i 501webapp_1.0.0-1_all.deb` and the package would be installed, *but we won't do this*
  - Once installed with `sudo dpkg -i` (later) this can be removed the standard way with `sudo apt-get remove 501webapp`
  - This is the new, just-created directory structure for the standard Debian package builder:

| **`deb/build/debian/`** :

```
deb/build/debian/
          └─ 501webapp/
             ├─ DEBIAN/
             │  ├─ control
             │  ├─ conffiles
             │  ├─ md5sums
             │  ├─ preinst
             │  ├─ postinst
             │  ├─ prerm
             │  └─ postrm
             ├─ etc/
             │  └─ 501webapp/
             │     └─ in.conf.php
             ├─ usr/
             │  └─ share/
             │     └─ doc/
             │        └─ 501webapp/
             │           ├─ changelog.Debian.gz
             │           └─ copyright
             └─ var/
                └─ www/
                   └─ 501/
                      └─ [ files from 501/cms/* ]
```

- You will need to have certain dependencies installed even before building the package
  - These should already be installed from [Linux 501](https://github.com/inkVerb/VIP/blob/master/501/README.md), but are here for reference if needed

| **Install dependencies** :$

```console
sudo apt-get install apache2 php mariadb-server libxml2-utils xmlstarlet imagemagick ffmpeg libmp3lame0 pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-recommended
```

- Build package:
  - Navigate to directory `deb/debian/`
  - Run this, then the package will be built, then installed:

| **Build, *then* install Debian package** :$

```console
dpkg-deb --build 501webapp  # Create the .deb package
sudo dpkg -i 501webapp.deb  # Install the package
```

- Special notes about Debian
  - The directory of the package files (`501webapp/`) will be the same as the package installer's `.deb` basename
  - Debian is unique offering `--purge`, making it both convenient and dangerous
    - The web app folder `/var/www/501/` remains after package removal, only deleted with a purge (which uses `postrm`)
    - That folder and its files do not reside inside the package, so they are not included in a remove operation, but only are removed with `--purge`-activated scripts
    - The workflow must be carefully selected; one error in an `install` or `remove` operation and the package will `exit` unfinished, then the system is stuck with a problem
    - If written wrong...
      - These scripts can cause serious errors, they can delete the `/var` or `/etc` directories, or do catastrophic damage
      - A mild `E:` error may be fixable with this :$
        - `sudo dpkg --remove --force-all 501webapp && sudo apt-get update`
      - This is why Arch runs scripts only as `chroot`, limiting `remove` vs `--purge` cabability, to prevent a faulty uninstall script from causing catastrophic damage
  - The package installer will appear at `501webapp.deb` in the same directory as (`501webapp/`) regardless of the PWD from where the `dpkg-deb --build` command was run
    - For `deb/501webapp` it will be at `deb/501webapp.deb`
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
└─ rpmbuild/
   └─ SPECS/
      └─ 501webapp.spec
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
if [ -d "/srv/www" ]; then
  webdir="/srv/www"
  mkdir -p "/var/"
  ln -sfn "/srv/www" "/var/"
elif [ -d "/var/www" ]; then
  webdir="/var/www"
else
  mkdir -p "/var/www"
  webdir="/var/www"
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

# Create the database
mariadb -e "
CREATE DATABASE IF NOT EXISTS blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON blog_db.* TO 'blog_db_user'@'localhost' IDENTIFIED BY 'blogdbpassword';
FLUSH PRIVILEGES;"

# Export the current database (such as upgrade)
mkdir -p /var/501webapp
rm -f /etc/501webapp/blog_db.sql
mariadb-dump blog_db > /var/501webapp/blog_db.sql

# Set up the web directory
cd ${webdir}/501
mv htaccess .htaccess
mkdir -p media/docs media/audio media/video media/images media/uploads media/original/images media/original/video media/original/audio media/original/docs media/pro
chown -R $webuser:$webuser ${webdir}/501

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

| **Install dependencies on OpenSUSE** :$

```console
sudo zypper update
sudo zypper install httpd php mariadb libxml2 xmlstarlet ImageMagick ffmpeg lame pandoc texlive-scheme-full
```

- ***RedHat/CentOS distros don't support all packages, so they need to be downloaded and installed with `rpm` separately***
  - *[ImageMagick](https://imagemagick.org/script/download.php)*
  - *[ffmpeg](https://src.fedoraproject.org/rpms/ffmpeg) (probably `x86_64`)*
    - *[ffmpeg official](https://www.ffmpeg.org/download.html) (no `rpm` package from vendor's site)*
  - *[pandoc](https://www.rpmfind.net/linux/rpm2html/search.php?query=pandoc)*
    -  *[pandoc official](https://pandoc.org/installing.html) (no `rpm` package from vendor's site)*
  - *[texlive-scheme-full](https://www.tug.org/texlive/)*
  - *Or search [pkgs.org](https://pkgs.org/)*
  - *Install with :$ `sudo rpm -i that-package-you-downloaded.rpm`*
  - *Using these, the dependencies in the `.spec` file's `Requires:` line should be the same*

| **Install dependencies on RedHat/CentOS** :$ (will break because `ImageMagick`, `ffmpeg`, `pandoc` & `texlive-scheme-full` are not supported)

```console
sudo dnf update
sudo dnf install httpd php mariadb libxml2 xmlstarlet lame
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
      - `* Thu Jan 01 1970 Ink Is A Verb <codes@inkisaverb.com> - 1.0.0-1`

| **Remove RedHat/CentOS package** :$ (optional)

```console
sudo dnf remove 501webapp
```

| **Remove OpenSUSE package** :$ (optional)

```console
sudo zypper remove 501webapp
```