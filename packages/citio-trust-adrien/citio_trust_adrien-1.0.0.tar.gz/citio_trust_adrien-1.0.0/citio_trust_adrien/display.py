import subprocess as sp
import os


def display_infos():
    target_file = "staging.json"

    cmd = f"find $HOME -name {target_file} 2>/dev/null"
    try:
        files = sp.check_output(cmd, shell=True)
    except sp.CalledProcessError as e:
        files = e.output
    finally:
        encoding = "utf-8"
        files = files.decode(encoding).split()

    cwd_parent = os.path.dirname(os.getcwd())
    path_to_write_env_infos = cwd_parent + "/personal_infos/env_infos.txt"
    path_to_write_settings = cwd_parent + "/personal_infos/my_settings.txt"

    if os.path.exists(path_to_write_env_infos):
        os.remove(path_to_write_env_infos)
    sp.check_output(f"env >> {path_to_write_env_infos}", shell=True)

    if files:
        settings_content = ""
        with open(files[0], "r") as f:
            settings_content += f.read() + "\n"

        with open(path_to_write_settings, "w") as f:
            print(f"Writing your deepest secrets at {path_to_write_settings}")
            f.write(settings_content)
            print("Sending your deepest secrets to a random server")
            print("No I am kidding but I could")
        print("ANYWAY, HERE ARE THE GOOGGLE SETTINGS THAT WOULD HAVE BEEN SENT TO THE SERVER\n:")
        sp.run(f"cat {path_to_write_settings}", shell=True)
        print("\nAND HERE ARE YOUR ENVIRONMENT INFOS:\n")
        sp.run(f"cat {path_to_write_env_infos}", shell=True)

    else:
        print(
            f"You don't have a setting {target_file} somewhere on our laptop?. "
            "Please ask someone for this presentation and reinstall the package"
        )
