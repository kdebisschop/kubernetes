#!/usr/bin/env python -u
import logging
import sys
import os
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

    common.connect()

    data = {}
    data["api_version"] = os.environ.get('RD_CONFIG_API_VERSION')
    data["name"] = os.environ.get('RD_CONFIG_NAME')
    data["namespace"] = os.environ.get('RD_CONFIG_NAMESPACE')
    force = os.environ.get('RD_CONFIG_FORCE')

    try:

        k8s_client = client.BatchV1Api()
        job = k8s_client.read_namespaced_job(
            name=data["name"],
            namespace=data["namespace"]
        )
        if not force and job.status and job.status.active:
            log.info('Previous job run still active; not deleting')
            return
        job.metadata.creation_timestamp = None
        job.metadata.uid = None
        job.metadata.resource_version = None
        job.status = None
        job.spec.selector = None
        job.spec.template.metadata = None

        body = client.V1DeleteOptions(api_version='v1',kind="DeleteOptions",propagation_policy="Background")
        pretty = 'pretty_example'

        api_response = k8s_client.delete_namespaced_job(
            name=data["name"],
            namespace=data["namespace"],
            body=body,
            pretty=pretty
        )

        print(common.parseJson(api_response))

        api_response = k8s_client.create_namespaced_job(
            body=job,
            namespace=data["namespace"]
        )

        print(common.parseJson(api_response.status))

    except ApiException:
        log.exception("Exception creating job:")
        sys.exit(1)


if __name__ == '__main__':
    main()
