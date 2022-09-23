#!/usr/bin/env python -u
import logging
import sys
import os
import yaml
import common

from kubernetes import client
from kubernetes.client.rest import ApiException

logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                    format='%(levelname)s: %(name)s: %(message)s')
log = logging.getLogger('kubernetes-model-source')


def main():
    if os.environ.get('RD_CONFIG_DEBUG') == 'true':
        log.setLevel(logging.DEBUG)
        log.debug("Log level configured for DEBUG")

    data = {
        "type": os.environ.get('RD_CONFIG_TYPE'),
        "yaml": os.environ.get('RD_CONFIG_YAML'),
        "namespace": os.environ.get('RD_CONFIG_NAMESPACE')
    }

    common.connect()

    try:
        dep = yaml.safe_load(data["yaml"])

        if data["type"] == "Deployment":
            api_instance = client.AppsV1Api()
            resp = api_instance.create_namespaced_deployment(
                body=dep,
                namespace=data["namespace"],
                pretty="true")

        elif data["type"] == "ConfigMap":
            api_instance = client.CoreV1Api()
            resp = api_instance.create_namespaced_config_map(
                namespace=data["namespace"],
                body=dep,
                pretty="true")

        elif data["type"] == "StatefulSet":
            api_instance = client.AppsV1Api()
            resp = api_instance.create_namespaced_stateful_set(
                body=dep,
                namespace=data["namespace"],
                pretty="true")

        elif data["type"] == "Service":
            api_instance = client.CoreV1Api()
            resp = api_instance.create_namespaced_service(
                namespace=data["namespace"],
                body=dep,
                pretty="true")

        elif data["type"] == "Ingress":
            api_instance = client.ExtensionV1beta1Api()
            resp = api_instance.create_namespaced_ingress(
                body=dep,
                namespace=data["namespace"],
                pretty="true")

        elif data["type"] == "Job":
            api_instance = client.BatchV1Api()
            resp = api_instance.create_namespaced_job(
                namespace=data["namespace"],
                body=dep,
                pretty="true")

        elif data["type"] == "StorageClass":
            api_instance = client.StorageV1Api()
            resp = api_instance.create_storage_class(
                body=dep,
                pretty="true")

        elif data["type"] == "PersistentVolumeClaim":
            api_instance = client.CoreV1Api()
            resp = api_instance.create_namespaced_persistent_volume_claim(
                namespace=data["namespace"],
                body=dep,
                pretty="true")

        elif data["type"] == "Secret":
            api_instance = client.CoreV1Api()
            resp = api_instance.create_namespaced_secret(
                namespace=data["namespace"],
                body=dep,
                pretty="true")

        elif data["type"] == "PersistentVolume":
            api_instance = client.CoreV1Api()
            resp = api_instance.create_persistent_volume(
                body=dep,
                pretty="true")

        else:
            log.exception("No valid object type: " + data["type"])
            sys.exit(1)

        print(common.parseJson(resp.status))

    except ApiException:
        log.exception("Exception error creating: " + data["type"])
        sys.exit(1)


if __name__ == '__main__':
    main()
