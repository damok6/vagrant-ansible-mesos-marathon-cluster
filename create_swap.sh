dd if=/dev/zero of=/var/swap2 bs=1024 count=8388608
chown root:root /var/swap2
chmod 0600 /var/swap2
mkswap /var/swap2
swapon /var/swap2