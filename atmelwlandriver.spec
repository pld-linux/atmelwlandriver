#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	up		# don't build UP modules
%bcond_without	smp		# don't build SMP modules
%bcond_with	unicode		# use wx-gtk2-unicode-config instead of ansi
%bcond_without	userspace	# don't build userspace applications
%bcond_with	verbose		# verbose build (V=1)

%if !%{with kernel}
%undefine	with_dist_kernel
%endif

%define		_rel	0.9
Summary:	Linux driver for WLAN card based on AT76C5XXx
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart WLAN opartych na układach AT76C5XXx
Name:		atmelwlandriver
Version:	3.4.1.1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/atmelwlandriver/%{name}-%{version}.tar.bz2
# Source0-md5:	6cb3671091c7ccaa646222c50ee242c9
Source1:	%{name}-vnetrc
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-etc.patch
Patch2:		%{name}-usb-api.patch
Patch3:		%{name}-gcc4.patch
Patch4:		%{name}-winter-makefile.patch
Patch5:		%{name}-fwupgrade.patch
Patch6:		%{name}-cmdline.patch
#Patch2:	%{name}-fpmath.patch
#Patch3:	%{name}-delay.patch
#Patch4:	%{name}-usb_defctrl.patch
URL:		http://atmelwlandriver.sourceforge.net/
%if %{with kernel}
%if %{with dist_kernel}
BuildRequires:	kernel-module-build >= 3:2.6.11
BuildRequires:	kernel-source >= 2.6.11
%endif
BuildRequires:	rpmbuild(macros) >= 1.217
%endif
%if %{with userspace}
BuildRequires:	libusb-devel
BuildRequires:	ncurses-devel
BuildRequires:	ncurses-ext-devel
BuildRequires:	wxGTK2-%{?with_unicode:unicode-}devel >= 2.6.0
%endif
Requires:	wireless-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on ATMEL AT76C5XXx devices for
Linux.

%description -l pl.UTF-8
Sterownik dla Linuksa do kart sieci bezprzewodowych opartych o układy
ATMELA AT76C5XXx.

%package -n kernel-net-atmelwlandriver
Summary:	Linux driver for WLAN card based on AT76C5XXx
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart WLAN na układach AT76C5XXx
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel-net(atmelwlandriver) = %{version}

%description -n kernel-net-atmelwlandriver
This is driver for WLAN card based on ATMEL AT76C5XXx devices for
Linux.

%description -n kernel-net-atmelwlandriver -l pl.UTF-8
Sterownik dla Linuksa do kart sieci bezprzewodowych opartych o układy
ATMELA AT76C5XXx.

%package -n kernel-smp-net-atmelwlandriver
Summary:	Linux SMP driver for WLAN card based on AT76C5XXx
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do kart WLAN na układach AT76C5XXx
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel-net(atmelwlandriver) = %{version}

%description -n kernel-smp-net-atmelwlandriver
This is driver for WLAN card based on ATMEL AT76C5XXx devices for
Linux SMP.

%description -n kernel-smp-net-atmelwlandriver -l pl.UTF-8
Sterownik dla Linuksa SMP do kart sieci bezprzewodowych opartych o
układy ATMELA AT76C5XXx.

%package tools
Summary:	Command line tools for managing ATMEL Wireless Card
Summary(pl.UTF-8):	Narzędzia linii poleceń do obsługi bezprzewodowych kart ATMEL
Release:	%{_rel}
Group:		Networking/Utilities
Requires:	kernel-net(atmelwlandriver) = %{version}

%description tools
Managing tools for the ATMEL Wireless Card adapters. When the PCMCIA
module pcmf502*, the PCI module pcifvnet, or the USB module usbvnet*
is loaded the lvnet application can monitor the device's statistics or
change it's runtime parameters.

%description tools -l pl.UTF-8
Narzędzia do obsługi dla adapterów kart sieci bezprzewodowych ATMEL.
Kiedy moduł PCMCIA pcmf502*, moduł PCI pcifvnet, albo moduł USB
usbvnet* jest załadowany to aplikacja lvnet może monitorować dane
statystyczne urządzenia albo zmienić parametry jego pracy.

%package winter
Summary:	Graphical tool for monitoring ATMEL Wireless Cards
Summary(pl.UTF-8):	Graficzne narzędzie do monitorowania bezprzewodowych kart ATMEL
Release:	%{_rel}
Group:		Networking/Utilities
Requires:	kernel-net(atmelwlandriver) = %{version}

