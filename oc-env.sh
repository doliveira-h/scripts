#!/bin/bash
# Set variable value on Openshift 3.5
VAR1="$1"
VAR2="$2"
for dc in $(oc get dc --no-headers|grep -v front|grep -v dash|grep green|awk '{print $1}'); do 
    oc env dc $dc JDBC_URL=$VAR1
    oc env dc $dc REDIS_HOSTNAME=$VAR2
done
