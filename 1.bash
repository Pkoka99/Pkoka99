mkdir -p ~/local/chrome && cd ~/local/chrome
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
ar x google-chrome-stable_current_amd64.deb data.tar.xz
tar -xf data.tar.xz
mv opt/google/chrome/* ./
rm -rf opt data.tar.xz google-chrome-stable_current_amd64.deb
chmod +x google-chrome
echo 'export PATH=$HOME/local/chrome:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$HOME/local/chrome:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
pip install selenium
pip install --upgrade pip
wget https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.103/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver
mv chromedriver-linux64/chromedriver /usr/local/bin/
wget https://raw.githubusercontent.com/Pkoka99/Pkoka99/refs/heads/main/vv.py
python vv.py
