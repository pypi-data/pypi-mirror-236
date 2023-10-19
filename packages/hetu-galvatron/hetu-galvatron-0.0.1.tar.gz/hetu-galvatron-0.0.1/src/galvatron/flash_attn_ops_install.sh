git clone --recursive https://github.com/Dao-AILab/flash-attention.git
cd flash-attention/csrc/fused_dense_lib
pip3 install .
cd ../layer_norm
pip3 install .
cd ../rotary
pip3 install .
cd ../xentropy
pip3 install .
cd ../..
rm -rf flash-attention