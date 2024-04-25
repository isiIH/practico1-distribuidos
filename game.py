import random

class Game:
    def __init__(self):
        # variables globales
        self.limit_players_per_room = 6
        self.limit_teams = 3
        self.max_score = 20
        self.min_value_dice = 1
        self.max_value_dice = 6

        # variables generales
        self.locked = False
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

        # asigna turnos
        self.game_rotations = list(self.teams.keys()).copy()
        random.shuffle(self.game_rotations)

        print(f'Comienza el equipo {self.game_rotations[self.team_turn]} :o')

    
    def roll_dice(self, client_id):
        if client_id not in self.teams[self.game_rotations[self.team_turn]]:
            # no es turno de el equipo del jugador
            return -1

        if client_id in self.roll_set:
            # jugador ya lanzo dado
            return -2
        
        if self.locked:
            # juego terminado
            return -3
        
        num = random.randint(self.min_value_dice, self.max_value_dice)
        self.roll_set.add(client_id)
        self.team_turn_score += num

        print(f'{self.usernames[client_id]} ha lanzado el dado!')

        if len(self.roll_set) == len(self.teams[self.game_rotations[self.team_turn]]):
            self.pass_turn()

        return num


    def pass_turn(self):
        team_turn_name = self.game_rotations[self.team_turn]  
        self.scores[team_turn_name] += self.team_turn_score   # actualiza puntajes

        self.roll_set.clear()           # limpia lanzamientos de dado
        self.team_turn_score = 0        # limpia puntaje de equipo de turno
        self.team_turn = (self.team_turn + 1) % len(self.teams)     # siguiente turno

        # un equipo ha ganado
        if self.scores[team_turn_name] >= self.max_score:
            self.locked = True
            print(f'Ha ganado el equipo {team_turn_name}!!!')

            return

        print(f'  -> SCORES = {self.scores}')
        print(f'Ahora es turno del equipo {self.game_rotations[self.team_turn]} :p')


    def team_exists(self, team_name):
        # verifica si el equipo existe
        return True if (self.teams.get(team_name, None) is not None) else False


    def team_has_space(self, team_name):
        # verifica que haya espacio en el equipo
        return len(self.teams[team_name]) < self.limit_players_per_room


    def join_player(self, client_id, username, team_name):
        if not self.team_exists(team_name):
            # equipo no existe, se crea
            self.create_team(team_name)
        
        elif not self.team_has_space(team_name):
            # equipo sin espacio, fallo
            return False
        
        self.usernames[client_id] = username
        self.teams[team_name].append(client_id)

        print(f'{username} se ha unido al equipo {team_name}!')

    
    def create_team(self, team_name):
        self.teams[team_name] = []     # añade equipo
        self.scores[team_name] = 0     # inicializa puntaje a 0
        self.game_rotations.append(team_name)     # añade equipo a lista de turnos

        print(f'Bienvenido equipo {team_name}')

    
    def leave_player(self, client_id):
        # quita jugador del equipo
        for team_name, team_list in self.teams.items():
            if client_id in team_list:
                self.teams[team_name].remove(client_id)

                #equipo vacio
                if len(self.teams[team_name]) == 0:
                    print(f'{self.usernames[client_id]} despawneo del equipo {team_name} :(')
                    self.remove_team(team_name)

                break

        self.usernames.pop(client_id)     # quita nombre de usuario

    def remove_team(self, team_name):
        self.teams.pop(team_name)
        self.game_rotations.remove(team_name)
        self.scores.pop(team_name)

        print(f'El equipo {team_name} fue destruido')

    
    def get_teams(self):
        return self.teams
    
    def get_scores(self):
        return self.scores


game = Game()

game.join_player(1, 'manquisi', 'mancos')
game.join_player(2, 'mankris', 'pros')
game.start_game()
game.roll_dice(1)
game.roll_dice(2)
game.roll_dice(2)
game.roll_dice(1)
game.roll_dice(2)
game.roll_dice(2)
game.roll_dice(1)
game.roll_dice(2)
game.roll_dice(2)
game.roll_dice(1)
game.roll_dice(2)
game.roll_dice(2)
game.join_player(3, 'rata', 'gatos')
game.join_player(4, 'gata_xl', 'gatos')
game.roll_dice(1)
game.roll_dice(2)
game.roll_dice(1)
game.roll_dice(2)
game.roll_dice(3)
game.roll_dice(4)
game.roll_dice(3)
game.roll_dice(4)
game.leave_player(2)
game.roll_dice(1)
game.roll_dice(3)
game.roll_dice(4)
game.roll_dice(1)
game.roll_dice(3)
game.roll_dice(4)
game.roll_dice(1)
game.roll_dice(3)
game.roll_dice(4)