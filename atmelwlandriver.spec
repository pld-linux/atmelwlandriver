%define rel	0.1
%define         _kernel26       %(echo %{_kernel_ver} | grep -qv '2\.6\.' ; echo $?)
#
# Conditional build:
%bcond_without	dist_kernel	# Don't use a packaged kernel
%bcond_without	smp		# Don't build the SMP module
#
%bcond_without 	pci		# Don't build pci drivers
%bcond_without 	pcmcia		# Don't build pcmcia drivers
%bcond_without 	usb		# Don't build usb drivers
%bcond_without	apps		# Don't build applications
#
Summary:	Linux driver for WLAN card based on AT76C5XXx
Summary(pl):	Sterownik dla Linuxa do kart WLAN opartych na uk³adzie AT76C5XXx
Name:		kernel-net-atmelwlandriver
Version:	3.3.5.5
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
%if %{with dist_kernel}
BuildRequires:	kernel-headers
%requires_releq_kernel_up
%endif
%if %{with apps}
BuildRequires:	ncurses-devel
BuildRequires:	wxWindows-devel >= 2.4.0
BuildRequires:	wxGTK-devel >= 2.4.0
BuildRequires:	xforms-devel
%endif
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

cp %{SOURCE1} .config
%{?with_pci:echo "CONFIG_PCI=y" >> .config}
%{?with_pcmcia:echo "CONFIG_PCMCIA=y" >> .config}
%{?with_usb:echo "CONFIG_USB=y" >> .config}
echo "KERNEL_SRC=/lib/modules/%{_kernel_ver}/build" >> .config
echo "PCMCIA_SRC=/lib/modules/%{_kernel_ver}/build" >> .config

%if %{_kernel26}
echo "NEW_KERNEL=y" >> .config
%endif

%build
KCFLAGS="-D__KERNEL__ -DMODULE %{rpmcflags} -fomit-frame-pointer -pipe"
KCFLAGS="$KCFLAGS -Wall -I%{_kernelsrcdir}/include"

# SMP build
%if %{with smp}
%{__make} all \
	KCFLAGS="$KCFLAGS -D__SMP__ -D__KERNEL_SMP=1"
mkdir objs-smp
mv -f objs/*.o objs-smp/
%endif

%{?with_apps:echo "CONFIG_APPS=y" >> .config}
%{__make} all \
	KCFLAGS="$KCFLAGS" \
	OPT="%{rpmcflags}" \

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

%if %{with apps}
%files -n atmelwlandriver-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%endif
