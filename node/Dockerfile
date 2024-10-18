# CentOS8
FROM centos:8

# install ssh server
RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
RUN yum -y update && yum clean all
RUN yum -y install openssh-server && yum -y install sudo

# install python3.9
RUN yum -y install openssl-devel bzip2-devel libffi-devel
RUN yum -y groupinstall "Development Tools"
RUN dnf module -y install python39
RUN alternatives --set python /usr/bin/python3.9

# create Public key
RUN ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
RUN ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa

# set to login as root
RUN sed -ri 's/^#PermitEmptyPasswords no/PermitEmptyPasswords yes/' /etc/ssh/sshd_config

# set a password for root
RUN echo "root:" | chpasswd

# expose 22 port
EXPOSE 22

# start up sshd
CMD ["/usr/sbin/sshd", "-D"]
