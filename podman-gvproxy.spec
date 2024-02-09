# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: podman-gvproxy
Epoch: 100
Version: 0.7.1
Release: 1%{?dist}
Summary: Go replacement for libslirp and VPNKit
License: Apache-2.0
URL: https://github.com/containers/gvisor-tap-vsock/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.22
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