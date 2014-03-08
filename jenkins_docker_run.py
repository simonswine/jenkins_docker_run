#!/usr/bin/python

import os
import subprocess
import sys


CONTAINER_USER='devel'
CONTAINER_HOME='/devel'


def build_cmd(config):

    env_blacklist = ['WORKSPACE','HOME']
    env_vars = []

    # Prepare Environment variables
    for key in os.environ.keys():
        if key in env_blacklist:
            continue
        env_vars += [ 
            '-e',
            "%s=%s" % (key,os.environ[key])
        ]

    # Workspace in 
    workspace = os.path.join(
        CONTAINER_HOME,
        'workspace',
        os.path.basename(config['workspace'])
    )

    cmd = [
        '/usr/bin/docker',  # docker binary
        'run',              # run a command
        '-t',               # pseudo tty
        '-rm',              # remove afterwards
        '-u',               # use configured user 
        config['user'],
        '-v',               # mount workspace
        '%s:%s' % (config['workspace'],workspace),
        '-v',               # mount tmp_dir
        '%s:%s' % (config['tmp_dir'],config['tmp_dir']),
        '-e',
        'WORKSPACE=%s' % workspace,
        '-e',
        'HOME=%s' % CONTAINER_HOME,
   ] + env_vars + [
        '-w',
        workspace,
        config['image'],
        '/bin/bash','-l',
        config['cmd']
        ]

    return cmd


def main():

    config={}

    try:
        # TODO validate
        config['workspace']=os.environ['WORKSPACE']
        os.environ['JENKINS_HOME']
        os.environ['HOME']
    except:
        print >> sys.stderr, 'I must be executed within a jenkins job'
        sys.exit(1)

    config['user'] = CONTAINER_USER
    config['tmp_dir'] = '/tmp'

    #TODO validate
    config['image'] = sys.argv[1]
    #TODO validate, copy
    config['cmd'] = sys.argv[2]


    cmd = build_cmd(config)
    #print ("Running docker command:")
    #print (' '.join(cmd))

    process = subprocess.Popen(cmd,stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
	
    sys.exit(process.wait())
	


    pass


if __name__ == "__main__":
    main()
