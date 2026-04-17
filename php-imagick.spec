%define realname Imagick
%define modname imagick
%define soname %{modname}.so
%define inifile 55_%{modname}.ini
%define mod_src %{modname}.c
%define beta %{nil}
# Allow zend_* symbol references
%define _disable_ld_no_undefined 1

Summary:	Provides a wrapper to the ImageMagick library for PHP
Name:		php-%{modname}
Version:	3.8.1
Release:	1
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/imagick
Source0:	http://pecl.php.net/get/imagick-%{version}%{beta}.tgz
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:  php-devel >= 3:5.2.0
BuildRequires:	imagemagick-devel >= 7.0.0
Requires:	imagemagick >= 7.0.0
Requires:	freetype

%description
Imagick is a native php extension to create and modify images using the
ImageMagick API.

imagick is a native php-extension. See the examples in the
%{_docdir}/%{name}/examples directory for some hints on
how to use it.

%prep

%setup -qn %{modname}-%{version}%{beta}
[ "../package.xml" != "/" ] && mv -f ../package.xml .

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make_build LIBTOOL=rclibtool

%install
%make_install LIBTOOL=rclibtool INSTALL_ROOT=%{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP.
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[imagick]
imagick.locale_fix = 0
EOF

# We don't need the header, there are no other modules
# linking against this one
rm -rf %{buildroot}%{_includedir}

%files
%doc examples CREDITS README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
