import time
from halo import Halo


def deploy(to, project):
    spinner = Halo(
            text=f"deploying {project}...",
            spinner="bouncingBar")
    spinner.start()

    time.sleep(1.5)

    spinner.succeed(f"successfully deployed {project} to {to}!")
