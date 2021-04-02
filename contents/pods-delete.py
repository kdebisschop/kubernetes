#!/usr/bin/env python -u
import logging
import sys
import os
import common

from kubernetes import client
from kubernetes.client.rest import ApiException
from kubernetes.client.api import core_v1_api


logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                    format='%(levelname)s: %(name)s: %(message)s')
log = logging.getLogger('kubernetes-delete-pod')

if os.environ.get('RD_JOB_LOGLEVEL') == 'DEBUG':
    log.setLevel(logging.DEBUG)


def delete_pod(data):
    # Delete pod
    api = core_v1_api.CoreV1Api()
    common.delete_pod(api, data)

    print("Pod deleted successfully")


def main():

    if os.environ.get('RD_CONFIG_DEBUG') == 'true':
        log.setLevel(logging.DEBUG)
        log.debug("Log level configured for DEBUG")

    data = {}

    data["name"] = os.environ.get('RD_CONFIG_NAME', os.environ.get('RD_NODE_DEFAULT_NAME'))
    data["namespace"] = os.environ.get('RD_CONFIG_NAMESPACE', os.environ.get('RD_NODE_DEFAULT_NAMESPACE', 'default'))

    common.connect()

    try:
        delete_pod(data)
    except ApiException:
        log.exception("Exception deleting deployment:")
        sys.exit(1)


if __name__ == '__main__':
    main()
