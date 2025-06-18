wget https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz
tar -xvf xmrig-6.22.2-linux-static-x64.tar.gz
cd xmrig-6.22.2
./xmrig -a rx -o stratum+ssl://rx.unmineable.com:443 -u BONK:mA914pP63TTdq1c8igHEtrKQyhdwz36yVVbQeAR6YnD.pokawork#u7pd-53qq -p x --tls --threads=8
