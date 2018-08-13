#!/bin/bash

#    Copyright (C) <2018>  <Akshat Singh>
#    <akshat-pg8@iiitmk.ac.in>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}Cleaning the system...${NC}"
make clean

echo -e ""
echo -e "${RED}Bringing down the whole system...${NC}"
make down

sleep 5
echo -e ""
for (( i=1; i<=6; i++ )); do
  echo -e "${RED}[$i] Pruning all the containers...${NC}"
  docker container prune -f
  sleep 2
done;

echo -e ""
echo -e "${RED}Pruning the left-over containers...${NC}"
cid=`docker ps -a | awk '{print $1}' | tail -1`
docker stop $cid
docker rm $cid

echo -e ""
for (( i=1; i<=5; i++ )); do
  echo -e "${RED}[$i] Pruning all the volumes...${NC}"
  docker volume prune -f
  sleep 2
done;

echo -e ""
echo -e "${RED}Pruning the docker networks...${NC}"
docker network prune -f

echo -e ""
echo -e "${RED}Build all images?${NC}"
read -p "Press y for yes, waiting: " -n 1 -r
echo -e   
if [[ $REPLY =~ ^[Yy]$ ]]
then
    make build-all
    echo -e ""
    echo -e "${RED}Removing dangling images...${NC}"
    docker rmi $(docker images -f dangling=true  | awk '{print $3}')
fi

echo -e ""
echo -e "${RED}Bring the whole cluster up?${NC}"
read -p "Press y for yes, waiting: " -n 1 -r
echo -e    
if [[ $REPLY =~ ^[Yy]$ ]]
then
    make up
fi

sleep 10

echo -e ""
echo -e "${RED}zm-docker services statistics...${NC}"
docker stack services zm-docker
