Name:       xdesk
Version:    1.4.6
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://rustdesk.com
Vendor:     xdesk <info@rustdesk.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva2 pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/xdesk/
mkdir -p %{buildroot}/usr/share/xdesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/xdesk %{buildroot}/usr/bin/xdesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/xdesk/libsciter-gtk.so
install $HBB/res/xdesk.service %{buildroot}/usr/share/xdesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/xdesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/xdesk.svg
install $HBB/res/xdesk.desktop %{buildroot}/usr/share/xdesk/files/
install $HBB/res/xdesk-link.desktop %{buildroot}/usr/share/xdesk/files/

%files
/usr/bin/xdesk
/usr/share/xdesk/libsciter-gtk.so
/usr/share/xdesk/files/xdesk.service
/usr/share/icons/hicolor/256x256/apps/xdesk.png
/usr/share/icons/hicolor/scalable/apps/xdesk.svg
/usr/share/xdesk/files/xdesk.desktop
/usr/share/xdesk/files/xdesk-link.desktop
/usr/share/xdesk/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop xdesk || true
  ;;
esac

%post
cp /usr/share/xdesk/files/xdesk.service /etc/systemd/system/xdesk.service
cp /usr/share/xdesk/files/xdesk.desktop /usr/share/applications/
cp /usr/share/xdesk/files/xdesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable xdesk
systemctl start xdesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop rustdesk || true
    systemctl disable rustdesk || true
    rm /etc/systemd/system/rustdesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/rustdesk.desktop || true
    rm /usr/share/applications/rustdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