%description winter
Winter is an X application, that provides a visual environment to
configure and manage ATMEL cards. It's functionality is similar to
that of lvnet, extended by very useful features such as profiles,
localization and support for more than one devices alternatively.

%description winter -l pl.UTF-8
Winter jest aplikacją dla X, która dostarcza wizualne środowisko
pozwalające na konfigurację kart ATMELa. Jego funkcjonalność jest
podobna do tej jaką ma lvnet, dodatkowo rozszerzoną o bardzo przydatne
funkcje takie jak: profile, lokalizacje i wsparcie dla więcej niż
jednego urządzenia.

%package fucd
Summary:	Firmware upgrade tool for ATMEL Wireless Cards
Summary(pl.UTF-8):	Narzędzie aktualizacji bezprzewodowych kart ATMEL
Release:	%{_rel}
Group:		Networking/Utilities
Requires:	kernel-net(atmelwlandriver) = %{version}

%description fucd
Graphical firmware upgrade tool for ATMEL Wireless Cards.

%description fucd -l pl.UTF-8
Narzędzie do aktualizacji wewnętrznego oprogramowania bezprzewodowych
kart ATMELa.

%prep
%setup -q -n %{name}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1

ln -sf Makefile.kernelv2.6 Makefile

%build
%if %{with kernel}
# kernel module(s)
rm -rf built
mkdir -p built/{nondist,smp,up}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d o/include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers

%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} pcmcia buildonly=release \
		KERNEL_VERSION=%{__kernel_ver} \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} usb buildonly=release \
		KERNEL_VERSION=%{__kernel_ver} \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	mv -f objs/*/release/*.ko built/$cfg
done
%endif

%if %{with userspace}
%{__make} winter \
	OPT="%{rpmcflags}" \
	WXCONFIG="wx-gtk2-%{?with_unicode:unicode}%{!?with_unicode:ansi}-config"

%{__make} lvnet \
	OPT="%{rpmcflags} %{rpmldflags}" \
	INCDIR=%{_includedir} \

%{__make} -C src/apps/fw-upgrade atmelup \
	CCC="%{__cc}" \
	CCFLAGS="%{rpmcflags}" \
	WXCONFIG="wx-gtk2-%{?with_unicode:unicode}%{!?with_unicode:ansi}-config"

%{__make} -C src/apps/fw-upgrade fucd \
	OPT="%{rpmcflags}" \
	WXCONFIG="wx-gtk2-%{?with_unicode:unicode}%{!?with_unicode:ansi}-config"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}

%if %{with kernel}
cd built
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/{net/pcmcia,usb/net}
install %{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/pcm* \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/pcmcia
install %{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/usb* \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net
%if %{with smp} && %{with dist_kernel}
install smp/pcm* \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/pcmcia
install smp/usb* \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/net
%endif
cd -
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
cp scripts/atmel.conf $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
cp scripts/fastvnet.sh $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/vnetrc
%endif

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install man/lvnet.1 $RPM_BUILD_ROOT%{_mandir}/man1
install src/apps/fw-upgrade/atmelup $RPM_BUILD_ROOT%{_sbindir}
install src/apps/cmd_line/lvnet $RPM_BUILD_ROOT%{_sbindir}
install objs/winter $RPM_BUILD_ROOT%{_sbindir}
install src/apps/fw-upgrade/fucd $RPM_BUILD_ROOT%{_sbindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-net-atmelwlandriver
%depmod %{_kernel_ver}

%postun -n kernel-net-atmelwlandriver
%depmod %{_kernel_ver}

%post -n kernel-smp-net-atmelwlandriver
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-atmelwlandriver
%depmod %{_kernel_ver}smp

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel-net-atmelwlandriver
%defattr(644,root,root,755)
%doc CHANGES README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/atmel.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vnetrc
%attr(755,root,root) %{_sbindir}/fastvnet.sh
/lib/modules/%{_kernel_ver}/kernel/drivers/net/pcmcia/*.ko*
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/*.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-atmelwlandriver
%defattr(644,root,root,755)
%doc CHANGES README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/atmel.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vnetrc
%attr(755,root,root) %{_sbindir}/fastvnet.sh
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/pcmcia/*.ko*
/lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/net/*.ko*
%endif
%endif

%if %{with userspace}
%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/atmelup
%attr(755,root,root) %{_sbindir}/lvnet
%{_mandir}/man1/*

%files winter
%defattr(644,root,root,755)
%doc src/apps/winter/README.linux
%attr(755,root,root) %{_sbindir}/winter

%files fucd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/fucd
%endif
