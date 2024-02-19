

# My-DJ Web App

## Introduction
My-DJ enhances your Spotify listening experience by integrating with LangChain for advanced music queue management, allowing users to manage music playback, queue songs, control playback, and make natural language music requests through a web interface.

## Features
- **Spotify Integration**: Seamless integration with Spotify accounts for music playback.
- **Queue Management**: Intuitive addition of tracks to the playback queue.
- **Playback Controls**: Basic controls including play, pause, and skip.
- **Natural Language Music Requests**: LangChain integration interprets music requests made through a messaging interface.

## Getting Started

### Prerequisites
To run My-DJ, you need Python 3.6 or newer. All other dependencies are listed in the `requirements.txt` file and will be installed via pip.

### Installation
Clone or download this repository to your local machine. Then, in the project directory, install the required dependencies:

```bash
pip install -r requirements.txt
```

This command installs Flask for web server functionality, Requests for HTTP requests, LangChain for natural language processing, and other necessary libraries.

### Running the App
Start the web application by running:

```bash
python app.py
```

This will initiate a local web server on `http://localhost:3000`. Navigate to this URL in your web browser to access My-DJ.

## Usage
Log in with your Spotify account upon accessing My-DJ. Use the message box to enter song requests in natural language. The LangChain integration processes your requests, queuing the corresponding tracks. Use the available playback controls to manage your music.

## Contributing
Contributions to My-DJ are welcome! Please refer to the issue tracker for submitting bugs, feature suggestions, or pull requests.

## License
My-DJ is licensed under the MIT License.

## Acknowledgments
- **Spotify**: For the Web Playback SDK that enables web-based music playback.
- **Flask**: For the lightweight and efficient web framework.
- **LangChain**: For providing natural language processing capabilities.


