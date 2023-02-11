python --version
apt-get update
apt-get install vim
pip install -r requirements.txt
export PYTHONPATH=.
echo "You can add  'export PYTHONPATH=.:$PYTHONPATH' to ~/.bashrc"
source ~/.bashrc
$PYTHONPATH
python --version