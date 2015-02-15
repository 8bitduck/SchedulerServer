#!/bin/bash
echo "Setting up Development VM"

echo "Fixing tty issue with root"
sed -i 's/^mesg n$/tty -s \&\& mesg n/g' /root/.profile

echo "Updating package lists..."
apt-get -y update
aptitude -y upgrade --safe 2> /dev/null

apt-get -y install \
  python3-pip \
  python3-dev \
  postgresql \
  postgresql-contrib \
  libpq-dev \
  libxml2-dev \
  libxslt1-dev \
  curl

# Install the python3 versions of virtualenv and wrapper
pip3 install virtualenv
pip3 install virtualenvwrapper

sudo -u postgres /usr/bin/createuser -s vagrant
sudo -u postgres /usr/bin/createdb -E utf-8 -O vagrant SMSSchedulerServer_dev

cat >> /home/vagrant/.bashrc <<EOF
export PATH=/usr/local/bin:$PATH
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export DEBUG=True
source /usr/local/bin/virtualenvwrapper.sh
workon SMSSchedulerServer

cd /vagrant

echo "Some helpful commands to get up and running:"
echo "--------------------------------------------"
echo "pip install -r requirements.txt   # Install the python dependencies"
echo "./manage.py runserver [::]:8000   # Run the development server"
echo "./manage.py migrate"              # Apply database changes (to all apps)
echo "./manage.py migrate example 0002" # Roll back migrations on the example app to 0002
echo "./manage.py startapp appname"     # Start a django app called 'appname'
EOF

su vagrant -c "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 && source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv --python=/usr/bin/python3 SMSSchedulerServer"

echo ""
echo "Finished setting up the development server."
echo ""
echo "Login to the vagrant box with:"
echo "vagrant ssh"
echo "Run the Install Requireemnts for pip"
echo "Sync the database"
echo "And then run the server"
