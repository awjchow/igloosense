#!/bin/bash
 
#Make a new dir where you'll put the binary
sudo mkdir /opt/node
 
#Get it
wget http://nodejs.org/dist/v0.12.0/node-v0.12.0-linux-arm-pi.tar.gz
 
#unpack
tar xvzf node-v0.12.0-linux-arm-pi.tar.gz
 
#Copy to the dir you made as the first step
sudo cp -r node-v0.12.0-linux-arm-pi/* /opt/node
 
#Add node to your path so you can call it with just "node"
cd ~
nano .bash_profile
 
#Add these lines to the file you opened
PATH=$PATH:/opt/node/bin
export PATH
#Save and exit
 
#Test
node -v
npm -v