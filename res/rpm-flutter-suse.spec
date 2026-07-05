Name:       xdesk
Version:    1.4.6
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://rustdesk.com
Vendor:     xdesk <info@rustdesk.com>
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/xdesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/xdesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/xdesk.service -t "%{buildroot}/usr/share/xdesk/files"
install -Dm 644 $HBB/res/xdesk.desktop -t "%{buildroot}/usr/share/xdesk/files"
install -Dm 644 $HBB/res/xdesk-link.desktop -t "%{buildroot}/usr/share/xdesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/xdesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/xdesk.svg"

%files
/usr/share/xdesk/*
/usr/share/xdesk/files/xdesk.service
/usr/share/icons/hicolor/256x256/apps/xdesk.png
/usr/share/icons/hicolor/scalable/apps/xdesk.svg
/usr/share/xdesk/files/xdesk.desktop
/usr/share/xdesk/files/xdesk-link.desktop

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
cp /usr/share/rustdesk/files/rustdesk-link.desktop /usr/share/applications/
ln -sf /usr/share/rustdesk/rustdesk /usr/bin/rustdesk
systemctl daemon-reload
systemctl enable rustdesk
systemctl start rustdesk
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
    rm /usr/bin/rustdesk || true
    rmdir /usr/lib/rustdesk || true
    rmdir /usr/local/rustdesk || true
    rmdir /usr/share/rustdesk || true
    rm /usr/share/applications/rustdesk.desktop || true
    rm /usr/share/applications/rustdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/rustdesk || true
    rmdir /usr/local/rustdesk || true
  ;;
esac
