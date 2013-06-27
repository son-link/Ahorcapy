echo 'Installing Ahorcapy'

install -m755 ahorcapy.py /usr/bin/ahorcapy
mkdir -p /usr/share/ahorcapy
install -m644 COPYING /usr/share/ahorcapy
cp lists -r /usr/share/ahorcapy/

sed -i "s/COPYING/\/usr\/share\/ahorcapy\/COPYING/g" /usr/bin/ahorcapy
sed -i "s/words.txt/\/usr\/share\/ahorcapy\/words.txt/g" /usr/bin/ahorcapy
sed -i "s/lists\//\/usr\/share\/ahorcapy\/lists\//g" $pkgdir/usr/bin/ahorcapy

cp lang/* -r /usr/share/locale

echo 'Install complete'
