from requests import get, exceptions


BASE_API_URL = 'http://mush.com.br/api/player'


class MushMC:
    """
    Class to interact with the MushMC API.
    """

    def __init__(self, async_run: bool = False):
        """
        Initializes the API object.
        :param async_run: Whether to use asyncio or not.
        """

        self.async_run = async_run

    @staticmethod
    def get_api_response(url: str, retries: int = 3, timeout: int = 5) -> dict:
        """
        Gets the API response with network error handling.
        :param url: Formatted API URL.
        :param retries: Number of connection attempts.
        :param timeout: Connection timeout.
        :return: API data in JSON format.
        """

        while retries > 0:
            try:
                response = get(url, allow_redirects=True, timeout=timeout)
                response.raise_for_status()
                return response.json()
            except exceptions.RequestException:
                retries -= 1
        raise ConnectionError(f'Could not connect to "{url}".')

    class Player:
        """
        Class to represent a player in MushMC.
        """

        def __init__(self, nick_or_uuid: str, retries: int = 3, timeout: int = 5):
            """
            Initializes a player object.
            :param nick_or_uuid: Username or UUID of the player.
            :param retries: Number of connection attempts.
            :param timeout: Connection timeout.
            """

            self.raw_response = self._get_data(nick_or_uuid, retries, timeout)
            self._process_response()

        @staticmethod
        def _get_data(nick_or_uuid: str, retries: int, timeout: int) -> dict:
            """
            Gets raw player data from the API.
            :param nick_or_uuid: Username or UUID of the player.
            :param retries: Number of connection attempts.
            :param timeout: Connection timeout.
            :return: Raw API data in JSON format.
            """

            url = f'{BASE_API_URL}/{nick_or_uuid}'
            data = MushMC.get_api_response(url, retries, timeout)
            if not data['success'] or not data['response'].get('success', True):
                raise ValueError(f'"{nick_or_uuid}" has never been registered on MushMC.')
            return data['response']

        def _process_response(self):
            """
            Processes the API response and initializes the player's attributes.
            """

            self.first_login = self.raw_response.get('first_login')
            self.last_login = self.raw_response.get('last_login')
            self.is_online = self.raw_response.get('connected')
            self.discord = self.raw_response.get('discord')
            self.account = self.raw_response.get('account')
            self.rank = self.raw_response.get('rank')
            self.clan = self.raw_response.get('clan')
            if self.raw_response.get('stats'):
                self.raw_response['play_time'] = self.raw_response['stats'].pop('play_time')
            self.play_time = self.raw_response.get('play_time')

        def list_games(self) -> list:
            """
            Gets a list of the games in which the player has played.
            :return: List of game names.
            """

            return list(self.raw_response.get('stats', {}).keys())

        def get_game_stats(self, game: str) -> dict:
            """
            Gets the stats of a specific game played by the player.
            :param game: Name of the game.
            :return: Game data in JSON format.
            """
            return self.raw_response.get('stats', {}).get(game, None)
