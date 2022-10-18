from constants import PLAYERS, TEAMS
from statistics import mean
import re
import getpass


def clean_data(players):
    cleaned = []
    for player in players:
        fixed = {}
        fixed['name'] = player['name']
        fixed['height'] = int(player['height'].split(' ')[0])
        if player['experience'] == 'YES':
            fixed['experience'] = True
        else:
            fixed['experience'] = False
        fixed['guardians'] = re.split(' and ', player['guardians'])
        cleaned.append(fixed)
    return cleaned


def balance_teams(players, teams):
    experienced = player_experience(players, True)
    inexperienced = player_experience(players, False)

    num_players_team = len(players)  / len(teams)
    experienced_player_per_team = len(experienced) / len(teams)
    inexperienced_player_per_team = len(inexperienced) / len(teams)

    
    for counter in range(len(teams)):
        teams[counter - 1] = []
    
    balance_team_draft(experienced, teams, experienced_player_per_team)
    balance_team_draft(inexperienced, teams, num_players_team)

    return teams


def balance_team_draft(players, teams, limit_per_team):
    for counter in range(len(teams)):
        for player in players.copy():
            if len(teams[counter - 1]) < limit_per_team:
                teams[counter - 1].append(player)
                print(player['name'])
                players.remove(player)
            else:
                break
    return teams


def player_experience(players, boolean_value):
    filtered_player = []
    for player in players:
        if player['experience'] == boolean_value:
            filtered_player.append(player)
    return filtered_player


def display_menu():
    print("=== Menu ===\n".upper())
    print("A) Display Team Stats")
    print("B) Quit")
    return input("\nEnter an option: ")


def display_team_selection(teams):
    index = 1
    print("=== Teams ===\n".upper())
    for counter in range(len(teams)):
        print(f"{index}) {teams[counter]}")
        index += 1
    option = int(input("\nEnter an option: "))
    return option


def display_team_stats(players,team_name):
        print(f"=== {team_name} ===\n".upper() )

        # Total Players
        total_players = len(players)
        print(f"Total Players: {total_players}")

        # Total Experience vs Unexperienced
        total_experienced = 0
        total_inexperienced = 0

        for player in players:
            if player['experience'] == True:
                total_experienced +=1
            else:
                total_inexperienced +=1
        print(f"Total Experienced: {total_experienced}")
        print(f"Total Inexperienced: {total_inexperienced}")

        # Average Height
        height_list = []
        for player in players:
            height_list.append(player['height'])
        average_height = round(mean(height_list),2)
        print(f"Average Height: {average_height} inches")

        # Players
        print(f"\nPlayers:")
        player_list_display = ""
        players = sorted(players, key=lambda x:x['height']) # https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
        for player in players:
            player_list_display += player['name'] + ", "
        print(player_list_display[:-2])
    
        # Guardians
        print(f"\nGuardians:")
        guardian_list = set()
        guardian_list_display = ""
        for player in players:
            guardians = set(player['guardians'])
            guardian_list = set(guardian_list).union(guardians)

            # guardians.add(guardian)
        for guardian in guardian_list:
            guardian_list_display += guardian + ", "
        
        print(guardian_list_display[:-2])


def display_divider():
    print("\n"  +("-_" * 20)+"\n")


def display_continue():
    getpass.getpass("Press ENTER to continue...") # This is like an input but text is hidden


if __name__ == "__main__":
    sorted_teams = balance_teams(clean_data(PLAYERS), TEAMS.copy())
    while True:
        menu_choice = display_menu()
        
        if menu_choice.upper() == "A":
            try:
                display_divider()
                selected_team = display_team_selection(TEAMS) - 1
            except (ValueError) as err:
                display_divider()
                print(f"We ran into an issue. {err}. Please try again")
                continue
            try:
                display_divider()
                display_team_stats(sorted_teams[selected_team],TEAMS[selected_team])
            except (IndexError) as err:
                display_divider()
                print(f"We ran into an issue. {err}. Please try again")
                continue
        elif menu_choice.upper() == "B":
            break
        else:
            display_divider()
            print(f"Invalid Input! Please Try Again!")

        display_divider()
        display_continue()
        display_divider()