#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP modules
%bcond_without	userspace	# don't build userspace applications
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

Summary:	Linux driver for WLAN card based on AT76C5XXx
Summary(pl):	Sterownik dla Linuksa do kart WLAN opartych na uk�adach AT76C5XXx
Name:		atmelwlandriver
Version:	3.4.1.1
%define		_rel	0.1
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
#Patch2:		%{name}-fpmath.patch
#Patch3:		%{name}-delay.patch
#Patch4:		%{name}-usb_defctrl.patch
URL:		http://atmelwlandriver.sourceforge.net/
%if %{with kernel}
%if %{with dist_kernel}
BuildRequires:	kernel-module-build >= 2.6.11
BuildRequires:	kernel-source >= 2.6.11
%endif
BuildRequires:	rpmbuild(macros) >= 1.217
%endif
%if %{with userspace}
BuildRequires:	libusb-devel
BuildRequires:	ncurses-devel
BuildRequires:	ncurses-ext-devel
BuildRequires:	wxGTK2-devel >= 2.4.0
BuildRequires:	wxWindows-devel >= 2.4.0
%endif
Requires:	wireless-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on ATMEL AT76C5XXx devices for
Linux.

%description -l pl
Sterownik dla Linuksa do kart sieci bezprzewodowych opartych o uk�ady
ATMELA AT76C5XXx.

%package -n kernel-net-atmelwlandriver
Summary:	Linux driver for WLAN card based on AT76C5XXx
Summary(pl):	Sterownik dla Linuksa do kart WLAN na uk�adach AT76C5XXx
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

%description -n kernel-net-atmelwlandriver -l pl
Sterownik dla Linuksa do kart sieci bezprzewodowych opartych o uk�ady
ATMELA AT76C5XXx.

%package -n kernel-smp-net-atmelwlandriver
Summary:	Linux SMP driver for WLAN card based on AT76C5XXx
Summary(pl):	Sterownik dla Linuksa SMP do kart WLAN na uk�adach AT76C5XXx
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

%description -n kernel-smp-net-atmelwlandriver -l pl
Sterownik dla Linuksa SMP do kart sieci bezprzewodowych opartych o
uk�ady ATMELA AT76C5XXx.

%package tools
Summary:	Command line tools for managing ATMEL Wireless Card
Summary(pl):	Narz�dzia linii polece� do obs�ugi bezprzewodowych kart ATMEL
Release:	%{_rel}
Group:		Networking/Utilities
Requires:	kernel-net(atmelwlandriver) = %{version}

%description tools
Managing tools for the ATMEL Wireless Card adapters. When the PCMCIA
module pcmf502*, the PCI module pcifvnet, or the USB module usbvnet*
is loaded the lvnet application can monitor the device's statistics or
change it's runtime parameters.

%description tools -l pl
Narz�dzia do obs�ugi dla adapter�w kart sieci bezprzewodowych ATMEL.
Kiedy modu� PCMCIA pcmf502*, modu� PCI pcifvnet, albo modu� USB
usbvnet* jest za�adowany to aplikacja lvnet mo�e monitorowa� dane
statystyczne urz�dzenia albo zmieni� parametry jego pracy.

%package winter
Summary:	Graphical tool for monitoring ATMEL Wireless Cards
Summary(pl):	Graficzne narz�dzie do monitorowania bezprzewodowych kart ATMEL
Release:	%{_rel}
Group:		Networking/Utilities
Requires:	kernel-net(atmelwlandriver) = %{version}

%description winter
Winter is an X application, that provides a visual enviroment to
configure and manage ATMEL cards. It's functionality is similar to
that of lvnet, extended by very useful features such as profiles,
localization and support for more than one devices alternatively.

%description winter -l pl
Winter jest aplikacj� dla X, kt�ra dostarcza wizualne �rodowisko
pozwalaj�ce na konfiguracj� kart ATMELa. Jego funkcjonalno�� jest
podobna do tej jak� ma lvnet, dodatkowo rozszerzon� o bardzo przydatne
funkcje takie jak: profile, lokalizacje i wsparcie dla wi�cej ni�
jednego urz�dzenia.

%package fucd
Summary:	Firmware upgrade tool for ATMEL Wireless Cards
Summary(pl):	Narz�dzie aktualizacji bezprzewodowych kart ATMEL
Release:	%{_rel}
Group:		Networking/Utilities
Requires:	kernel-net(atmelwlandriver) = %{version}

%description fucd
Graphical firmware upgrade tool for ATMEL Wireless Cards.

%description fucd -l pl
Narz�dzie do aktualizacji wewn�trznego oprogramowania bezprzewodowych
kart ATMELa.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
ln -sf Makefile.kernelv2.6 Makefile

%if %{with kernel}
# kernel module(s)
rm -rf built
mkdir -p built/{nondist,smp,up}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} pcmcia buildonly=release \
		KERNEL_VERSION=%{__kernel_ver} \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} usb buildonly=release \
		KERNEL_VERSION=%{__kernel_ver} \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}

	mv -f objs/*/release/*.ko built/$cfg
done
%endif

%if %{with userspace}
%{__make} winter \
	OPT="%{rpmcflags}"

%{__make} lvnet \
	OPT="%{rpmcflags} %{rpmldflags}"

%{__make} -C src/apps/fw-upgrade atmelup \
	CCC="%{__cc}" \
	CCFLAGS="%{rpmcflags}"

%{__make} -C src/apps/fw-upgrade fucd \
	OPT="%{rpmcflags}"
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
#for i in /lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/usbvnet* ; do
#	cuted_i=$(basename $i|cut -d. -f1)
#	if [ -f $i ]; then
#		if ( grep $cuted_i /etc/modprobe.conf >/dev/null ); then
#			echo "NOP" >/dev/null;
#		else
#			echo "#post-install $cuted_i /usr/sbin/fastvnet.sh">> /etc/modprobe.conf;
#		fi
#	fi
#done
%depmod %{_kernel_ver}

%postun -n kernel-net-atmelwlandriver
%depmod %{_kernel_ver}

%post -n kernel-smp-net-atmelwlandriver
#for i in /lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/net/usbvnet* ; do
#	cuted_i=$(basename $i|cut -d. -f1)
#	if [ -f $i ]; then
#		if ( grep $cuted_i /etc/modprobe.conf >/dev/null ); then
#			echo "NOP" >/dev/null;
#		else
#			echo "#post-install $cuted_i /usr/sbin/fastvnet.sh">> /etc/modprobe.conf;
#		fi
#	fi
#done
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-atmelwlandriver
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel-net-atmelwlandriver
%defattr(644,root,root,755)
%doc CHANGES README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/atmel.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vnetrc
%attr(755,root,root) %{_sbindir}/fastvnet.sh
/lib/modules/%{_kernel_ver}/kernel/drivers/net/pcmcia/*.ko*
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/*.ko*

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
