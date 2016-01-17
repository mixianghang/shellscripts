#!/bin/bash
./retrieveAfrinic.sh 20160101 20160101
./retrieveAfrinic.sh 20160108 20160108
./format/formatAfrinic.sh 20160101 20160101
./format/formatAfrinic.sh 20160108 20160108

