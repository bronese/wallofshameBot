WallOfShameBot

This project is a Discord bot that interacts with the MusicBrainz API to fetch and display information about music artists and genres. It uses the py-cord library to interact with the Discord API and the requests library to interact with the MusicBrainz API.
Features

- Spotify Integration: The bot can fetch and display information about the music that server members are currently listening to on Spotify. This includes the song title, artist, album, duration, and a link to the song on Spotify.

- MusicBrainz Integration: The bot can fetch and display information about artists and genres from the MusicBrainz database.

- Customizable Genres and Artists: Server administrators can customize the genres and artists that the bot fetches information about.

- Docker Support: The bot can be deployed using Docker.
Setup

1. Clone the repository.
2. Install the required dependencies by running pip install -r requirements.txt.
3. Set up the bot on the Discord developer portal and get your bot token.
4. Replace the placeholder token in config.ini with your bot token.
5. Run main.py to start the bot.
Usage

The bot has several commands that server members can use:

- ?genre: Opens a modal where server administrators can input custom genres.
- ?custom_artists: Opens a modal where server administrators can input custom artists.
- ?personal: Displays information about the music that the command user is currently listening to on Spotify.
- ?serverwide: Displays information about the music that all server members are currently listening to on Spotify.
Docker Deployment

The bot can be deployed using Docker. A Dockerfile is included in the repository. To build and run the Docker image, use the following commands:

GitHub Actions

The repository includes several GitHub Actions workflows for continuous integration:

- update-config.yml: Updates the bot token in config.ini whenever changes are pushed to the main branch.
- pytest.yml: Runs unit tests whenever changes are pushed to the test branch.
- docker-image.yml: Builds and pushes a Docker image whenever the update-config.yml workflow completes or a pull request is made to the main branch.
Contributing

Contributions are welcome. Please open an issue to discuss your proposed changes before making a pull request.
License

This project is licensed under the MIT License.
