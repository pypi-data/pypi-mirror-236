import click
import subprocess

@click.command()
def start():
    """Start your vm"""
    try:
        subprocess.run(["gcloud", "compute", "instances", "start", "--zone=europe-west4-a", "lewagon-data-eng-vm-kay-pi"], check=True)
        print("VM started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start VM: {e}")

@click.command()
def stop():
    """Stop your vm"""
    try:
        subprocess.run(["gcloud", "compute", "instances", "stop", "--zone=europe-west4-a", "lewagon-data-eng-vm-kay-pi"], check=True)
        print("VM stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop VM: {e}")
@click.command()


def connect():
    """Connect to your vm in vscode inside your ~/code/kay-pi/folder"""
    try:
        subprocess.run([
            "code",
            "--folder-uri",
            "vscode-remote://ssh-remote+panidis.k@35.204.214.151/home/panidis.k/code/kay-pi"
        ], check=True)
        print("Connected to VM in VS Code successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to VM in VS Code: {e}")
