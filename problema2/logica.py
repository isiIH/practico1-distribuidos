import random
from dotenv import load_dotenv
import os
load_dotenv()

class Game:
    def __init__(self):
        # variables globales
        self.num_juego = 1
        self.limit_players_per_room = int(os.getenv("NPLAYERS"))
        self.limit_teams = int(os.getenv("NTEAMS"))
        self.max_score = int(os.getenv("NROWS"))
        self.min_value_dice = int(os.getenv("MIN"))
        self.max_value_dice = int(os.getenv("MAX"))

        # variables generales
        self.locked = False
        self.gamemode = 0 #0 -> Join | 1 -> Play
        self.teams = {}
        self.usernames = {}
        self.scores = {}
        self.game_rotations = []

        # variables equipo de turno
        self.roll_set = set()
        self.team_turn = 0
        self.team_turn_score = 0


    def start_game(self):
        assert len(self.teams.keys()) >= 2

        self.gamemode = 1

        # asigna turnos
        self.game_rotations = list(self.teams.keys()).copy()
        random.shuffle(self.game_rotations)
        
        print(f'Team turn: {self.team_turn}')
        print(f'Comienza el equipo {self.game_rotations[self.team_turn]} :o')

    
    def roll_dice(self, client_id):
        if client_id not in self.teams[self.game_rotations[self.team_turn]]:
            # no es turno de el equipo del jugador
            return -1,False

        if client_id in self.roll_set:
            # jugador ya lanzo dado
            return -2,False
        
        if self.locked:
            # juego terminado
            return -3,False
        
        num = random.randint(self.min_value_dice, self.max_value_dice)
        self.roll_set.add(client_id)
        self.team_turn_score += num

        print(f'{self.usernames[client_id]} ha lanzado el dado!')
        print(f"Resultado: {num}")

        if self.check_if_pass_turn():
            self.pass_turn()
            return num, True

        return num, False
    

    def check_if_pass_turn(self):
        if len(self.roll_set) >= len(self.teams[self.game_rotations[self.team_turn]]):
            return True
        return False


    def pass_turn(self):
        team_turn_name = self.game_rotations[self.team_turn]  
        self.scores[team_turn_name] += self.team_turn_score   # actualiza puntajes


        # un equipo ha ganado
        if self.scores[team_turn_name] >= self.max_score:
            self.locked = True
            print(f'Ha ganado el equipo {team_turn_name}!!!')

            return
        
        self.roll_set.clear()           # limpia lanzamientos de dado
        self.team_turn_score = 0        # limpia puntaje de equipo de turno
        self.team_turn = (self.team_turn + 1) % len(self.teams)     # siguiente turno

        print(f'  -> SCORES = {self.scores}')
        print(f'Ahora es turno del equipo {self.game_rotations[self.team_turn]} :p')


    def team_exists(self, team_name):
        # verifica si el equipo existe
        return True if (self.teams.get(team_name, None) is not None) else False


    def team_has_space(self, team_name):
        # verifica que haya espacio en el equipo
        return len(self.teams[team_name]) < self.limit_players_per_room


    def view_limit(self, team_name):
        if team_name not in self.teams.keys() and len(self.get_teams().keys()) >= self.limit_teams:
            print(f"No se pueden ingresar más equipos! Límite {self.limit_teams}")
            return False
        
        if team_name in self.teams.keys() and not self.team_has_space(team_name):
            # equipo sin espacio, fallo
            print(f"No se pueden ingresar más jugadores! Límite {self.limit_players_per_room}")
            return False

        return True
    
    def join_player(self, client_id, username, team_name):
        if not self.team_exists(team_name):
            # equipo no existe, se crea
            self.create_team(team_name)
        
        self.usernames[client_id] = username
        self.teams[team_name].append(client_id)

        print(f'{username} se ha unido al equipo {team_name}!')

    
    def create_team(self, team_name):
        self.teams[team_name] = []     # añade equipo
        self.scores[team_name] = 0     # inicializa puntaje a 0
        self.game_rotations.append(team_name)     # añade equipo a lista de turnos

        print(f'Bienvenido equipo {team_name}')

    
    def leave_player(self, client_id):
        if client_id not in self.usernames.keys():
            print("No existe jugador con este id: ", client_id)
            return False

        # quita jugador del equipo
        for team_name, team_list in self.teams.items():
            if client_id in team_list:
                self.teams[team_name].remove(client_id)

                print(f'{self.usernames[client_id]} despawneo del equipo {team_name} :(')
                self.usernames.pop(client_id)

                #equipo vacio
                if len(self.teams[team_name]) == 0:
                    self.remove_team(team_name)

                # revisa si se debe pasar turno
                if team_name == self.game_rotations[self.team_turn]:
                    self.roll_set.remove(client_id)
                    if self.check_if_pass_turn():
                        self.pass_turn()

                return True


    def remove_team(self, team_name):
        if self.game_rotations[self.team_turn] == team_name:
            self.team_turn = self.team_turn % (len(self.teams) - 1)     # siguiente turno

        self.teams.pop(team_name)
        self.game_rotations.remove(team_name)
        self.scores.pop(team_name)

        print(f'El equipo {team_name} fue destruido')


    def end_game(self):
        self.teams.clear()
        self.game_rotations.clear()
        self.scores.clear()
        self.usernames.clear()

        self.locked = False
        self.roll_set = set()
        self.team_turn = 0
        self.team_turn_score = 0
        self.gamemode = 0

        self.num_juego += 1

    
    def get_teams(self):
        return self.teams
    
    def get_scores(self):
        return self.scores


game = Game()
