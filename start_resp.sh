# Reset MAC Address Random
#sudo ifconfig eth1 hw ether $(ethtool -P eth1 | awk '{print $3}') 1>&-

while true;do
echo "[+] Capturando MAC Address, aguarde 10 segundos..."

echo "" > /tmp/captured_mac.txt

sudo tshark -i eth1 -Y "_ws.col.protocol matches \"IGMPv3\"" -T fields -e eth.src -a duration:10 2>&- | sort -u > /tmp/captured_mac.txt
echo "64:1c:67:e6:d8:a0" > /tmp/captured_mac.txt #HARCODED
# Caminho do arquivo de onde ler o valor
arquivo="/tmp/captured_mac.txt"
valor=$(cat "$arquivo" | tr -d '[:space:]')
# Executa o comando macchanger com o valor lido do arquivo
sudo macchanger -m "$valor" eth1 2>&- # Substitua "eth1" pela interface de rede desejada

cd /usr/share/responder
sudo python3 automation.py
done
