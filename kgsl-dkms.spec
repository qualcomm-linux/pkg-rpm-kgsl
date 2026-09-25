Name:           kgsl-dkms
Version:        1.0.16
Release:        1%{?dist}
Summary:        Qualcomm KGSL GPU kernel module (DKMS)
License:        GPL-2.0-only
URL:            https://github.com/qualcomm-linux/kgsl
Source0:        https://github.com/qualcomm-linux/kgsl/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        kgsl-dkms.dkms
Source2:        kgsl-dkms.conf
Source3:        50-kgsl.rules

%global modprobedir %{_prefix}/lib/modprobe.d
%global udevrulesdir %{_prefix}/lib/udev/rules.d

BuildArch:      noarch
BuildRequires:  cpio
Requires:       dkms
# DKMS uses the matching kernel-devel build tree to compile the module.
# The installation repository must provide kernel-devel for the target kernel.
Requires:       kernel-devel

%description
Kernel Graphics Support Layer (KGSL) driver for the Adreno family of Qualcomm
GPUs. It provides GPU memory management, command submission, power management,
and userspace debug and profiling interfaces for hardware-accelerated OpenGL,
compute, and Vulkan on Qualcomm Snapdragon platforms.

This package contains the source code for the msm_kgsl kernel module and builds
it through DKMS for supported installed kernels.

%prep
%autosetup -n kgsl-%{version}

%build
# The upstream Makefile builds against a selected kernel tree. DKMS invokes it
# later with KERNEL_SRC set to the target kernel build directory.
:

%install
install -d %{buildroot}%{_usrsrc}/kgsl-%{version}

# Mirrors debian/rules: stage the upstream source while excluding VCS metadata
# and the upstream top-level license/readme files.
find . -mindepth 1 \
    \( -path './.git' -o -path './.github' -o -path './.pc' \) -prune -o \
    ! -path './.gitignore' \
    ! -path './LICENSE.txt' \
    ! -path './README.md' \
    -print0 | cpio --null -pdm %{buildroot}%{_usrsrc}/kgsl-%{version}

# dh_dkms installs this template as dkms.conf and replaces #MODULE_VERSION#.
install -Dm0644 %{SOURCE1} \
    %{buildroot}%{_usrsrc}/kgsl-%{version}/dkms.conf
sed -i 's/#MODULE_VERSION#/%{version}/g' \
    %{buildroot}%{_usrsrc}/kgsl-%{version}/dkms.conf

install -Dm0644 %{SOURCE2} \
    %{buildroot}%{modprobedir}/kgsl-dkms.conf
install -Dm0644 %{SOURCE3} \
    %{buildroot}%{udevrulesdir}/50-kgsl.rules

# Debian's initramfs-tools hook has no portable RPM equivalent. DKMS and the
# target distribution's kernel/initramfs integration are responsible for it.

%check
:

%post
%{_sbindir}/dkms add -m kgsl -v %{version} || :
%{_sbindir}/dkms autoinstall -m kgsl -v %{version} || :

%preun
if [ "$1" -eq 0 ]; then
    %{_sbindir}/dkms remove -m kgsl -v %{version} --all || :
fi

%files
%license LICENSE.txt
%{_usrsrc}/kgsl-%{version}
%{modprobedir}/kgsl-dkms.conf
%{udevrulesdir}/50-kgsl.rules

%changelog
* Fri Sep 25 2026 Maintainers.pkg-rpm-kgsl <Maintainers.pkg-rpm-kgsl@qualcomm.com> - 1.0.16-1
- Update to upstream 1.0.16.

* Tue Sep 01 2026 Maintainers.pkg-rpm-kgsl <Maintainers.pkg-rpm-kgsl@qualcomm.com> - 1.0.13-1
- Update to upstream 1.0.13.
