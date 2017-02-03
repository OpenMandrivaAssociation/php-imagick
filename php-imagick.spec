%define realname Imagick
%define modname imagick
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 55_%{modname}.ini
%define mod_src %{modname}.c
%define beta %{nil}

Summary:	Provides a wrapper to the ImageMagick library for PHP
Name:		php-%{modname}
Version:	3.4.3
Release:	1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/imagick
Source0:	http://pecl.php.net/get/imagick-%{version}%{beta}.tgz
BuildRequires:  php-devel >= 3:5.2.0
BuildRequires:	imagemagick-devel >= 6.3.8
Requires:	imagemagick >= 6.3.8
Requires:	freetype
Epoch:		1

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
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install

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

%files 
%doc examples CREDITS README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
