# Vaatimukset
- Python3
- pip


# Asennusohjeet

1. Luo uusi virtuaaliympäristö opt/OumanHA kansioon:
`sudo python3 -m venv /opt/OumanHA`

2. Kopioi kansioon _OumanHA.py_ ja _requirements.txt_.

4. Siirry kansioon
`cd /opt/OumanHA`
ja aja komento
`source bin/activate`

3. Asenna vaaditut kirjastot:
`pip install -r requirements.txt`

4. Lisää _pi_ käyttäjä sarjaportin käyttäjäryhmään, jos se jo ei ole lisättynä:
`sudo usermod -a -G dialout pi`

5. Liitä Ouman käyttäen usb miniB kaapelia Raspberryyn. Tarkista allaolevalla komennolla minkä portin Ouman sai.
`dmesg -w`

```
cdc_acm 1-1.3:1.0: ttyACM0: USB ACM device
usbcore: registered new interface driver cdc_acm
cdc_acm: USB Abstract Control Model driver for USB modems and ISDN adapters
```

Tässä tapauksessa Ouman sai portin `ttyACM0`.

Muokkaa portti tarvittaessa tiedostoon `/opt/OumanHA/OumanHA.py` kohtaan _read_measurements_.

```
def read_measurements():
    # Open the serial port
    try:
        ser = serial.Serial(
            port='/dev/ttyACM0', 

```

Voit koestaa python ohjelmaa ajamalla komennon virtuaaliympäristössä.
```
(OumanHA) root@raspberrypi-01:/opt/OumanHA# python3 OumanHA.py
 * Serving Flask app 'OumanHA'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
```

# Asenna OumanHA palveluksi Raspberryyn ja aseta se käynnistymään automaattisesti järjestelmän käynnistyessä.

1. Kopioi _OumanHA.service_ tiedosto _/etc/systemd/system/_ kansioon.

2. Lataa järjestelmäpalvelut uudelleen
`systemctl daemon-reload`

4. Aktivoi palvelu
`systemctl enable OumanHA.service`

5. Käynnistä palvelu
`systemctl start OumanHA.service`

Hetken päästä FlaskAPI tuo näkyviin dataa Oumanista. Voit kokeilla selaimella http://<raspin_osoite>:5001/measurements sivua, jossa pitäisi palautua kaikki 27 Oumanista noudettua mittausta.


Mittaukset voivat olla eri tavalla eri konfiguraatioissa. Allaoleva lista on oman Oumanini konfiguraatiosta päätelty, jossa L1 piiri säätää lämmitystä ja puukattila hoitaa lämmityksen.
| Nro | Mittaus |
| ------ | ------ |
|    1    |    Menovesi käyrän mukaan    |
|    2    |    Huonekompensointi    |
|    3    |    Huonekompensoinnin aikakorjaus   |
|    4    |    Tuntematon    |
|   5   |      Tuntematon  |
|   6     |    Tuntematon    |
|    7    |    Laskennallinen menovesi    |
|    8    |    Asetusarvon hidastusvaikutus  |
|    9    |    Menoveden lämpötila    |
|    10    |   Ulkolämpötila     |
|    11    |   Hidastettu ulkolämpötila |
|    12    |   Huonelämpötila         |
|    13    |   Hidastettu huonelämpötila     |
|    14    |   Huonekaukosäädön vaikutus     |
|  15   |   L1 venttiilin asentotavoite %     |
|   16     |  L1 venttiilin todellinen asento %      |
|   17    |     Tuntematon     |
|    18    |    Tuntematon      |
|    19    |     Tuntematon     |
|    20    |    Tuntematon      |
|    21    |    Hidastettu ulkolämpötila     |
|    22    |   Tuntematon       |
|   23    |    Tuntematon      |
|    24    |   Tuntematon       |
|   25   |     Tuntematon     |
|   26     |   Tuntematon       |
|    27    |    Tuntematon      |

# License
 Copyright (C) 2025 by Jari Väisänen
 Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.

 THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING 
 ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. 
 IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR 
 ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
 NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.