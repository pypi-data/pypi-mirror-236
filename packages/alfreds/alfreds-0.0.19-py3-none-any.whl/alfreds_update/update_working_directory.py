import json
import os
import yaml

from alfreds_init.init import get_alfred_dir, stop_container, run_container, alfreds_init


def update_working_directory(new_working_directory):
    print("Updating working dir...")
    alfred_agent_dir = get_alfred_dir()
    # read agent path from alfred_agent_dir/config.json
    with open(alfred_agent_dir + "/config.json", "r") as f:
        config = json.load(f)
        agent_path = config["agent_path"]
        seed_dir = config["seed_dir"]

    if agent_path is None:
        print("Error: agent path not found")
        return

    alfreds_init(agent_path, new_working_directory, seed_dir, show_warning=False)
    print("Working directory updated.")

    # write new working directory to alfred_agent_dir/config.json
    config["working_dir"] = new_working_directory
    with open(alfred_agent_dir + "/config.json", "w") as f:
        f.write(json.dumps(config))
