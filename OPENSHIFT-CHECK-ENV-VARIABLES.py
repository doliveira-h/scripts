#!-*- conding: utf8 -*-
"""
    Developed by: Danilo Oliveira
    E-mail: doliveira.h@gmail.com
"""
import sys
import json
import openshift

def help():
    """ 
        Params Help
    """
    print("## Param 01: Regiao origem do openshift")
    print("## Param 02: Projeto origem do openshift")
    print("## Param 03: DeploymentConfig origem do openshift")
    print("## Param 04: Regiao destino do openshift")
    print("## Param 05: Projeto destino do openshift")
    print("## Param 06: DeploymentConfig destino do openshift")   
    print("## Param 07: Openshit usuario")
    print("## Param 08: Openshit senha")

def converte(l):
    d = dict()
    for i in l:
        if i.get("value"):
            d[i["name"]]=i["value"]
        else:
            d[i["name"]]=""
    return d

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same

def main():
    """
        Main loop
    """
    try:
        oc = openshift.Openshift()

        # variables
        openshift_region1 = sys.argv[1].lower()
        openshift_project1 = sys.argv[2].lower()
        openshift_dc1 = sys.argv[3].lower()
        openshift_region2 = sys.argv[4].lower()
        openshift_project2 = sys.argv[5].lower()
        openshift_dc2 = sys.argv[6].lower()
        openshift_username = sys.argv[7].lower()
        openshift_password = sys.argv[8].lower()
        host = 'https://api.{0}.paas.gsnetcloud.corp:8443'.format(openshift_region1)
        userpass = '{0}:{1}'.format(openshift_username, openshift_password)
        token = oc.get_login_token(host, userpass.encode())
        dc1 = oc.get_deploymentconfig(host, openshift_project1, token, openshift_dc1)
        if openshift_region1 != openshift_region2:
            host = 'https://api.{0}.paas.gsnetcloud.corp:8443'.format(openshift_region2)
            token = oc.get_login_token(host, userpass.encode())
        dc2 = oc.get_deploymentconfig(host, openshift_project2, token, openshift_dc2)
        env1 = converte(dc1['spec']['template']['spec']['containers'][0]['env'])
        env2 = converte(dc2['spec']['template']['spec']['containers'][0]['env'])
        added, removed, modified, same = dict_compare(env1, env2)
        print("Variaveis {}:{} [{}] ==> {}:{} [{}]".format(openshift_region1, openshift_project1, openshift_dc1, openshift_region2, openshift_project2, openshift_dc2))
        print("Modificadas:")
        for m in modified:
            print("{} = [{}] [{}]".format(m,modified[m][0],modified[m][1]))
        print("\nAdicionadas {}:{} [{}]".format(openshift_region1, openshift_project1, openshift_dc1))
        for add in added:
            print("{}".format(add))
        print("\nAdicionadas {}:{} [{}]".format(openshift_region2, openshift_project2, openshift_dc2))
        for rem in removed:
            print("{}".format(rem))
        print("\nNao Modificadas")
        for s in same:
            print("{}".format(s))
    except (ValueError, TimeoutError, EOFError, IOError, SystemError, SyntaxError) as err:
        print("\n==> Erro: ", err)
        raise err

if __name__ == "__main__":
    if len(sys.argv) != 9:
        help()
    else:
        main()    
