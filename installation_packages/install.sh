#!/bin/bash
# MotifCluster Environment Installation Script
# Creates a conda/mamba environment and installs all required packages
# Usage: ./install.sh [env_name]
# Example: ./install.sh motifcluster_test
#          ./install.sh # will use motifcluster by default

set -euo pipefail

ENV_NAME="${1:-motifcluster}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo "MotifCluster Environment Setup"
echo "========================================"
echo ""

# Check for conda
if ! command -v conda >/dev/null 2>&1; then
  echo "Error: conda not found in PATH. Install Miniconda/Anaconda first."
  exit 1
fi

# Initialize shell functions if needed
if ! type conda >/dev/null 2>&1; then
  conda init bash >/dev/null 2>&1 || true
  source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true
fi

# Try to get mamba; fallback to conda
PKG=conda
if ! command -v mamba >/dev/null 2>&1; then
  echo "[info] mamba not found; trying to install in base..."
  conda install -n base -c conda-forge -y mamba || true
  hash -r
fi
if command -v mamba >/dev/null 2>&1; then
  PKG=mamba
  echo "[info] using mamba (faster installation)"
else
  echo "[info] using conda"
fi

# # Check if environment already exists
# if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
#   echo "[warn] environment '$ENV_NAME' already exists. Deleting it first..."
#   conda env remove -n "$ENV_NAME" -y
# fi
# Check if environment already exists
if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  echo "[warn] environment '$ENV_NAME' already exists. Deleting it first..."
  exit 1
fi

echo "[info] creating environment: $ENV_NAME (python=3.9)"
$PKG create -n "$ENV_NAME" -y python=3.9

echo "[info] activating $ENV_NAME"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME" || { echo "Error: failed to activate $ENV_NAME"; exit 1; }
export PATH="$CONDA_PREFIX/bin:$PATH"

# Install conda packages
echo ""
echo "[info] installing conda packages from conda-forge and bioconda..."
$PKG install -c conda-forge -c bioconda -y \
    bedtools=2.30.0 \
    biopython=1.78 \
    matplotlib-base=3.7.0 \
    numpy=1.23.4 \
    pandas=1.4.1 \
    pybedtools=0.9.0 \
    pysam=0.18.0 \
    pyranges=0.0.120 \
    cython=0.29.32 \
    lxml=4.8.0 \
    natsort=7.1.1 \
    ncls=0.0.64 \
    pyrle=0.0.34 \
    fuc=0.10.0

# Install PyTorch with CUDA support (if GPU available)
echo ""
echo "[info] installing PyTorch with CUDA 11.3..."
$PKG install -c pytorch -y \
    pytorch \
    cudatoolkit=11.3 \
    torchaudio=0.11.0

# Install pip packages
echo ""
echo "[info] installing pip packages..."
pip install wget==3.2 shapely==1.8.5.post1 colour==0.1.5 \
    scikit-learn==1.0.2 threadpoolctl==3.1.0 termcolor==2.1.1 \
    pyparsing==3.0.7 fonttools==4.29.1 got10k==0.1.3 \
    kiwisolver==1.3.2 pillow==9.0.1 joblib==1.1.0 \
    scipy==1.8.0 matplotlib==3.5.1 fire==0.4.0 \
    packaging==21.3

echo ""
echo "========================================"
echo "[done] Installation Complete!"
echo "========================================"
echo "Environment '$ENV_NAME' ready at: $CONDA_PREFIX"
echo ""
echo "To activate the environment, run:"
echo "  conda activate $ENV_NAME"
echo ""
echo "To deactivate, run:"
echo "  conda deactivate"
echo ""
conda deactivate
