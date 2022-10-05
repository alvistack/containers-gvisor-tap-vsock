%global debug_package %{nil}

Name: podman-gvproxy
Epoch: 100
Version: 0.3.0
Release: 1%{?dist}
Summary: Go replacement for libslirp and VPNKit
License: Apache-2.0
URL: https://github.com/containers/gvisor-tap-vsock/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.19
BuildRequires: glibc-static
Requires: podman

%description
A replacement for libslirp and VPNKit, written in pure Go. It is based
on the network stack of gVisor. Compared to libslirp, gvisor-tap-vsock
brings a configurable DNS server and dynamic port forwarding.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
        go build \
            -mod vendor -buildmode pie -v \
            -ldflags "-s -w" \
            -o ./bin/gvproxy ./cmd/gvproxy

%install
install -Dpm755 -d %{buildroot}%{_libexecdir}/podman
install -Dpm755 -t %{buildroot}%{_libexecdir}/podman bin/gvproxy

%files
%license LICENSE
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/*

%changelog
