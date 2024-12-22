#!/bin/bash

sudo cp ble-scan.service /etc/systemd/system/
sudo cp ble-scan.timer /etc/systemd/system/

sudo cp ble-stop-end.service /etc/systemd/system/
sudo cp ble-stop-end.timer /etc/systemd/system/
