"""
@file server.py
@brief A Flask server for submitting repository URLs to be built by a CIS

@date January 17, 2022

@author
 - InnovAnon, Inc.
 - Assistant AI
"""

from logging import DEBUG
from os import environ
from traceback import format_tb
from typing import Dict, Tuple, Union, Optional

from docker import DockerClient, errors, from_env, types # type: ignore
from flask import Flask, request
#from libia.log import configure_logging
from teamhack_cis.log import configure_logging

logger = configure_logging(__name__)


class DockerAPIError(Exception):
    """Custom exception for Docker API errors."""


class ServerError(Exception):
    """Custom exception for server errors."""


def cis_daemon(dc:DockerClient, url:str, image:str, secrets:Dict[str,str])->Tuple[str,int]:
    """
    Run a CIS build inside a Docker container.

    Args:
      dc (Docker.client): Docker client object.
      url (str): Repository URL for the repository to be built.
      recursive (bool): Whether to do a recursive checkout.
      branch (str): Branch of the repository.
      image (str): Docker image for running the build.
      secrets (Dict[str,str]): Dictionary to be passed as environment variables to the container.

    Returns:
      Tuple[str,int]: A tuple containing the execution logs and the HTML status code.

    Raises:
      APIError: If there is an error with the Docker API.
      Exception: If there is any other error.
    """

    logger.debug(
        'cis_daemon(url=%s, image=%s)', url, image)

    environment = {
        'IA_CIS_IMAGE': image,
        'IA_CIS_REPOSITORY': url,
    }
    logger.debug('cis_daemon() 2')

    environment.update(secrets)

    try:
        # Create a Docker container within the container
        # image has ENTRYPOINT ["/usr/local/bin/cis"]
        cont = dc.containers.create(image,
                                    environment=environment)
        logger.debug('container created')

        # Start the container
        cont.start()
        logger.debug('container started')

        # Wait for the container to complete its execution
        cont.wait()
        logger.debug('container execution completed')

        # Get the container logs
        logs = cont.logs().decode('utf-8')
        logger.debug('container logs: %s', logs)

        # Remove the container
        cont.remove()
        logger.debug('container removed')

        # return useful output and HTML status
        return logs, 200

    except errors.APIError as e:
        # HandlDocker API errors
        error_message = f'Docker APIError: {e.response.status_code} {e.response.reason}'
        logger.error("".join(format_tb(e.__traceback__)))
        raise DockerAPIError(error_message) from e

    except Exception as e:
        # Handle any other exceptions
        error_message = f'Error: {str(e)}'
        logger.error("".join(format_tb(e.__traceback__)))
        raise ServerError(error_message) from e


def create_app(dc:DockerClient)->Flask:
    """
    Create a Flask application with routes conforming to the Legion Suite's /upload convention.

    Parameters:
    - dc (Docker.client): Docker client object.

    Returns:
    - Flask: The Flask application.

    The Flask application created by this function allows users to submit repository URLs
    to be built by a continuous integration system.
    The application handles requests with the HTTP POST method and
    expects JSON payloads containing the following parameters.

    Example JSON payload:
    {
      "url": "https://github.com/username/repo",
      "recursive": true,
      "branch": "main",
      "image": "custom/image",
      "SECRET_KEY": "abc123",
      "API_KEY": "def456"
    }
    """

    app = Flask(__name__)
    app.logger.setLevel(DEBUG)
    default_image = environ.get('IA_CIS_BUILD', 'innovanon/build')

    @app.route('/upload', methods=['POST'])
    def upload()->Union[Tuple[str,int],Tuple[str,int]]:
        """
        @brief Handle file upload requests.

        @return: Tuple containing the execution logs and the HTML status code.
        """

        logger.debug('upload()')
        try:
            # get the JSON payload
            logger.debug('data: %s', request.get_data()) # need to delete this
            data = request.get_json(force=True)
            logger.debug('data: %s', data)

            # extract our parameters
            #url = data.get('url')
            url = data['url']
            logger.debug('url: %s', url)
            recursive = data.get('recursive')
            logger.debug('recursive: %s', recursive)
            branch = data.get('branch')
            logger.debug('branch: %s', branch)
            # innovanon/build
            image = data.get('image',         default_image)
            logger.debug('image: %s', image)

            # pass the rest to the nested container as environment secrets
            secrets = {
                k: v for k, v in data.items() if k not in {
                    'url', 'recursive', 'branch', 'image'
                }
            }
        except KeyError as e:
            error_message = f'Missing required parameter: {str(e.args[0])}'
            logger.error("".join(format_tb(e.__traceback__)))
            return error_message, 400
        #except Exception as e:
        #    error_message = f'Error: {str(e)}'
        #    logger.error("".join(format_tb(e.__traceback__)))
        #    return error_message, 500

        # run the build
        logger.debug('payload processed')
        setup_environment(secrets, branch, recursive)
        logger.debug('setup environment')

        try:
            ret = cis_daemon(dc, url, image, secrets)
            #ret = str(dc), 200
        except DockerAPIError as e:
            error_message = f'Docker API Error: {str(e)}'
            logger.error("".join(format_tb(e.__traceback__)))
            return error_message, 500
        except ServerError as e:
            error_message = f'Server Error: {str(e)}'
            logger.error("".join(format_tb(e.__traceback__)))
            return error_message, 500

        logger.debug('build finished')
        output, status = ret
        assert status == 200
        return output, status

    return app


