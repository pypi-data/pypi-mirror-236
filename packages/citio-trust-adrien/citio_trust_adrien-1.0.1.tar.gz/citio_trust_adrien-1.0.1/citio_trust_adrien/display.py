import subprocess as sp
import os
import shutil


def display_and_save_infos():
    target_file = "staging.json"

    cmd = f"find $HOME -name {target_file} 2>/dev/null"
    try:
        files = sp.check_output(cmd, shell=True)
    except sp.CalledProcessError as e:
        files = e.output
    finally:
        encoding = "utf-8"
        files = files.decode(encoding).split()

    path_to_write_personal_infos = os.environ["HOME"] + "/tmp/citio_trust_adrien/personal_infos"

    if os.path.exists(path_to_write_personal_infos):
        print(f"Deleting folder {path_to_write_personal_infos}\n")
        shutil.rmtree(path_to_write_personal_infos)
    os.makedirs(
        path_to_write_personal_infos,
    )
    sp.check_output(f"env >> {path_to_write_personal_infos}/env_infos.txt", shell=True)

    if files:
        settings_content = ""
        with open(files[0], "r") as f:
            settings_content += f.read() + "\n"

        with open(f"{path_to_write_personal_infos}/my_settings.txt", "w") as f:
            print(
                f"WRITING YOUR DEEPEST SECRETS AT {path_to_write_personal_infos}/my_settings.txt"
            )
            f.write(settings_content)
            print("-----------------------------------------------------------")
            print("SENDING YOUR DEEPEST SECRETS TO A RANDOM SERVER")
            print("No I am kidding but I could")
        print("ANYWAY, HERE ARE THE GOOGLE SETTINGS THAT WOULD HAVE BEEN SENT TO THE SERVER\n:")
        print("\n-----------------------------------------------------------")
        sp.run(f"cat {path_to_write_personal_infos}/my_settings.txt", shell=True)
        print("\n-----------------------------------------------------------")
        print("\nAND HERE ARE YOUR ENVIRONMENT INFOS:\n")
        sp.run(f"cat {path_to_write_personal_infos}/env_infos.txt", shell=True)

    else:
        print(
            f"You don't have a setting {target_file} somewhere on our laptop?. "
            "Please ask someone for this presentation and reinstall the package"
        )
