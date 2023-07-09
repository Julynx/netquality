# netquality
*Benchmark your internet connection.*
<br>
<br>

Measure speed, ping, jitter and packet loss.            |  Get a rating to understand and compare results.
:-------------------------:|:-------------------------:
![](https://i.imgur.com/K1hF3o6.png)  |  ![](https://i.imgur.com/diodVSM.png)

<br>

## Downloading and running (Ubuntu)
First, install [speedtest-cli](https://www.speedtest.net/es/apps/cli):
```
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest
```
Then, clone this repository:
```
git clone https://github.com/julynx/netquality
cd netquality
sudo chmod +x netquality
```
You can now run ```netquality``` from the folder.

<br>

## Installing to system path (Linux)
Open a **Terminal** inside the **netquality folder** and run the following command:
```
sudo cp netquality /usr/bin
```
You can now run netquality from anywhere with the ```netquality``` command.

<br>

## Uninstalling
To uninstall ```netquality```, simply remove the installation folder and the executables from the system path.
