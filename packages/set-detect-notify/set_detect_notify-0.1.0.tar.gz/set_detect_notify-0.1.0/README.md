# Set, Detect, Notify  
Recognize faces/objects in (Wyze Cam) footage and send notifications to your phone (or other devices)

### Features  
- Recognize objects  
- Recognize faces  
- Send notifications to your phone (or other devices) using [ntfy](https://ntfy.sh/)  
- Optionally, run headless with Docker  
- Either use a webcam or an RTSP feed  
    - Use [mrlt8/docker-wyze-bridge](https://github.com/mrlt8/docker-wyze-bridge) to get RTSP feeds from Wyze Cams  


## Prerequisites  
### Poetry/Python  
- Camera, either a webcam or a Wyze Cam  
    - All RTSP feeds _should_ work, however.
- Python
- Poetry
### Docker
- A Wyze Cam  
    - Any other RTSP feed _should_ work, as mentioned above
- Python
- Poetry

## What's not required  
- A Wyze subscription  

## Usage    
### Installation  
1. Clone this repo with `git clone https://github.com/slashtechno/wyze-face-recognition.git`  
2. `cd` into the cloned repository  
3. Then, either install with [Poetry](https://python-poetry.org/) or run with Docker  

#### Docker  
1. Modify to `docker-compose.yml` to achieve desired configuration
2. Run in the background with `docker compose up -d

#### Poetry  
1. `poetry install`  
2. `poetry run -- set-detect-notify`  
### Configuration  
The following are some basic CLI options. Most flags have environment variable equivalents which can be helpful when using Docker. 

- For face recognition, put images of faces in subdirectories `./faces` (this can be changed with `--faces-directory`) 
    - Keep in mind, on the first run, face rec
- By default, notifications are sent for all objects. This can be changed with one or more occurrences of `--detect-object` to specify which objects to detect
    - Currently, all classes in the [COCO](https://cocodataset.org/) dataset can be detected
- To specify where notifications are sent, specify a [ntfy](https://ntfy.sh/) URL with `--ntfy-url`
- To configure the program when using Docker, edit `docker-compose.yml` and/or set environment variables.
- **For further information, use `--help`**

### How to uninstall  
- If you used Docker, run `docker-compose down --rmi all` in the cloned repository
- If you used Poetry, just delete the virtual environment and then the cloned repository