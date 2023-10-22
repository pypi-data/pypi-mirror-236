import subprocess
from argparse import ArgumentParser

from autotrain import logger

from . import BaseAutoTrainCommand


def run_app_command_factory(args):
    return RunSetupCommand(args.update_torch, args.colab)


class RunSetupCommand(BaseAutoTrainCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        run_setup_parser = parser.add_parser(
            "setup",
            description="✨ Run AutoTrain setup",
        )
        run_setup_parser.add_argument(
            "--update-torch",
            action="store_true",
            help="Update PyTorch to latest version",
        )
        run_setup_parser.add_argument(
            "--colab",
            action="store_true",
            help="Run setup for Google Colab",
        )
        run_setup_parser.set_defaults(func=run_app_command_factory)

    def __init__(self, update_torch: bool, colab: bool = False):
        self.update_torch = update_torch
        self.colab = colab

    def run(self):
        # install latest transformers
        cmd = "pip uninstall -y transformers && pip install git+https://github.com/huggingface/transformers.git"
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Installing latest transformers@main")
        _, _ = pipe.communicate()
        logger.info("Successfully installed latest transformers")

        cmd = "pip uninstall -y peft && pip install git+https://github.com/huggingface/peft.git"
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Installing latest peft@main")
        _, _ = pipe.communicate()
        logger.info("Successfully installed latest peft")

        cmd = "pip uninstall -y diffusers && pip install diffusers==0.21.4"
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Installing latest diffusers@main")
        _, _ = pipe.communicate()
        logger.info("Successfully installed latest diffusers")

        cmd = "pip uninstall -y trl && pip install git+https://github.com/huggingface/trl.git"
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Installing latest trl@main")
        _, _ = pipe.communicate()
        logger.info("Successfully installed latest trl")

        if self.colab:
            cmd = "pip install -U xformers"
        else:
            cmd = "pip uninstall -U xformers==0.0.22"
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Installing latest xformers")
        _, _ = pipe.communicate()
        logger.info("Successfully installed latest xformers")

        if self.update_torch:
            cmd = "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info("Installing latest PyTorch")
            _, _ = pipe.communicate()
            logger.info("Successfully installed latest PyTorch")
