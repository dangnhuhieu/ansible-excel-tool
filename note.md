# ansible-excel-tool

docker-compose build --no-cache
docker-compose up -d
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ansible
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' node01

docker exec -it ansible /bin/bash
docker exec -it node01 /bin/bash


httpd_install_inventory.txt
[node]
172.19.0.3

test ssh
ssh root@172.19.0.3


ansible node -m ping -i httpd_install_inventory.txt
# run as roles
ansible-playbook -i httpd_install_inventory.txt httpd_install_playbook.yml

# remove all
docker-compose down
docker volume remove ansible-excel-tool_Ansible_Playbook
docker images
docker image rm ansible-excel-tool-ansible
docker image rm ansible-excel-tool-node01

# run python tool
python .\ansible\Ansible_Playbook\excel\main.py httpd_parameter_sheet.xlsx