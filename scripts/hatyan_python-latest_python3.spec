#rpmbuild requires (sudo yum -y install): rpm-build and python3 (or anaconda or anything else), the python version you use will also be the version that is in the hatyan_env
#start rpmbuild like this:
#rpmbuild -v -bb ~/hatyan_github/scripts/hatyan_python-latest_python3.spec --define "VERSIONTAG main"

Name:        hatyan_python
Version:     2.3.7
Release:     1
BuildArch:   x86_64
URL:         https://github.com/Deltares/hatyan
AutoReq:     no
Summary:     Python version of the hatyan RWS program for tidal analysis and prediction, packed with Python venv with necessary Python libraries
License:     LGPL
Provides:    hatyan_python
Requires:    glibc >= 2.12 coreutils expect stix-fonts fontconfig freetype libstdc++ jasper libXcursor libXrender xorg-x11-xauth mesa-libGL mesa-libEGL libXi

%description
%{summary}

#prevent build_id links (/usr/lib/.build-id/*) on github platform
%define _build_id_links none
#define versiontag (defaults to main if not passed as rpmbuild define flag, there should be a github tag created with that name, e.g. v2.2.86)
%{!?VERSIONTAG: %define VERSIONTAG main}

#install the code into directories on the build machine
%install
#clear build folder, clone specific hatyan versiontag
rm -rf %{_topdir}/BUILD/*
git clone -b %{VERSIONTAG} https://github.com/Deltares/hatyan.git %{_topdir}/BUILD/hatyan_github #the BUILD folder is where it automatically clones to
#create sh script for running hatyan on linux in one command
mkdir -p $RPM_BUILD_ROOT/usr/bin
EXECFILE=$RPM_BUILD_ROOT/usr/bin/hatyan
cp %{_topdir}/BUILD/hatyan_github/scripts/hatyan.sh $EXECFILE
chmod +x $EXECFILE
#create folder for hatyan_env and potentially other folders/files
mkdir -p $RPM_BUILD_ROOT/opt/hatyan_python
cp -r %{_topdir}/BUILD/hatyan_github/doc $RPM_BUILD_ROOT/opt/hatyan_python
cp -r %{_topdir}/BUILD/hatyan_github/tests $RPM_BUILD_ROOT/opt/hatyan_python
#cp -r %{_topdir}/BUILD/hatyan_github/hatyan $RPM_BUILD_ROOT/opt/hatyan_python
# create python3 venv hatyan_env
python3 -m venv $RPM_BUILD_ROOT/opt/hatyan_python/hatyan_env
. $RPM_BUILD_ROOT/opt/hatyan_python/hatyan_env/bin/activate #Was (but does not work on github): source $RPM_BUILD_ROOT/opt/hatyan_python/hatyan_env/bin/activate
echo "The rpmbuildversion is:"
rpmbuild --version
echo "The python version used should be something like 3.6.8 or 3.6.12 with the current fixed libraries. This is necessary since CentOS6 contained glibc=2.12 and not higher, newer machine has glibc=2.17. Python 3.8 requires glibc>2.24 or so, but might not be available on destination machine. Github has setup-python action for specific python version. The python version used for venv is:"
python --version
# upgrade pip and setuptools to make sure all dependencies are handled well
python -m pip install --upgrade pip setuptools
#install hatyan package from source, also install old library versions to make it work on CentOS (prevent errors related to Qt and others)
python -m pip install %{_topdir}/BUILD/hatyan_github -r %{_topdir}/BUILD/hatyan_github/requirements_dev.txt
#install pyqt5==5.7.1 to avoid "Failed to import any qt binding" error. The fixed version is necessary since CentOS/RHEL6 have glibc 2.12 and higher pyqt5 versions require glibc>=2.14
python -m pip install pyqt5==5.7.1
#remove BUILDROOT prefix in bin files like activate to make it work after installation (pip/python/activate can find each other):
sed -i "s#/.*/rpmbuild/BUILDROOT/.*x86_64##g" $RPM_BUILD_ROOT/opt/hatyan_python/hatyan_env/bin/*
deactivate #deactivate venv hatyan_env
exit 0 #to prevent compiling

# gathers list of files and packs them to the RPM
%files
/opt/hatyan_python
/usr/bin/hatyan
