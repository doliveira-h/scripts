#!/bin/bash
for dc in $(oc get dc --no-headers|grep -v front|awk '{print $1}'); do 
    oc set probe dc $dc --liveness --get-url=http://:8081/actuator/health --initial-delay-seconds=180
    oc set probe dc $dc --readiness --get-url=http://:8081/actuator/health --initial-delay-seconds=180
done
