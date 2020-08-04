# Downloading CSV from Crowdtangle Mails
### Purpose
To download the CSV files that are sent from Crowdtangle.
### Pre-requisites
- Crowdtangle user's facebook-related e-mail address.
- Python 3.7
### Setup
- You can install required setups from pip;

    ``` commandline
    $ pip install -r requirements.txt
    ```
### Docker Setup

- Build the docker image

    ```
    docker build --tag csvdatadownload:latest .
    ```

- To try it:

    ```
    docker run -d --name csvdatadownload -v /home/dev1/ftp:/data/ftp csvdatadownload:latest
    ```

- Remove container:

    ```
    docker rm -f csvdatadownload
    ```

- Build Crone Docker Container

    ```
    docker create --name csvdatadownload --shm-size=2g -v /home/dev1/ftp:/app/ftp csvdatadownload:latest

    docker start csvdatadownload

    ```

- To view the logs of a Docker container in real time, use the following command:

    ```
    docker logs -f csvdatadownload
    ```

### Usage
- You can fill the " XXX " parts in the config.JSON file and you are good to go.

### Output
- Program does not exit automatically for now, you can terminate after the program stops saving files.

### Known Issues
* Download path must not include any special characters and should be written in English.
- Please log in with a Microsoft account, like Outlook or Hotmail.