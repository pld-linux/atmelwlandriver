# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP modules
%bcond_without	userspace	# don't build userspace applications
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	Linux driver for WLAN card based on AT76C5XXx
Summary(pl):	Sterownik dla Linuxa do kart WLAN opartych na uk³adzie AT76C5XXx
Name:		kernel-net-atmelwlandriver
Version:	3.3.5.5
%define		rel	0.1
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/sourceforge/atmelwlandriver/atmelwlandriver-%{version}.tar.bz2
# Source0-md5:	4248ff3f0a0d7d3f83d02cb540bff6f9
Source1:	atmelwlandriver.config
# Patch0:		atmelwlandriver-makefile.patch
Patch1:		atmelwlandriver-etc.patch
URL:		http://atmelwlandriver.sourceforge.net
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	%{kgcc_package}
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel-module-build
%endif
%if %{with userspace}
BuildRequires:	ncurses-devel
BuildRequires:	wxWindows-devel >= 2.4.0
BuildRequires:	wxGTK-devel >= 2.4.0
BuildRequires:	xforms-devel
%endif
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires:	wireless-tools
Requires(post,postun):	/sbin/depmod
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
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires:	wireless-tools
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-atmelwlandriver
This is driver for WLAN card based on ATMEL AT76C5XXx devices for
Linux.

%description -n kernel-smp-net-atmelwlandriver -l pl
Sterownik dla Linuksa do kart sieci bezprzewodowych opartych o uk³ady
ATMELA AT76C5XXx.

%package -n atmelwlandriver-tools
Summary:	Tools for monitoring ATMEL Wireless Card
Summary(pl):	Narzêdzia do monitorowania bezprzewodowych kart ATMEL
Release:	%{rel}
Group:		Networking/Utilities
Requires:	%{name} = %{version}

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
#%%patch0 -p1
%patch1 -p1

%build
cp -f Makefile{.kernelv2.6,}

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
    touch include/config/MARKER
    %{__make} -C %{_kernelsrcdir} clean \
	RCS_FIND_IGNORE="-name '*.ko' -o" \
	M=$PWD O=$PWD \
	%{?with_verbose:V=1}
    %{__make} pcmcia buildonly=release \
	M=$PWD O=$PWD \
	%{?with_verbose:V=1}
    %{__make} usb buildonly=release \
	M=$PWD O=$PWD \
	%{?with_verbose:V=1}
    mv -f objs/*/release/*.ko built/$cfg
done
%endif

%if %{with userspace}
#        make lvnet              - compile lvnet utility
#        make winter             - compile winter utility - ( CAUTION : MUST have wxwindows installed )
#        make install            - install modules and programs

#%{?with_apps:echo "CONFIG_APPS=y" >> .config}
#%{__make} all \
#	KCFLAGS="$KCFLAGS" \
#	OPT="%{rpmcflags}" \
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/{net,usb,pcmcia}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/{net,usb,pcmcia}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/pcmcia,%{_mandir}/man1}

mv -f scripts/.vnetrc $RPM_BUILD_ROOT%{_sysconfdir}/vnetrc
cp scripts/atmel.conf $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_prefix} \
        MODDIR=$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver} \
	MAN_PATH=$RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post
for i in /lib/modules/%{_kernel_ver}/kernel/drivers/usb/usbvnet* ; do
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
for i in /lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/usbvnet* ; do
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

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fastvnet.sh
%doc CHANGES README
/lib/modules/%{_kernel_ver}/*
%{_sysconfdir}/pcmcia/atmel.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vnetrc

%if %{with smp}
%files -n kernel-smp-net-atmelwlandriver
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fastvnet.sh
%doc CHANGES README
/lib/modules/%{_kernel_ver}smp/*
%{_sysconfdir}/pcmcia/atmel.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vnetrc
%endif

%if %{with userspace}
%files -n atmelwlandriver-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%endif
