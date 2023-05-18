# Real Estate

### Clone the project
**Clone the repo:**
```
git clone https://github.com/Kelp1e/real_estate.git
```

### Build Docker's Containers
**Linux / MacOS** by using Makefile:
```
cd real_estate
make build
```
**Windows:**
```
cd real_estate
docker compose up --build -d --remove-orphans
```
**Windows** by using Chocolatey:
```
Get-ExecutionPolicy
Set-ExecutionPolicy AllSigned
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install make
cd real_estate
make build
```
