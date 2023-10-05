import os

def main():
    user = os.getlogin()
    extdrives = os.listdir(f'/media/{user}')

    if len(extdrives) == 1:
        [extdrive] = extdrives
        os.environ['MARDAQ_EXT_DRIVE'] = f"/media/{user}/{extdrive}"
        os.makedirs(f"/media/{user}/{extdrive}/data", exist_ok=True)
        os.makedirs(f"/media/{user}/{extdrive}/logs", exist_ok=True)

    elif len(extdrives) == 0:
        os.environ['MARDAQ_EXT_DRIVE'] = 'none'



if __name__ == "__main__":
    main()