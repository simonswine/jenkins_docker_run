#!/usr/bin/python

import os
import subprocess
import sys


JENKINS_USER='jenkins'
JENKINS_HOME='/jenkins'


def build_cmd(config):

    cmd = [
        '/usr/bin/docker',  # docker binary
        'run',              # run a command
        '-t',               # pseudo tty
        '-rm',              # remove afterwards
        '-u',               # use user jenkins
        config['user'],
        '-v',               # mount workspace
        '%s:%s' % (config['workspace'],config['workspace']),
        '-v',               # mount tmp_dir
        '%s:%s' % (config['tmp_dir'],config['tmp_dir']),
        '-w',
        config['workspace'],
        config['image'],
        '/bin/bash',
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

    config['user'] = JENKINS_USER

    config['tmp_dir'] = '/tmp'

    #TODO validate
    config['image'] = sys.argv[1]
    #TODO validate, copy
    config['cmd'] = sys.argv[2]


    cmd = build_cmd(config)
    print ("Running command: ",' '.join(cmd))


    subprocess.call(cmd,stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    pass


if __name__ == "__main__":
    main()



 


#/usr/bin/docker run -t -u jenkins -v /tmp:/tmp -v $WORKSPACE:$WORKSPACE -w $WORKSPACE jenkins1.dmz:5000/former03/jenkins_slave:wheezy_ruby_test /bin/bash
