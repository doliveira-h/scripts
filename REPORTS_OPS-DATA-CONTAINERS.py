#!-*- conding: utf8 -*-
"""
    Developed by: Danilo Oliveira
    E-mail: doliveira.h@gmail.com
"""
import sys
import json
import openshift
#from easy_openshift import openshift

def help():
    """ 
        Params Help
    """
    print("## Param 01: Regiao do openshift")
    print("## Param 02: Ambiente")
    print("## Param 03: Openshit usuário")
    print("## Param 04: Openshit senha")

def print_dcs(region, env , project, dcs):
    """
        Print information for each DeploymentConfig inside of DeploymentConfigList dcs
    """
    for dc in dcs["items"]:
        name=dc["spec"]["template"]["spec"]["containers"][0]["name"]
        image=dc["spec"]["template"]["spec"]["containers"][0]["image"]
        if dc["spec"]["template"]["spec"]["containers"][0]["resources"].get("limits"):
            lcpu=dc["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"].get("cpu")
            lmem=dc["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"].get("memory")
        else:
            lcpu=None
            lmem=None
        if dc["spec"]["template"]["spec"]["containers"][0]["resources"].get("requests"):
            rcpu=dc["spec"]["template"]["spec"]["containers"][0]["resources"]["requests"].get("cpu")
            rmem=dc["spec"]["template"]["spec"]["containers"][0]["resources"]["requests"].get("memory")
        else:
            rcpu=None
            rmem=None
        print("{};{};{};{};{};{};{};{};{}".format(region, env, project, name, rcpu, lcpu, rmem, lmem, image))

def main():        
    """
        Main loop
    """
    try:
        oc = openshift.Openshift()

        # variables
        openshift_regions = sys.argv[1].lower()
        openshift_envs = sys.argv[2].lower()
        openshift_username = sys.argv[3].lower()
        openshift_password = sys.argv[4].lower()
        #print csv header
        print("REGION;AMBIENTE;PROJETO;APP;REQUESTS_CPU;LIMITS_CPU;REQUESTS_MEMORY;LIMITS_MEMORY;REGISTRY_IMAGE")
        
        #login on regions  
        for regions in openshift_regions.split(','):
            host = 'https://api.{0}.paas.gsnetcloud.corp:8443'.format(regions)
            userpass = '{0}:{1}'.format(openshift_username, openshift_password)
            token = oc.get_login_token(host, userpass.encode())
            #list all projects
            projects = oc.get_projects(host, token)
            for project in projects["items"]:
                project_name=project["metadata"]["name"]
                for openshift_env in openshift_envs.split(','):
                    if openshift_env in project_name:
                        #get all deploymentconfigs from project
                        dcs = oc.get_deploymentconfigs(host, project_name, token)
                        print_dcs(regions, openshift_env, project_name, dcs)

    except (ValueError, TimeoutError, EOFError, IOError, SystemError, SyntaxError) as err:
        print("\n==> Erro: ", err)
        raise err

if __name__ == "__main__":
    if len(sys.argv) != 5:
        help()
    else:
        main()