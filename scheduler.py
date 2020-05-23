'''
	Define a representation of a team that contains their team name, bye week, list of opponents
	and the number of opponents that are preset
'''
class Team():
	def __init__(self, name, bye, num_opponents):
		self.name = name
		self.bye = bye
		self.opponents = [None] * num_opponents
		self.known_opponents = 0
'''
	Load the data from the input file
'''
def read_initial_info(input_file):
	teams = list()
	byes = dict()
	team_names = list()
	with open(input_file, 'r') as f:
		num_teams = int(f.readline().strip())
		num_opponents = (num_teams - 1) * 2
		for i in range(num_teams):
			line = f.readline().strip()
			bye = int(line[line.rfind(" ") + 1:])
			name = line[ : line.rfind(" ")]
			teams.append(Team(name, bye, num_opponents))
			team_names.append(name)
			byes[name] = bye

		line = f.readline().strip()
		while line:
			matchup_week = int(line.split(" ")[-1])
			team1 = ""
			team2 = ""
			for team_name in team_names:
				if (line.find(team_name) != -1):
					if (team1 == ""):
						team1 = team_name
					else:
						team2 = team_name
			for i in range(num_teams):
				if teams[i].name == team1:
					teams[i].opponents[matchup_week - 1] = team2
					teams[i].known_opponents += 1
				elif teams[i].name == team2:
					teams[i].opponents[matchup_week - 1] = team1
					teams[i].known_opponents += 1
			line = f.readline().strip()
	return teams, byes

'''
	Output the teams to the terminal and potentially to a file
'''
def print_teams(teams, output_to_file):
	for name, team in teams.items():
		print(name, team.bye, team.opponents)

	if output_to_file:
		with open('output.txt', 'w+') as f:
			for name, team in teams.items():
				f.write(name + " " + str(team.bye) + " ")
				for opponent in team.opponents:
					f.write(opponent + " " )
				f.write('\n')
'''
	Determine if the given schedule is valid
'''
def valid_schedule(teams, byes, num_teams):
	# All teams must have a full 14 week schedule
	for team_name, team in teams.items():
		if None in team.opponents:
			return False
		# How many times will this team play every other team?
		opponent_count = dict()
		for opponent in team.opponents:
			if (opponent_count.get(opponent) == None):
				opponent_count[opponent] = 1
			else:
				opponent_count[opponent] += 1
			if opponent_count[opponent] > 2:
				return False
		# Check that they play once in the first half of the schedule
		opponents = set()
		for opponent in team.opponents[0: num_teams - 1]:
			opponents.add(opponent)
		if len(opponents) != num_teams - 1:
			return False
		# Check that they play once in the second half of the schedule
		opponents = set()
		for opponent in team.opponents[num_teams - 1:]:
			opponents.add(opponent)
		if len(opponents) != num_teams - 1:
			return False
		# Check that each team has exactly one free win
		myFreeWin = -1
		for idx, opponent in enumerate(team.opponents):
			print(opponent, byes[opponent])
			if byes[opponent] == idx + 1 and myFreeWin == -1:
				myFreeWin = idx
			elif byes[opponent] == idx + 1 and myFreeWin != -1:
				return False

	return True
'''
	Branch based on most known opponents
'''
def set_up_branching(teams):
	new_teams = dict()
	for idx, team in enumerate(teams):
		max_idx = idx
		for j in range(idx + 1, len(teams)):
			if teams[max_idx].known_opponents < teams[j].known_opponents:
				max_idx = j
		teams[idx], teams[max_idx] = teams[max_idx], teams[idx]

	for team in teams:
		new_teams[team.name] = team

	return new_teams

'''
	Backtracking implementation
'''
def recursively_generate_schedule(teams, byes, num_teams):
	# Base case - done when we have a schedule that meets the criteria
	if valid_schedule(teams, byes, num_teams):
		print_teams(teams, True)
		return True
	else:
		# Find a team that does not have an opponent scheduled yet
		for team_name, team in teams.items():
			for idx, opponent in enumerate(team.opponents):
				if opponent == None:
					# Avoid branches that clearly won't work with the current configuration
					for other_team in teams:
						# Has this team already been scheduled in the first num_teams weeks
						skip = False
						if idx < num_teams - 1:
							for recently_played in team.opponents[:num_teams - 1]:
								if recently_played == other_team:
									skip = True
						# Has this team already been scheduled in the last num_teams weeks
						else:
							for recently_played in team.opponents[num_teams - 1:]:
								if recently_played == other_team:
									skip = True
						# Would this be a free win?
						if idx == byes[other_team] - 1 and other_team != team_name:
							# Do they already have a free win?
							for week, recently_scheduled in enumerate(team.opponents):
								if recently_scheduled != None and byes[recently_scheduled] == week + 1:
									skip = True
						# This is potentially a valid opponent
						if not skip and teams[other_team].opponents[idx] == None and other_team != team_name:
							# Try with this opponent
							team.opponents[idx] = other_team
							teams[other_team].opponents[idx] = team_name
							# Next iteration
							done = recursively_generate_schedule(teams, byes, num_teams)
							# Return true to previous calls to exit
							if done:
								return True
							# Backtrack
							team.opponents[idx] = None
							teams[other_team].opponents[idx] = None

def main():
	init_teams, byes = read_initial_info("input.txt")
	init_teams = set_up_branching(init_teams)
	print_teams(init_teams, False)
	val = recursively_generate_schedule(init_teams, byes, len(init_teams))

if __name__ == '__main__':
	main()