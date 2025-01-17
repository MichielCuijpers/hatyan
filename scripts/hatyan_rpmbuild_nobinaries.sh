# usage: in PuTTY from current folder: './hatyan_rpmbuild_nobinaries.sh'
# do not forget to chmod +x ./hatyan_rpmbuild_nobinaries.sh
#
# if it doesn't work (permission issue), try:
#    dos2unix hatyan_rpmbuild.sh
#    ./hatyan_rpmbuild_nobinaries.sh
#
# rpmbuild requires (sudo yum -y install): centos-release-scl-rh, rh-python36-python,  rh-python36-python-virtualenv, rpm-build
#!/bin/bash
set -e

versiontag=put_versiontag_here #the versiontag is also internally stored in the specfile, this should be aligned with this one. Possible are main, branches, tags like v2.3.0

#define and delete resulting directories first to start clean (for h6)
RPMTOPDIR=$HOME/rpmbuild
HATYANEXEC=~/hatyan_fromhome.sh
rm -rf ${RPMTOPDIR}
rm -f ${HATYANEXEC}

# download spec from source, setup conda env with specific python version to use in rpmbuild, rpmbuild from spec, deactivate conda env
rm -rf hatyan_github
git clone -b ${versiontag} https://github.com/Deltares/hatyan.git hatyan_github 
module load anaconda3
conda create -n hatyan_setup_venv python=3.6.12 -y 
conda activate hatyan_setup_venv
rpmbuild -v -bi hatyan_github/scripts/hatyan_python-latest_python3.spec --define "VERSIONTAG ${versiontag}"
conda deactivate
module unload anaconda3

HATYANENVDIR=$(find $HOME/rpmbuild/BUILDROOT/hatyan_python-*/opt/hatyan_python/hatyan_env | head -n 1)
cp hatyan_github/scripts/hatyan.sh $HATYANEXEC
chmod +x $HATYANEXEC
#replace env location in activate script and hatyanexec (double quote to expand variable)
sed -i "s#/opt/hatyan_python/hatyan_env#${HATYANENVDIR}#g" $HATYANENVDIR/bin/activate
sed -i "s#/opt/hatyan_python/hatyan_env#${HATYANENVDIR}#g" $HATYANEXEC

echo "If all went well, there is now a hatyan_env copied from the RPM BUILDROOT in $HATYANENVDIR and $HATYANEXEC can be used to execute hatyan:"
echo "EXAMPLE: ./hatyan_fromhome.sh hatyan_github/tests/configfiles/predictie_2019_19Ycomp4Ydia_VLISSGN_interactive.py"