def setup_environment(environment:Dict[str,str], branch:Optional[str],
                      recursive:Optional[str])->None:
    """ helper method to add branch, recursive and certdir """
    if branch:
        environment['IA_CIS_BRANCH'] = branch
    if recursive is not None:
        environment['IA_CIS_RECURSIVE'] = recursive
    certdir = environ.get("DOCKER_TLS_CERTDIR",   None)
    if certdir:
        environment['DOCKER_TLS_CERTDIR'] = certdir


def get_dc()->DockerClient:
    """
    Get the Docker client object.

    Returns:
    - docker.client.DockerClient: The Docker client object.

    The function is responsible for creating and configuring the Docker client object
    using the Docker SDK.
    It sets up the necessary mount points for the build container and
    returns the Docker client object.
    """

    dc = from_env()

    # configure build container to use apt-cacher-ng
    mount_apt_proxy = types.Mount(
        '/etc/apt/apt.conf.d/00aptproxy', '/etc/apt/apt.conf.d/00aptproxy',
        type='bind', read_only=True)

    # configure build container's Bazel to use compiler farm
    mount_bazel_conf = types.Mount(
        '/root/.bazelrc', '/home/cis/.bazelrc',
        type='bind', read_only=True)

    # configure most other tools to use compiler farm
    mount_ccache_conf = types.Mount(
        '/etc/ccache.conf.d/', '/etc/ccache.conf.d/',
        type='bind', read_only=True)

    # bind-mounts our socket for building Docker images within the nested build container
    mount_docker_socket = types.Mount(
        '/var/run/docker.sock', '/var/run/docker.sock',
        type='bind')

    # branding
    mount_issue = types.Mount(
        '/etc/issue', '/etc/issue',
        type='bind', read_only=True)
    mount_issue_net = types.Mount(
        '/etc/issue', '/etc/issue.net',
        type='bind', read_only=True)
    mount_motd = types.Mount(
        '/etc/motd', '/etc/motd',
        type='bind', read_only=True)

    # configure build system to use centralized logging
    mount_syslog_conf = types.Mount(
        '/etc/rsyslod.d/', '/etc/rsyslog.d/',
        type='bind', read_only=True)

    mounts = [
        mount_apt_proxy,
        mount_bazel_conf,
        mount_ccache_conf,
        mount_docker_socket,
        mount_issue,
        mount_issue_net,
        mount_motd,
        mount_syslog_conf,
    ]

    # Add mounts to the Docker client object
    for container in dc.containers.list():
        container.mount(mounts)
    logger.debug('mounts added')
    return dc


#, *args:Any, **kwargs:Any)->None:
def start_server(host:str, port:int)->None:
    """
    Starts the Flask server to handle incoming requests.

    Args:
      host (str): The host IP to bind the server to.
      port (int): The port number to bind the server to.
      *args: Additional positional arguments.
      **kwargs: Additional keyword arguments.

    Returns:
      None

    The function creates a Docker client object and a Flask application,
    and then starts the Flask server to listen for incoming requests.
    """
    dc = get_dc()
    app = create_app(dc) # , **kwargs)
    app.run(debug=True, host=host, port=port) #, *args)

# https://www.easydevguide.com/posts/curl_upload_flask
