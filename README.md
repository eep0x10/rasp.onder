# Projeto

O Objetivo desse projeto visa realizar de forma "automatizada" e "stealth" o bypass da camada de proteção 802.1x PNAC (Filtro de MAC) e iniciar quaisquer scripts/exploits/ferramentas ao ingressar dentro da rede alvo utilizando ferramentas como RaspberryPI3 e um Switch, ambos de fácil acesso para compra.

No cenário proposto, um atacante utilizará a ferramenta + scripts contruidos para realizar o ataque, ao obter acesso local aos cabos de rede referente a rede alvo, basta plugar um computador de um colaborador para clonar seu MAC, e depois o mesmo ingresará na rede, assim rodando as automações, em sequência é recomendável que a caixa seja escondida equanto conectada ao cabo de rede, para que permaneça na rede realizando os ataques.

Para o caso atual, a ferramenta a ser ativada sera o "Responder", o qual terá função de coletar Hashes de usuários na rede e exfiltra-los para um servidor externo (C2).

# Equipamentos

* Raspberry PI (recomendável PI3 1GB RAM)
* 1 Cabo microUSB/USB-C (Depende do RaspberryPI)
* Tela Touch RaspberryPI (Recomendável/Não Obrigatório)
* Switch de rede
* Conversor de energia do Switch para USB
* 2 Cabos de Rede RJ45 (Pequenos)
* 1 PowerBank (Pequeno)
* Teclado Bluethooth (Recomendável/Não Obrigatório)
* Conversor LAN - USB
* Fita Dupla-Face + Caixa (20cm x 15cm +-)



