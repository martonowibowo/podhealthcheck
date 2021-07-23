from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from datetime import datetime
from pprint import pprint
import pytz
import os
from os import getenv
from time import sleep
from dotenv import load_dotenv


load_dotenv()


def loadConfig():
    kubeContext = getenv('kubecontext')
    deployment = getenv('deployment','local')

    #load kubeconfig
    if deployment == 'local':
        config.load_kube_config(context=kubeContext)
    else:
        config.load_incluster_config()


def deletePod(name,namespace):

    print ("delete Pod")
    v1 = client.CoreV1Api()
    podname=name
    namespace=namespace
    grace_period_seconds=10
    try:
        delpod = v1.delete_namespaced_pod(podname,namespace,grace_period_seconds=grace_period_seconds,pretty=True)
        pprint (delpod) 
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)

def main():
    while True:
        namespace = getenv('namespace')


        utc = pytz.timezone('UTC')
        now = datetime.now(utc)
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("Current Time =", current_time)

        v1 = client.CoreV1Api()

        ret = v1.list_namespaced_pod(namespace=namespace)
        for i in ret.items:
            namespace = i.metadata.namespace
            pod_name = i.metadata.name
            state = i.status.phase
            reason = i.status.reason
            message = i.status.message
            start_time = i.status.start_time
            #print(type(start_time))
            if state != "Running" and state != "Succeeded" and state != "Failed":
                print("%s\t%s\t%s" % (state,start_time,pod_name))
                if type(start_time) == None.__class__ :
                    selisihWaktu = 0
                    print (selisihWaktu)
                    deletePod(pod_name,namespace)
                else:
                    selisihWaktu = now-start_time
                    selisihWaktu = selisihWaktu.seconds
                    print (selisihWaktu)
                    if selisihWaktu > 600:
                        deletePod(pod_name,namespace)
        sleep(30)

if __name__ == "__main__":
    loadConfig()
    main()