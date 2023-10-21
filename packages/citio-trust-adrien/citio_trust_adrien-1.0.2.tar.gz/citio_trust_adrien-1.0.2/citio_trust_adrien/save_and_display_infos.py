import subprocess as sp
import os
import shutil

PATH_TO_WRITE_PERSONAL_INFOS = os.environ["HOME"] + "/citio_trust_adrien/personal_infos"


def save_infos() -> None:
    target_file = "staging.json"

    cmd = f"find $HOME -name {target_file} 2>/dev/null"
    try:
        files = sp.check_output(cmd, shell=True)
    except sp.CalledProcessError as e:
        files = e.output
    finally:
        encoding = "utf-8"
        files = files.decode(encoding).split()

    if os.path.exists(PATH_TO_WRITE_PERSONAL_INFOS):
        shutil.rmtree(PATH_TO_WRITE_PERSONAL_INFOS)
    os.makedirs(
        PATH_TO_WRITE_PERSONAL_INFOS,
    )
    sp.check_output(f"env >> {PATH_TO_WRITE_PERSONAL_INFOS}/env_infos.txt", shell=True)

    if files:
        settings_content = ""
        with open(files[0], "r") as f:
            settings_content += f.read() + "\n"

        with open(f"{PATH_TO_WRITE_PERSONAL_INFOS}/my_settings.txt", "w") as f:
            f.write(settings_content)


def display_infos() -> None:
    if os.path.exists(f"{PATH_TO_WRITE_PERSONAL_INFOS}/my_settings.txt"):
        print("\n-----------------------------------------------------------")
        print(f"WRITING YOUR DEEPEST SECRETS AT {PATH_TO_WRITE_PERSONAL_INFOS}/my_settings.txt")
        print("SENDING YOUR DEEPEST SECRETS TO A RANDOM SERVER")
        print("No I am kidding but I could")
        print("ANYWAY, HERE ARE THE GOOGLE SETTINGS THAT WOULD HAVE BEEN SENT TO THE SERVER\n:")
        print("\n-----------------------------------------------------------")
        sp.run(f"cat {PATH_TO_WRITE_PERSONAL_INFOS}/my_settings.txt", shell=True)
    else:
        print(
            "YOU DON'T HAVE A SETTING staging.json STORED SOMEWHERE ON YOUR LAPTOP? "
            "PLEASE ASK SOMEONE FOR THIS DEMO AND REINSTALL THE PACKAGE"
        )
    print("\n-----------------------------------------------------------")
    print("\nAND HERE ARE YOUR ENVIRONMENT INFOS:\n")
    print("\n-----------------------------------------------------------")
    sp.run(f"cat {PATH_TO_WRITE_PERSONAL_INFOS}/env_infos.txt", shell=True)
