# set the version of the package

from sys import argv

def main():
    action = argv[1] if len(argv) > 1 else "help"

    match action:
        case "help":
            print("Usage: python version_helper.py [command]")
            print("Commands:")
            print("  show    - Show the current version")
            print("  update [version] - Update the version")
        case "show":
            from ciphercon import __version__
            print(f"Current version: {__version__}")
        case "update":
            if len(argv) < 3:
                print("Please provide a version to update to.")
                return
            new_version = argv[2]
            # check if the version is in the correct format
            if not new_version.count(".") == 2:
                print("Version must be in the format X.Y.Z")
                return
            
            for part in new_version.split("."):
                if not part.isdigit():
                    print("Version must be in the format X.Y.Z where X, Y, and Z are integers")
                    return

            # Update the version in __init__.py
            with open("ciphercon/__init__.py", "r") as f:
                lines = f.readlines()
            with open("ciphercon/__init__.py", "w") as f:
                for line in lines:
                    if line.startswith("__version__"):
                        f.write(f'__version__ = "{new_version}"\n')
                    else:
                        f.write(line)

            # Update the version in the pyproject.toml
            with open("pyproject.toml", "r") as f:
                lines = f.readlines()
            with open("pyproject.toml", "w") as f:
                for line in lines:
                    if line.startswith("version ="):
                        f.write(f'version = "{new_version}"\n')
                    else:
                        f.write(line)
            
            # Update the version in the README.md
            with open("README.md", "r") as f:
                lines = f.readlines()
            with open("README.md", "w") as f:
                for i, line in enumerate(lines):
                    if i == 0:
                        f.write(f"# Ciphercon v{new_version}\n")
                    else:
                        f.write(line)

            print(f"Version updated to {new_version}")

if __name__ == "__main__":
    main()