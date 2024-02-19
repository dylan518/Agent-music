let player;
let isTrackPlaying = false;
var trackQueue = [];
let messages = [];
var token = globalConfig.token;

// Get the Spotify access token from the backend
window.onSpotifyWebPlaybackSDKReady = () => {
    player = new Spotify.Player({
        name: 'Web Playback SDK Quick Start Player',
        getOAuthToken: cb => { cb(token); }
    });

    // Error handling
    player.addListener('initialization_error', ({ message }) => { console.error(message); });
    player.addListener('authentication_error', ({ message }) => { console.error(message); });
    player.addListener('account_error', ({ message }) => { console.error(message); });
    player.addListener('playback_error', ({ message }) => { console.error(message); });
    player.addListener('player_state_changed', state => {
        if (!state) {
            console.log('Player state is not available.');
            return;
        }

        // Check if the track is paused and the position is at the end of the track's duration
        const isTrackEnded = state.paused && (state.position === 0 || state.duration - state.position < 3000); // 3 seconds threshold

        // If the track ended, play the next track in the queue
        if (isTrackEnded && !state.loading) {
            console.log('Track has ended, playing next in queue.');
            isTrackPlaying = false;
            playNextTrackInQueue();
        }
    });
    // Ready
    player.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
        // Store the device ID for later use if needed
        player._device_id = device_id;
    });

    player.connect();
};

// Play track by name
function playTrackByName(trackName) {
    fetch(`https://api.spotify.com/v1/search?q=${encodeURIComponent(trackName)}&type=track&limit=1`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.tracks && data.tracks.items.length > 0) {
                const trackUri = data.tracks.items[0].uri;
                isTrackPlaying = true;

                fetch(`https://api.spotify.com/v1/me/player/play?device_id=${player._device_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({ uris: [trackUri] }),
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                }).then(() => {
                    console.log(`Started playback of track ${trackName}`);
                    player.togglePlay();
                    // No need to call togglePlay since we're directly playing the track
                }).catch(e => console.error(e));
            } else {
                console.log(`No tracks found with the name "${trackName}"`);
                isTrackPlaying = false;
                playNextTrackInQueue(); // Try to play the next track if the current one fails
            }
        })
        .catch(error => {
            console.error('Error searching for track:', error);
            isTrackPlaying = false;
        });
}

// Add a track to the queue
function addToQueue(trackName) {
    trackQueue.push(trackName);
    if (!isTrackPlaying) {
        playNextTrackInQueue();
    }
}

// Define the control functions
function togglePlay() {
    if (player) {
        player.togglePlay().then(success => {
            console.log('Playback toggled', success);
        }).catch(e => console.log(e));
    }
}
// Update the playback state
function updatePlaybackState() {
    console.log('Updating playback state...');
    if (player && typeof player.getCurrentState === 'function') {
        player.getCurrentState().then(state => {
            if (!state) {
                console.log('Player state is not available.');
                return;
            }

            // Ensure you're accessing the correct properties
            const { current_track } = state.track_window;
            const position = state.position;
            const duration = state.duration;

            if (typeof position === 'undefined' || typeof duration === 'undefined') {
                console.log('Position or duration is undefined.');
                return; // Exit if either is undefined
            }

            // Update UI elements with the current track information
            document.getElementById('track-name').textContent = current_track.name;
            document.getElementById('artist-name').textContent = current_track.artists.map(artist => artist.name).join(', ');
            document.getElementById('album-cover').src = current_track.album.images[0].url;
        }).catch(error => {
            console.error('Error fetching player state:', error);
        });
    } else {
        console.log('Player is not initialized');
    }
}

//check playback state every second
setInterval(updatePlaybackState, 1000);
var updateStateInterval = setInterval(updatePlaybackState, 1000);


// Play the next track in the queue
function playNextTrackInQueue() {
    if (trackQueue.length > 0) {
        const nextTrackName = trackQueue.shift(); // Remove the first track name from the queue
        playTrackByName(nextTrackName);
        isTrackPlaying = true;
        displayQueue(); // Call this function to update the UI after modifying the queue
    } else {
        isTrackPlaying = false; // No more tracks to play
        console.log("Queue is empty.");
    }
}


// Display the queue
function displayQueue() {
    const queueElement = document.getElementById('trackQueue');
    queueElement.innerHTML = ''; // Clear the current display
    trackQueue.forEach(trackName => {
        const li = document.createElement('li');
        li.textContent = trackName; // Directly use the string
        queueElement.appendChild(li);
    });
}
// Update the queue and messages from the backend
function updateQueueFromBackend() {
    const queueJson = encodeURIComponent(JSON.stringify(trackQueue));
    const messagesJson = encodeURIComponent(JSON.stringify(messages));

    fetch(`/update_queue?queue=${queueJson}&messages=${messagesJson}`)
        .then(response => response.json())
        .then(data => {
            console.log('Response received:', data);
            const updatedQueue = data.updated_queue; // Access the updated queue

            // Map through the updatedQueue to extract only the 'name' property for each track
            trackQueue = updatedQueue.map(track => track.name);
            window.trackQueue = trackQueue; // Update the global queue
            displayQueue(); // Update the visual queue display with just the track names
            console.log('Updated Queue:', trackQueue);

            // Optionally, update messages and handle playback
            messages = data.messages; // Update messages if necessary
            console.log('Updated Messages:', messages);

            if (!isTrackPlaying && trackQueue.length > 0) {
                playNextTrackInQueue(); // Automatically start playing the updated queue
            }
        })
        .catch(error => console.error('Error updating queue:', error));
}

// Add a message to the queue and request an update
function addMessageAndRequestQueueUpdate() {
    // Get the user message
    const userMessage = document.getElementById('userMessage').value;
    if (!userMessage) {
        console.log("Please enter a message.");
        return;
    }

    // Add the message to the messages array
    messages.push(userMessage);



    // Update the queue based on the messages
    updateQueueFromBackend();

    document.getElementById('queueAndPlayer').classList.remove('hidden');


    // Clear the input field
    document.getElementById('userMessage').value = '';
}

