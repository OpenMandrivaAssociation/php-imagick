%define realname Imagick
%define modname imagick
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 55_%{modname}.ini
%define mod_src %{modname}.c

Summary:	Provides a wrapper to the Image Magick Library for PHP
Name:		php-%{modname}
Version:	2.0.0
Release:	%mkrel 0.a3.3
Group:		System/Servers
License:	PHP License
URL:		http://pecl.php.net/package/imagick
Source0:	%{modname}-%{version}a3.tar.bz2
BuildRequires:  php-devel >= 3:5.2.0
BuildRequires:	XFree86-devel
BuildRequires:	freetype-devel
BuildRequires:	freetype2-devel
BuildRequires:	ImageMagick-devel >= 6.2.4
BuildRequires:	bzip2-devel
BuildRequires:	libjbig-devel
BuildRequires:	lcms-devel
BuildRequires:	zlib-devel >= 1.1.4
BuildRequires:	chrpath
Requires:	ImageMagick
Requires:	freetype
Requires:	freetype2
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-root

%description
This is a dynamic shared object (DSO) that adds Imagick support to PHP.

imagick is a native php-extension. See the examples in the
%{_docdir}/%{name}-%{version}/examples directory
for some hints on how to use it. 

%prep

%setup -q -n imagick-%{version}a3

%build

phpize
%configure2_5x \
    --with-imagick

%make
mv modules/*.so .
chrpath -d %{soname}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > README.%{modname} <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc examples CREDITS INSTALL README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
