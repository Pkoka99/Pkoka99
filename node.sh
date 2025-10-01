!apt update -y
!apt install curl -y

# Install Node.js versi 20 (LTS)
!curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
!apt-get install -y nodejs

# Cek versi
!node -v
!npm -v

# Buat folder kerja
!mkdir -p /content/wa-bot
%cd /content/wa-bot

# Init project & install Baileys
!npm init -y
!npm install @whiskeysockets/baileys
