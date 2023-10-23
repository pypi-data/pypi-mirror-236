import boto3
import os
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class HistoryReader:
    """
    Reads poker history files from the bucket
    """
    def __init__(self):
        self.s3 = boto3.resource(
            's3',
            region_name=os.environ.get("DO_REGION").strip(),
            endpoint_url=os.environ.get("DO_ENDPOINT").strip(),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID").strip(),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY").strip()
        )
        self.bucket = self.s3.Bucket("manggy-poker")

    @staticmethod
    def floatify(txt_num: str) -> float:
        """
        Transforms any written str number into a float
        :param txt_num: number to transform
        :return: float number
        """
        try:
            return float(txt_num.replace(",", "."))
        except TypeError:
            return float(0)
        except AttributeError:
            return float(0)
        except ValueError:
            return float(0)

    @staticmethod
    def extract_game_type(hand_txt: str) -> dict:
        """
        Extract the type of the game (Tournament or CashGame).
        """
        if "Tournament" in hand_txt:
            game_type = "Tournament"
        elif "CashGame" in hand_txt:
            game_type = "CashGame"
        else:
            game_type = "Unknown"
        return {"Gametype": game_type}

    def extract_players(self, hand_txt: str) -> dict:
        """
        Extract player information from a raw poker hand history and return as a dictionary.

        Parameters:
            hand_txt (str): The hand history as a string.

        Returns:
            dict: A dictionary containing player information (seat, pseudo, stack, and bounty if available).
        """
        # Initialize an empty dictionary to store the player information
        players_info = {}
        # Regex pattern to capture seat number, pseudo, stack, and optional bounty
        pattern = r"Seat (\d+): ([\w\s.\-&]{3,12}) \((\d+)(?:, ([\d\.]+[€$]))?"
        # Find all matching player information using the regex pattern
        matches = re.findall(pattern, hand_txt)
        # Populate the players_info dictionary from the matches
        for match in matches:
            seat, pseudo, stack, bounty = match
            bounty = bounty.replace("€", "").replace("$", "") if bounty else None
            players_info[int(seat)] = {
                "seat": int(seat),
                "pseudo": pseudo,
                "stack": self.floatify(stack),
                "bounty": self.floatify(bounty)
            }
        return players_info

    def extract_posting(self, hand_txt: str) -> list:
        """
        Extract blinds and antes posted information from a  poker hand history and return as a dictionary.

        Parameters:
            hand_txt (str): The raw poker hand history as a string.

        Returns:
            list: A dictionary containing blinds and antes information.
        """
        # Initialize an empty dictionary to store blinds and antes information
        blinds_antes_info = []
        # Regex pattern to capture blinds and antes posted by players
        blinds_pattern = r"(\n[\w\s\-&.]{3,12})\s+posts\s+(small blind|big blind|ante)\s+([\d.,]+)"
        # Find all matching blinds and antes information using the regex pattern
        matches = re.findall(blinds_pattern, hand_txt)
        # Populate the blinds_antes_info dictionary from the matches
        for match in matches:
            pseudo, blind_type, amount = match
            blinds_antes_info.append({
                "pseudo": pseudo.strip(),
                "amount": self.floatify(amount),
                "blind_type": blind_type
            })
        return blinds_antes_info

    def extract_buyin(self, hand_txt: str) -> dict:
        """
        Extract the buy-in and rake information.
        """
        ko_buyin_match = re.search(r"buyIn: ([\d.,]+)€ \+ ([\d.,]+)€ \+ ([\d.,]+)€", hand_txt)
        buyin_match = re.search(r"buyIn: ([\d.,]+)€ \+ ([\d.,]+)€", hand_txt)
        freeroll_match = re.search(r"buyIn: Free", hand_txt)
        if ko_buyin_match:
            buyin, ko, rake = ko_buyin_match.group(1), ko_buyin_match.group(2), ko_buyin_match.group(3)
        elif buyin_match:
            buyin, rake = buyin_match.group(1), buyin_match.group(2)
            ko = None
        elif freeroll_match:
            buyin, ko, rake = 0, 0, 0
        else:
            buyin, ko, rake = None, None, None
        return {"Buyin": self.floatify(buyin), "ko": self.floatify(ko), "Rake": self.floatify(rake)}

    @staticmethod
    def extract_datetime(hand_txt: str) -> dict:
        """
        Extract the datetime information.
        """
        datetime_match = re.search(r"- (\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) UTC", hand_txt)
        dt = datetime.strptime(datetime_match.group(1), "%Y/%m/%d %H:%M:%S")
        return {"Datetime": dt}

    def extract_blinds(self, hand_txt: str) -> dict:
        """
        Extract the blind levels and ante.
        """
        tour_blinds_match = re.search(r"\((\d+)/(\d+)/(\d+)\)", hand_txt)
        other_blinds_match = re.search(r"\(([\d€.]+)/([\d€.]+)\)", hand_txt)
        if tour_blinds_match:
            ante, sb, bb = tour_blinds_match.group(1), tour_blinds_match.group(2), tour_blinds_match.group(3)
        elif other_blinds_match:
            sb, bb = other_blinds_match.group(1).replace("€", ""), other_blinds_match.group(2).replace("€", "")
            ante = 0
        else:
            ante, sb, bb = None, None, None
        return {"Ante": self.floatify(ante), "SB": self.floatify(sb), "BB": self.floatify(bb)}

    @staticmethod
    def extract_level(hand_txt: str) -> dict:
        """
        Extract the level information.
        """
        level_match = re.search(r"level: (\d+)", hand_txt)
        if level_match:
            return {"Level": int(level_match.group(1))}
        else:
            return {"Level": 0}

    @staticmethod
    def extract_max_players(hand_txt: str) -> dict:
        """
        Extract the max players at the table.
        """
        table_match = re.search(r"(\d+)-max", hand_txt)
        return {"max_players": int(table_match.group(1))}

    @staticmethod
    def extract_button_seat(hand_txt: str) -> dict:
        """
        Extract the button seat information.
        """
        button_match = re.search(r"Seat #(\d+) is the button", hand_txt)
        return {"Button": int(button_match.group(1))}

    @staticmethod
    def extract_table_name(hand_txt: str) -> dict:
        """
        Extract the table name information.
        """
        table_match = re.search(r"Table: '(.*)' ", hand_txt)
        return {"table_name": table_match.group(1)}

    @staticmethod
    def extract_hero_hand(hand_txt: str) -> dict:
        """
        Extract the hero's hand (hole cards) from a single poker hand text and return as a string.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            str: A string representing the hero's hand (hole cards).
        """
        # Regex pattern to capture hero's hand
        hero_hand_pattern = r"Dealt to ([\w\s.\-&]{3,12}) \[(\w\w) (\w\w)\]"
        # Find the match using the regex pattern
        hero_hand_match = re.search(hero_hand_pattern, hand_txt, re.UNICODE)
        hero, card1, card2 = hero_hand_match.groups()
        return {"Hero": hero, "Card1": card1, "Card2": card2}

    @staticmethod
    def extract_flop(hand_txt: str) -> dict:
        """
        Extract the cards on the Flop from a single poker hand text and return as a string.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            str: A string representing the cards on the Flop.
        """
        # Regex pattern to capture the Flop
        flop_pattern = r"\*\*\* FLOP \*\*\* \[(\w\w) (\w\w) (\w\w)\]"
        # Find the match using the regex pattern
        flop_match = re.search(flop_pattern, hand_txt, re.UNICODE)
        if flop_match:
            card1, card2, card3 = flop_match.groups()
        else:
            card1, card2, card3 = None, None, None
        return {"Flop1": card1, "Flop2": card2, "Flop3": card3}

    @staticmethod
    def extract_turn(hand_txt: str) -> dict:
        """
        Extract the card on the Turn from a single poker hand text and return as a string.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            dict: A dictionary representing the card on the Turn.
        """
        turn_pattern = r"\*\*\* TURN \*\*\* \[\w\w \w\w \w\w\]\[(\w\w)\]"
        turn_match = re.search(turn_pattern, hand_txt, re.UNICODE)
        if turn_match:
            card = turn_match.group(1)
        else:
            card = None
        return {"Turn": card}

    @staticmethod
    def extract_river(hand_txt: str) -> dict:
        """
        Extract the card on the River from a single poker hand text and return as a string.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            dict: A dictionary representing the card on the River.
        """
        river_pattern = r"\*\*\* RIVER \*\*\* \[\w\w \w\w \w\w \w\w\]\[(\w\w)\]"
        river_match = re.search(river_pattern, hand_txt, re.UNICODE)
        if river_match:
            card = river_match.group(1)
        else:
            card = None
        return {"River": card}

    def parse_actions(self, actions_txt: str) -> list:
        """
        Parse the actions text from a poker hand history for a specific street
        and return a list of dictionaries containing the actions.

        Parameters:
            actions_txt (str): The raw actions text for a specific street.

        Returns:
            list: A list of dictionaries, each representing an action.
        """
        # The list to hold the parsed actions
        parsed_actions = []
        # The value for 'amount' is optional, thus marked by '?'
        action_re = re.compile(
            r"\n(?P<pl_name>[\w\s\-&.]{3,12})\s+(?P<move>calls|bets|raises|folds|checks)(?: (?P<value>\d+))?")
        # Find all the matches using the regex pattern
        actions = action_re.findall(actions_txt)
        for action in actions:
            player, action_type, amount = action

            # Create a dictionary for this action
            action_dict = {
                'player': player.strip(),  # Removing any leading/trailing spaces
                'action': action_type,
                'amount': self.floatify(amount)
            }
            # Add this action to the list of parsed actions
            parsed_actions.append(action_dict)
        return parsed_actions

    def extract_actions(self, hand_txt: str):
        """
        Extract the actions information from a poker hand history and return as a nested dictionary.
        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            dict: A dictionary containing all the actions extracted from the poker hand history.
        """
        actions_dict = {}
        preflop_pattern = r"\*\*\*\sPRE-FLOP\s\*\*\*([\w\s.€-]+)"
        flop_pattern = r"\*\*\*\sFLOP\s\*\*\*\s\[[\w\s]+\]([\w\s.€-]+)"
        turn_pattern = r"\*\*\*\sTURN\s\*\*\*\s\[[\w\s]+\]\[[\w\s]+\]([\w\s.€-]+)"
        river_pattern = r"\*\*\*\sRIVER\s\*\*\*\s\[[\w\s]+\]\[[\w\s]+\]([\w\s.€-]+)"
        for pattern, street in zip([preflop_pattern, flop_pattern, turn_pattern, river_pattern],
                                   ['PreFlop', 'Flop', 'Turn', 'River']):
            actions_match = re.search(pattern, hand_txt, re.DOTALL)
            if actions_match:
                actions_txt = actions_match.group(1)
                actions_dict[street] = self.parse_actions(actions_txt)
            else:
                actions_dict[street] = []
        return actions_dict

    @staticmethod
    def extract_showdown(hand_txt: str) -> dict:
        """
        Extract the showdown information from a poker hand history.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            showdown_info: A dict of dictionaries, each containing the player's shown cards.
        """
        showdown_info = {}
        showdown_pattern = r"([\w\s.\-&]+)\s+shows\s+\[(\w\w) (\w\w)\]"
        showdown_matches = re.findall(showdown_pattern, hand_txt)
        for player, card1, card2 in showdown_matches:
            showdown_info[player.strip()] = {"Card1": card1, "Card2": card2}
        return showdown_info

    def extract_winners(self, hand_txt: str) -> dict:
        """
        Extract the winners information from a poker hand history and return it as a nested dictionary.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            dict: A nested dictionary with pl_names as keys, each containing a dictionary with the amount and pot type.
        """
        # Dictionary to hold the winners information
        winners_info = {}
        # Regex pattern to capture the winners
        winners_pattern = r"\n([\w\s.\-&]{3,12}) collected (\d+) from (pot|main pot|side pot \d+)"
        # Find all the matches using the regex pattern
        winners_matches = re.findall(winners_pattern, hand_txt)
        for winner, amount, pot_type in winners_matches:
            winners_info[winner] = {"amount": self.floatify(amount), "pot_type": pot_type}
        return winners_info

    @staticmethod
    def extract_hand_id(hand_txt: str) -> dict:
        """
        Extract the hand id information from a poker hand history.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            dict: A dictionary containing the hand id extracted from the poker hand history.
        """
        hand_id_match = re.search(r"HandId: #([\d\-]+)", hand_txt)
        return {"HandId": hand_id_match.group(1)}

    def parse_hand(self, hand_txt: str) -> dict:
        """
        Extract all information from a poker hand history and return as a dictionary.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            dict: A dictionary containing all the information extracted from the poker hand history.
        """
        hh_dict = {"HandId": self.extract_hand_id(hand_txt)["HandId"],
                   "Datetime": self.extract_datetime(hand_txt)["Datetime"],
                   "GameType": self.extract_game_type(hand_txt)["Gametype"],
                   "Buyins": self.extract_buyin(hand_txt),
                   "Blinds": self.extract_blinds(hand_txt),
                   "Level": self.extract_level(hand_txt)["Level"],
                   "MaxPlayers": self.extract_max_players(hand_txt)["max_players"],
                   "ButtonSeat": self.extract_button_seat(hand_txt)["Button"],
                   "TableName": self.extract_table_name(hand_txt)["table_name"],
                   "Players": self.extract_players(hand_txt),
                   "HeroHand": self.extract_hero_hand(hand_txt),
                   "Postings": self.extract_posting(hand_txt),
                   "Actions": self.extract_actions(hand_txt),
                   "Flop": self.extract_flop(hand_txt),
                   "Turn": self.extract_turn(hand_txt),
                   "River": self.extract_river(hand_txt),
                   "Showdown": self.extract_showdown(hand_txt),
                   "Winners": self.extract_winners(hand_txt)}
        return hh_dict

    def parse_history_from_key(self, key: str) -> dict:
        """
        Extract all information from a poker hand history and return as a dictionary.

        Parameters:
            key (str): The key of the poker hand history in the bucket.

        Returns:
            dict: A dictionary containing all the information extracted from the poker hand history.
        """
        history_object = self.bucket.Object(key).get()
        history_txt = history_object["Body"].read().decode("utf-8")
        return self.parse_hand(history_txt)
