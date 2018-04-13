#!/bin/bash
# -------------------------------------------------------------------------------------- #
# Script para definir variavem de ambiente
# Autor: Danilo Oliveira
# -------------------------------------------------------------------------------------- #
#
DIR_DEVOPS="/opt/rundeck/automations/rundeck_automation/paas_portal"
FILE_SCRIPT="${DIR_DEVOPS}/REPORTS_OPS-DATA-CONTAINERS.py"
PYTHON_PATH="/opt/rundeck/python3-venv/bin/python3"

pushd $(pwd)

"${PYTHON_PATH}" "${FILE_SCRIPT}" \
    "@option.OPENSHIFT_REGIONS@" \
    "@option.OPENSHIFT_AMBIENTES@" \
	"@option.OPENSHIFT_USERNAME@" \
	"@option.OPENSHIFT_PASSWORD@"

popd
