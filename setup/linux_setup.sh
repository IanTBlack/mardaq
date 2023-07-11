sudo apt update
sudo apt upgrade

# Install MariaDB/MySQL
sudo apt install mariadb-server


#Install Labjack LJM
cd ~
sudo wget https://cdn.docsie.io/file/workspace_u4AEu22YJT50zKF8J/doc_VDWGWsJAhd453cYSI/boo_9BFzMKFachlhscG9Z/file_21GtgtM0dOeqJYB3l/labjackm-12000-opensuse-linux-aarch64-releasetar.gz
tar -zvxf labjackm-12000-opensuse-linux-aarch64-releasetar.gz
cd LabJackM-1.2000-openSUSE-Linux-aarch64/
sudo ./LabJackM.run