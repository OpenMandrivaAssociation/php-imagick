%define realname Imagick
%define modname imagick
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 55_%{modname}.ini
%define mod_src %{modname}.c

Summary:	Provides a wrapper to the ImageMagick library for PHP
Name:		php-%{modname}
Version:	3.1.2
Release:	1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/imagick
Source0:	http://pecl.php.net/get/imagick-%{version}.tgz
BuildRequires:  php-devel >= 3:5.2.0
BuildRequires:	imagemagick-devel >= 6.3.8
Requires:	imagemagick >= 6.3.8
Requires:	freetype
Requires:	freetype2
Epoch:		1

%description
Imagick is a native php extension to create and modify images using the
ImageMagick API.

imagick is a native php-extension. See the examples in the
%{_docdir}/%{name}/examples directory for some hints on
how to use it.

%prep

%setup -q -n imagick-%{version}RC2
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

%clean

%files 
%doc examples CREDITS INSTALL README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 1:3.1.0-0.0.RC2.1mdv2012.0
+ Revision: 806386
- 3.1.0RC2
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-9
+ Revision: 761259
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-8
+ Revision: 696435
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-7
+ Revision: 695410
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-6
+ Revision: 646652
- rebuilt for php-5.3.6

* Mon Feb 07 2011 Funda Wang <fwang@mandriva.org> 1:3.0.1-5
+ Revision: 636558
- tighten BR

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-4mdv2011.0
+ Revision: 629814
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-3mdv2011.0
+ Revision: 628135
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-2mdv2011.0
+ Revision: 600499
- rebuild

* Mon Nov 22 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-1mdv2011.0
+ Revision: 599692
- 3.0.1

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-0.0.RC2.2mdv2011.0
+ Revision: 588837
- rebuild

* Thu Sep 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.1-0.0.RC2.1mdv2011.0
+ Revision: 578873
- 3.0.1RC2

* Thu Jul 15 2010 Funda Wang <fwang@mandriva.org> 1:3.0.0-0.0.RC2.1mdv2011.0
+ Revision: 553490
- new version 3.0.0 RC2

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.0-0.0.RC1.2mdv2010.1
+ Revision: 514561
- rebuilt for php-5.3.2

* Mon Mar 01 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.0-0.0.RC1.1mdv2010.1
+ Revision: 512913
- 3.0.0RC1
- better versioning

* Sun Jan 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.0b2-1mdv2010.1
+ Revision: 495450
- 3.0.0b2

* Thu Jan 14 2010 Funda Wang <fwang@mandriva.org> 1:3.0.0b1-3mdv2010.1
+ Revision: 491456
- rebuild for new imagemagick

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.0b1-2mdv2010.1
+ Revision: 485395
- rebuilt for php-5.3.2RC1

* Sat Dec 19 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.0b1-1mdv2010.1
+ Revision: 480117
- 3.0.0b1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.3.0-3mdv2010.1
+ Revision: 468177
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.3.0-2mdv2010.0
+ Revision: 451281
- rebuild

* Wed Jul 29 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.3.0-1mdv2010.0
+ Revision: 403392
- 2.3.0

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.3.0-0.RC1.1mdv2010.0
+ Revision: 376960
- 2.3.0RC1

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.2-3mdv2009.1
+ Revision: 346505
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.2-2mdv2009.1
+ Revision: 341767
- rebuilt against php-5.2.9RC2

* Sat Feb 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.2-1mdv2009.1
+ Revision: 338375
- 2.2.2

* Wed Jan 28 2009 Götz Waschk <waschk@mandriva.org> 1:2.2.2-0.0.RC3.2mdv2009.1
+ Revision: 335034
- rebuild for new libmagick

* Sun Jan 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.2-0.0.RC3.1mdv2009.1
+ Revision: 330986
- 2.2.2RC3

* Tue Jan 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.2-0.0.RC2.1mdv2009.1
+ Revision: 329194
- 2.2.2RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.2-0.0.RC1.2mdv2009.1
+ Revision: 321802
- rebuild

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.2-0.0.RC1.1mdv2009.1
+ Revision: 321647
- 2.2.2RC1

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.1-2mdv2009.1
+ Revision: 310277
- rebuilt against php-5.2.7

* Tue Oct 28 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.1-1mdv2009.1
+ Revision: 297806
- 2.2.1

* Tue Sep 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.1-0.RC2.1mdv2009.0
+ Revision: 283045
- 2.2.1RC2

* Sat Aug 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.1-0.RC1.1mdv2009.0
+ Revision: 275328
- 2.2.1RC1

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.0-2mdv2009.0
+ Revision: 238404
- rebuild

* Thu Jul 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.0-1mdv2009.0
+ Revision: 233359
- 2.2.0

* Fri Jun 13 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.0-0.1.rc1.1mdv2009.0
+ Revision: 218775
- 2.2.0RC1

