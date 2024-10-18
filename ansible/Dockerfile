# CentOS8
FROM centos:8

# system update
RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

RUN yum -y update && yum clean all

# install sudo & nano
RUN yum -y install sudo && yum install -y nano
# install ssh clients
RUN yum -y install openssh-clients

# install python3.9
RUN yum -y install openssl-devel bzip2-devel libffi-devel
RUN yum -y groupinstall "Development Tools"
RUN dnf module -y install python39
RUN alternatives --set python /usr/bin/python3.9

# install ansible
RUN python3 -m pip -V
RUN pip3 install --upgrade pip
RUN pip3 install ansible
RUN ansible-galaxy collection install community.general

# COPY data
COPY ./Ansible_Playbook/ /root/Ansible_Playbook/
