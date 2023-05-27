import copy
import random


class MatchedMap:
    def __init__(self, names_list: list[str]) -> None:
        self.names_list: list[str] = names_list
        self.names: list[str] = []

        self.match_to_self: bool = False
        self.match_to_reciprocal: bool = False
        self.randomize_name_order: bool = False
        self.__forbidden_matches: dict[str, str] = {}

        self.__last_map: dict[str, str] = {}
        self.__validate_setup()

    def __validate_setup(self) -> None:
        """ Validate input and perform any setup.
        :returnval None:
        """
        if not self.names_list:
            raise ValueError('Provide a list of strings of names')

        duplicate_names: set[str] = set(
            [
                n
                for n
                in self.names_list
                if self.names_list.count(n) > 1
            ]
        )

        if duplicate_names:
            raise ValueError(
                'Duplicate name(s) in names_list (including ' \
                f'{", ".join(list(duplicate_names)[:3])})'
            )

        try:
            self.names = [str(n) for n in self.names_list]
        except ValueError:
            raise

    def __shuffle_names(self) -> None:
        """ Shuffle self.names in place.
        :returnval None:
        """
        random.shuffle(self.names)

    def __recursive_mm_gen(self, names: list[str],
                            current_mm: dict[str, str]) -> dict[str, str]:

        """ Recursively generate a new matched map, following the constraints
        established.
        :returnval dict[str, str]: The matched map, or an empty dict if no map
                is possible
        """
        if not names:
            return current_mm
        if not current_mm.keys():
            for name in names:
                current_mm[name] = ''

        for key_name in current_mm.keys():
            if current_mm[key_name]:
                continue
            for list_name in names:
                if list_name == key_name and not self.match_to_self:
                    continue
                if current_mm[list_name] == key_name and not self.match_to_reciprocal:
                    continue
                if (key_name in self.__forbidden_matches
                        and self.__forbidden_matches[key_name] == list_name):
                    continue

                new_mm: dict[str, str] = copy.deepcopy(current_mm)
                new_names: list[str] = copy.deepcopy(names)
                new_mm[key_name] = list_name
                new_names.remove(list_name)
                new_map: dict[str, str] = self.__recursive_mm_gen(new_names, new_mm)

                if new_map:
                    return new_map
                else:
                    continue
        return {}

    def set_forbidden_matches(self, forbidden_dict: dict[str, str]) -> None:
        """ Pass a dictionary with any forbidden matches.
        :param forbidden_dict dict[str, str]: A dictionary of forbidden matches
        :returnval None:
        """
        for k, v in forbidden_dict.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError(
                    'Invalid name (should be str): ' \
                    f'"{k if not isinstance(k, str) else v}"'
                )

            if k not in self.names or v not in self.names:
                raise ValueError(
                    f'Unrecognized name: "{k if k not in self.names else v}"'
                )

        self.__forbidden_matches = forbidden_dict

    def generate_matched_map(self) -> dict[str, str]:
        """ Use the list of names provided to generate a matched map.
        :returnval dict[str, str]: The generated map
        """
        if not self.names:
            return {}

        if self.randomize_name_order:
            self.__shuffle_names()

        matched_map: dict[str, str] = self.__recursive_mm_gen(self.names, {})

        if not matched_map:
            raise ValueError('Cannot generate map')

        self.__last_map = matched_map

        return self.__last_map

    def get_last_map(self) -> dict[str, str]:
        """ Retrieve the last successful map generated.
        :returnval dict[str, str]: The last map successfully generated
        """
        return self.__last_map


if __name__ == '__main__':
    names: list[str] = [
        'tristana',
        'jax',
        'lulu',
        'garen',
        'fiora',
        'zed',
        'twitch',
        'janna',
        'nami',
        'lux',
        'renekton',
    ]

    forbidden: dict[str, str] = {
        'tristana': 'jax',
        'jax': 'lulu',
        'lulu': 'tristana',
        'garen': 'fiora',
        'fiora': 'zed',
        'zed': 'garen',
        'twitch': 'janna',
        'janna': 'nami',
        'nami': 'lux',
        'lux': 'renekton',
        'renekton': 'twitch',
    }

    mapper: MatchedMap = MatchedMap(names)
    mapper.set_forbidden_matches(forbidden)
    mapper.randomize_name_order = True
    # mapper.match_to_reciprocal = True
    matched_map: dict[str, str] = mapper.generate_matched_map()

    print(matched_map)
