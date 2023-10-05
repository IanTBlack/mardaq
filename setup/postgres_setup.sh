sudo apt update
sudo apt upgrade
printf "\033[0;32mInstalling required Python packages...\033[0m\n"
printf "\033[0;32mInstalling postgresql...\033[0m\n"
sudo apt install postgresql

printf "\033[0;32mInstalling psycopg2...\033[0m\n"
sudo apt install -y python3-psycopg2