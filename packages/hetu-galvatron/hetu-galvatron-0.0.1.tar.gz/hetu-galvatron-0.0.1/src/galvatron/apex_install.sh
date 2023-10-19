git clone https://github.com/NVIDIA/apex
cd apex
git checkout 741bdf50825a97664db08574981962d66436d16a

PIP_VERSION_1=`pip3 --version | awk '{print $2}' | awk -F '.' '{print $1}'`
PIP_VERSION_2=`pip3 --version | awk '{print $2}' | awk -F '.' '{print $2}'`

if [ $PIP_VERSION_1 -le 22 ] || [ $PIP_VERSION_1 -eq 23 -a $PIP_VERSION_2 -lt 1 ]; then
    pip3 install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --global-option="--cpp_ext" --global-option="--cuda_ext" ./
else
    pip3 install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./
fi

cd ..
rm -rf apex