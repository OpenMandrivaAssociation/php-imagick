%define realname Imagick
%define modname imagick
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 55_%{modname}.ini
%define mod_src %{modname}.c

Summary:	Provides a wrapper to the ImageMagick library for PHP
Name:		php-%{modname}
Version:	2.2.0
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/imagick
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:  php-devel >= 3:5.2.0
BuildRequires:	X11-devel
BuildRequires:	freetype-devel
BuildRequires:	freetype2-devel
BuildRequires:	imagemagick-devel >= 6.3.8
BuildRequires:	bzip2-devel
BuildRequires:	libjbig-devel
BuildRequires:	lcms-devel
BuildRequires:	zlib-devel >= 1.1.4
Requires:	imagemagick >= 6.3.8
Requires:	freetype
Requires:	freetype2
Epoch:		1
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Imagick is a native php extension to create and modify images using the
ImageMagick API.

imagick is a native php-extension. See the examples in the
%{_docdir}/%{name}/examples directory for some hints on
how to use it.

%prep

%setup -q -n imagick-%{version}
[ "../package.xml" != "/" ] && mv -f ../package.xml .

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

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

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc examples CREDITS INSTALL README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
