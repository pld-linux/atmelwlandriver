# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP modules
%bcond_without	userspace	# don't build userspace applications
%bcond_with	verbose		# verbose build (V=1)
#
# TODO:
# 	- X11 tools
#
Summary:	Linux driver for WLAN card based on AT76C5XXx
Summary(pl):	Sterownik dla Linuxa do kart WLAN opartych na uk³adzie AT76C5XXx
Name:		kernel-net-atmelwlandriver
Version:	3.3.5.6
%define		_rel	0.2
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/sourceforge/atmelwlandriver/atmelwlandriver-%{version}.tar.bz2
# Source0-md5:	dd9a11d175ba0fbb62cf7fec5426f5de
Source1:	atmelwlandriver.config
Patch0:		atmelwlandriver-makefile.patch
Patch1:		atmelwlandriver-etc.patch
Patch2:		atmelwlandriver-fpmath.patch
Patch3:		atmelwlandriver-delay.patch
Patch4:		atmelwlandriver-usb_defctrl.patch
URL:		http://atmelwlandriver.sourceforge.net
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRequires:	%{kgcc_package}
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel-module-build >= 2.6.7
BuildRequires:	kernel-source
%endif
%if %{with userspace}
BuildRequires:	ncurses-devel
#BuildRequires:	wxWindows-devel >= 2.4.0
#BuildRequires:	wxGTK-devel >= 2.4.0
#BuildRequires:	xforms-devel
%endif
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires:	wireless-tools
Requires(post,postun):	/sbin/depmod
Provides:	kernel-net(atmelwlandriver) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on ATMEL AT76C5XXx devices for
Linux.

%description -l pl
Sterownik dla Linuksa do kart sieci bezprzewodowych opartych o uk³ady
ATMELA AT76C5XXx.

%package -n kernel-smp-net-atmelwlandriver
Summary:	Linux driver for WLAN card based on AT76C5XXx
Summary(pl):	Sterownik dla Linuxa do kart WLAN na uk³adzie AT76C5XXx
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires:	wireless-tools
Requires(post,postun):	/sbin/depmod
Provides:	kernel-net(atmelwlandriver) = %{version}

%description -n kernel-smp-net-atmelwlandriver
This is driver for WLAN card based on ATMEL AT76C5XXx devices for
Linux.

%description -n kernel-smp-net-atmelwlandriver -l pl
Sterownik dla Linuksa do kart sieci bezprzewodowych opartych o uk³ady
ATMELA AT76C5XXx.

%package -n atmelwlandriver-tools
Summary:	Tools for monitoring ATMEL Wireless Card
Summary(pl):	Narzêdzia do monitorowania bezprzewodowych kart ATMEL
Release:	%{_rel}
Group:		Networking/Utilities
Requires:	kernel-net(atmelwlandriver) = %{version}

%description -n atmelwlandriver-tools
Monitoring tools for the ATMEL Wireless Card adapters. When the pcmcia
module pcmf502*, the pci module pcifvnet, or the usb module usbvnet*
is loaded the lvnet, xvnet, winter application can monitor the
device's statistics or change it's runtime parameters.

%description -n atmelwlandriver-tools -l pl
Narzêdzia monitourj±ce dla adapterów kart sieci bezprzewodowych ATMEL.
Kiedy modu³ pcmcia pcmf502*, modu³ pci pcifvnet, albo modu³ usb
usbvnet* jest za³adowany to aplikacja lvnet, xvnet, winter mo¿e
monitorowaæ dane statystyczne urz±dzenia albo zmieniæ parametry jego
pracy.

%prep
%setup -q -n atmelwlandriver
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
#        make lvnet              - compile lvnet utility
#        make winter             - compile winter utility - ( CAUTION : MUST have wxwindows installed )
#        make install            - install modules and programs

%{__make} lvnet INC="%{_includedir}/ncurses -I../../includes"

#%{?with_apps:echo "CONFIG_APPS=y" >> .config}
#%{__make} all \
#	KCFLAGS="$KCFLAGS" \
#	OPT="%{rpmcflags}" \
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
%endif

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
#mv -f scripts/.vnetrc $RPM_BUILD_ROOT%{_sysconfdir}/vnetrc
install man/lvnet.1 $RPM_BUILD_ROOT%{_mandir}/man1
install src/apps/cmd_line/lvnet $RPM_BUILD_ROOT%{_sbindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
for i in /lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/usbvnet* ; do
    cuted_i=$(basename $i|cut -d. -f1)
    if  [ -f $i ]; then
	if ( grep $cuted_i /etc/modules.conf >/dev/null ); then
	    echo "NOP" >/dev/null; else
		echo "#post-install $cuted_i /bin/fastvnet.sh">> /etc/modules.conf;
	fi
    fi
done
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post -n kernel-smp-net-atmelwlandriver
for i in /lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/net/usbvnet* ; do
    cuted_i=$(basename $i|cut -d. -f1)
    if  [ -f $i ]; then
	if ( grep $cuted_i /etc/modules.conf >/dev/null ); then
	    echo "NOP" >/dev/null; else
	    echo "#post-install $cuted_i /bin/fastvnet.sh">> /etc/modules.conf;
	fi
    fi
done
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-atmelwlandriver
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files
%defattr(644,root,root,755)
%doc CHANGES README
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/atmel.conf
#%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vnetrc
%attr(755,root,root) %{_sbindir}/fastvnet.sh
/lib/modules/%{_kernel_ver}/kernel/drivers/net/pcmcia/*.ko*
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/net/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-atmelwlandriver
%defattr(644,root,root,755)
%doc CHANGES README
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/atmel.conf
#%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vnetrc
%attr(755,root,root) %{_sbindir}/fastvnet.sh
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/pcmcia/*.ko*
/lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/net/*.ko*
%endif
%endif

%if %{with userspace}
%files -n atmelwlandriver-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lvnet
%{_mandir}/man1/*
%endif
