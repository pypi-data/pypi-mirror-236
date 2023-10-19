"""
@file server.py
@brief A Flask server for submitting repository URLs to be built by a CIS

@date January 17, 2022

@author
 - InnovAnon, Inc.
 - Assistant AI
"""

from logging import DEBUG
from os import environ, path
from traceback import format_tb
from typing import Dict, List, Tuple, Union, Optional

from docker import DockerClient, errors, from_env, types # type: ignore
from flask import Flask, request
#from libia.log import configure_logging
from teamhack_cis.log import configure_logging

logger = configure_logging(__name__)


class DockerAPIError(Exception):
    """Custom exception for Docker API errors."""


class ServerError(Exception):
    """Custom exception for server errors."""


def cis_daemon(dc:DockerClient, mounts:List[types.Mount],
               url:str, image:str, secrets:Dict[str,str])->Tuple[str,int]:
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
                                    environment=environment,
                                    mounts=mounts,
                                    network='teamhack_default',
                                    #restart_policy='no',
                                    #detach=True,
                                    tty=False,
                                    stdin_open=False
                                    #auto_remove=True
                                    )
        logger.debug('container created')

        try:
            # Start the container
            cont.start()
            logger.debug('container started')

            # Wait for the container to complete its execution
            status = cont.wait()['StatusCode']
            logger.debug('container execution completed, status: %s', status)
            if status == 0:
                status = 200
            else:
                status = 400

            # Get the container logs
            logs = cont.logs().decode('utf-8')
            logger.debug('container logs: %s', logs)

            # return useful output and HTML status
            return logs, status

        finally:
            # Remove the container
            cont.remove()
            logger.debug('container removed')

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

DEFAULT_IMAGE = environ.get('IA_CIS_BUILD', 'innovanon/build')

def create_app(dc:DockerClient, mounts:List[types.Mount])->Flask:
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
            image = data.get('image',         DEFAULT_IMAGE)
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
            ret = cis_daemon(dc, mounts, url, image, secrets)
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
        #assert status == 200
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


def check_exists(file_path:str)->None:
    """ raise an exception is it doesn't """
    if not path.exists(file_path):
        logger.error('file DNE: %s', file_path)
        raise ServerError(f'file DNE: {file_path}')

def check_file_exists(file_path:str)->None:
    """ raise an exception is it doesn't """

    check_exists(file_path)

    if not path.isfile(file_path):
        logger.error('is not file: %s', file_path)
        raise ServerError(f'is not file: {file_path}')

def check_dir_exists(file_path:str)->None:
    """ raise an exception is it doesn't """

    check_exists(file_path)

    if not path.isdir(file_path):
        logger.error('is not dir: %s', file_path)
        raise ServerError(f'is not dir: {file_path}')

def check_sock_exists(file_path:str)->None:
    """ raise an exception is it doesn't """

    #check_file_exists(file_path)
    logger.info('cannot test: %s', file_path)

    # doesn't work
    #if not path.getfiletype(file_path) == 'SOCK':
    #    logger.error('is not sock: %s', file_path)
    #    raise ServerError(f'is not sock: {file_path}')

def get_mount(file_path:str, target:Optional[str]=None,
              read_only:bool=True)->types.Mount:
    """ create bind mount object """
    if target is None:
        target = file_path

    mount = types.Mount(
        source=file_path, target=target,
        type='bind', read_only=read_only)

    return mount

def get_mount2(file_path:str, target:str,
               read_only:bool=True)->types.Mount:
    """ create volume mount object """
    mount = types.Mount(
        source=file_path, target=target,
        type='volume', read_only=read_only)

    return mount


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

    mounts = []

    # bind-mounts seem to be looking for paths on the host !

    # files
    for file_path in [
        # configure build container to use apt-cacher-ng
        #'/etc/apt/apt.conf.d/00aptproxy',
        # branding
        '/etc/issue',
        '/etc/issue.net',
        #'/etc/motd',
    ]:
        check_file_exists(file_path)
        mount = get_mount(file_path)
        mounts.append(mount)

    # directories
    for file_path in [
        # configure most other tools to use compiler farm
        #'/etc/ccache.conf.d/',
        # configure build system to use centralized logging
        #'/etc/rsyslog.d/',
    ]:
        check_dir_exists(file_path)
        mount = get_mount(file_path)
        mounts.append(mount)

    # configure build container's Bazel to use compiler farm
    #file_path = '/root/.bazelrc'
    #check_file_exists(file_path)
    #mount = get_mount(file_path, target='/home/cis/.bazelrc')
    #mounts.append(mount)

    # bind-mounts our socket for building Docker images within the nested build container
    file_path = '/var/run/docker.sock'
    check_sock_exists(file_path)
    mount = get_mount(file_path, read_only=False)
    mounts.append(mount)

    mount = get_mount2('ccache-etc', target='/etc/ccache.conf.d/')
    mounts.append(mount)

    mount = get_mount2('syslog-client', target='/etc/rsyslog.d/')
    mounts.append(mount)

    mount = get_mount2('build-ccache',
                      target='/var/cache/ccache/', read_only=False)
    mounts.append(mount)


    logger.debug('mounts created')
    return dc, mounts


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
    dc, mounts = get_dc()

    secrets:Dict[str,str] = {}
    fuck_url = 'ssh+git://git@git.innovanon.com:2222/srv/git/InnovAnon-Inc/cis-test.git'
    setup_environment(secrets, None, None)
    output, status = cis_daemon(dc, mounts,
                                fuck_url,
                                'ubuntu', secrets)
    logger.debug('output: %s, status: %s', output, status)

    app = create_app(dc, mounts) # , **kwargs)
    app.run(debug=True, host=host, port=port) #, *args)

# https://www.easydevguide.com/posts/curl_upload_flask
