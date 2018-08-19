#!/bin/sh
#echo -n senha|base64
oc volumes dc ${OPENSHIFT_APP_NAME} --add --overwrite --name=configmap-volume --configmap-name=nat-configmap --mount-path=/etc/config/net -n ${OPENSHIFT_PROJECT_NAME}
