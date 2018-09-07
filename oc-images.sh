#!/bin/bash
echo "deployment - image"
for dc in $(oc get dc --no-headers|awk '{print $1}'); do 
	img=$(oc get dc $dc -o jsonpath="{.spec.template.spec.containers[0].image}")
	echo "$dc - $img"
done
