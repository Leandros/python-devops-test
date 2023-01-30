#!/usr/bin/env python3
import argparse
import subcommands.deploy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='cli',
            description='DevOps Coding Challenge')

    # persistent flags:
    parser.add_argument("-v", "--verbose",
                        help="enable verbose logging",
                        action="store_true",
                        dest="verbose")

    subparser = parser.add_subparsers(dest="subparser", required=True)

    # deploy --to=<to> <project>
    deploy_parser = subparser.add_parser("deploy")
    deploy_parser.add_argument("--to",
                               help="Which environment to deploy to [possible values: dev, staging, prod]",
                               action="store",
                               choices=["dev", "staging", "prod"],
                               required=True)
    deploy_parser.add_argument("project",
                               help="The project to deploy [possible values: frontend, backend]",
                               action="store",
                               choices=["frontend", "backend"])

    args = parser.parse_args()

    if args.subparser == "deploy":
        subcommands.deploy.deploy(args.to, args.project)

# Doxy.me Senior DevOps Coding Challenge:
#
# You're looking at a Python3 CLI application to interact with AWS.
#
# It's using argparse to parse and process command line arguments.
# Furthermore, the application depends on the AWS Python SDK. For any
# further dependencies check the `requirements.txt`.
#
#
# Task:
#
# Your task is to add a new sub-command called 'upload'. This command must
# take a single parameter, the path to a file (e.g., `./main.py upload <path-to-file>`).
# The file specified must be uploaded to an AWS S3 bucket, using the already
# provided interface in `providers/s3.py`.
# The file must be renamed and uploaded to S3 as `<unixtimestamp>.<original-file-ending>`.
#
# ** Please implement the subcommand and the required tests. **
#
#
# Further information:
#
# The S3 interface has two implementations, the first implementation is using
# the boto3 sdk, the second implementation is a mock implementation to be used
# for testing. It's guaranteed to make no network requests.