* Tue May 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.0-0.b2.1mdv2009.0
+ Revision: 202145
- 2.2.0b2

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.0-0.b1.2mdv2009.0
+ Revision: 200244
- rebuilt for php-5.2.6

* Wed Apr 30 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2.0-0.b1.1mdv2009.0
+ Revision: 199432
- 2.2.0b1

* Mon Mar 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-1mdv2008.1
+ Revision: 183288
- 2.1.1

* Sun Feb 24 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.1-1.RC1.1mdv2008.1
+ Revision: 174388
- 2.1.1RC1, obsoletes the patch

* Mon Feb 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.0-1mdv2008.1
+ Revision: 165096
- 2.1.0

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.0-0.RC3.2mdv2008.1
+ Revision: 162100
- rebuild

* Mon Jan 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.0-0.RC3.1mdv2008.1
+ Revision: 151162
- 2.1.0RC3

* Tue Jan 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.0-0.RC2.2mdv2008.1
+ Revision: 146469
- rebuilt against new imagemagick libs (6.3.7)

* Wed Dec 26 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1.0-0.RC2.1mdv2008.1
+ Revision: 137936
- 2.1.0RC2

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.1-2mdv2008.1
+ Revision: 107672
- restart apache if needed

* Thu Oct 25 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.1-1mdv2008.1
+ Revision: 102005
- 2.0.1

* Wed Oct 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-2mdv2008.0
+ Revision: 94891
- 2.0.0
- 2.0.0RC4
- 2.0.0RC3
- fix deps
- 2.0.0RC2

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-1.RC1.2mdv2008.0
+ Revision: 77550
- rebuilt against php-5.2.4

* Fri Aug 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-1.RC1.1mdv2008.0
+ Revision: 64725
- rebuild
- bump release
- bump release
- 2.0.0RC1

* Mon Jul 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.b3.1mdv2008.0
+ Revision: 52505
- 2.0.0b3

* Sun Jul 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.b2.1mdv2008.0
+ Revision: 46482
- 2.0.0b2

* Tue Jun 19 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.b1.1mdv2008.0
+ Revision: 41388
- 2.0.0b1

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.a3.4mdv2008.0
+ Revision: 39502
- use distro conditional -fstack-protector
- fix deps

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.a3.2mdv2008.0
+ Revision: 33812
- rebuilt against new upstream version (5.2.3)

* Wed May 30 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.a3.1mdv2008.0
+ Revision: 32748
- 2.0.0a3

* Mon May 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.a2.1mdv2008.0
+ Revision: 24032
- 2.0.0a2

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.9.13-2mdv2008.0
+ Revision: 21335
- rebuilt against new upstream version (5.2.2)

* Wed Apr 18 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.9.13-1mdv2008.0
+ Revision: 14496
- 0.9.13


* Wed Mar 21 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.11-6mdv2007.1
+ Revision: 147245
- rebuild

* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.9.11-5mdv2007.1
+ Revision: 117589
- rebuilt against new upstream version (5.2.1)

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.9.11-4mdv2007.1
+ Revision: 79291
- rebuild
- rebuilt for php-5.2.0
- Import php-imagick

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.9.11-2
- rebuilt for php-5.1.6

* Sat Aug 05 2006 Emmanuel Andry <eandry@mandriva.org> 1:0.9.11-1mdv2007.0
- fork for PHP5

* Wed Jul 26 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.9.11-3mdk
- rebuild

* Mon Jan 16 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.9.11-2mdk
- rebuilt against php-4.4.2

* Wed Nov 02 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.9.11-1mdk
- rebuilt for php-4.4.1
- fix versioning

* Thu Aug 25 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0_0.9.11-2mdk
- rebuilt against new Magick libs

* Tue Jul 12 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-1mdk
- rebuilt for php-4.4.0 final

* Wed Jul 06 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-0.RC2.1mdk
- rebuilt for php-4.4.0RC2

* Wed Jun 15 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0_0.9.11-0.RC1.1mdk
- rebuilt for php-4.4.0RC1

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_0.9.11-1mdk
- renamed to php4-*

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_0.9.11-1mdk
- 4.3.11

* Mon Mar 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.9.11-4mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.9.11-3mdk
- rebuilt against a non hardened-php aware php lib

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.9.11-2mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.9.11-1mdk
- rebuild for php 4.3.10

* Wed Nov 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_0.9.11-2mdk
- nuke redundant provides

* Sat Oct 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_0.9.11-1mdk
- rebuild for php 4.3.9

* Mon Aug 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_0.9.11-2mdk
- rebuilt against new imagick libs

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_0.9.11-1mdk
- 0.9.11
- built for php 4.3.8

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_0.9.9-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php4.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_0.9.9-1mdk
- 0.9.9
- fix url
- built for php 4.3.6


