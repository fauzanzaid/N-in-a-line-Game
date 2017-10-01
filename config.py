class Config():
	
	"""
	----------------------------------------
	INSTRUCTIONS
	----------------------------------------
	== board_dimensions ==
	(num_of_rows, num_of_columns)
	
	You can make the  board as  large as you
	want. However, AI player will take a lot
	of time to calculate moves if board size
	is greater  than 4 x 4. You can  make it
	larger to play  against  another  friend
	if you want without this problem.
	----------------------------------------
	== minimum_coins_aligned_to_win ==
	an integer

	If you  make it larger  than both of the
	dimensions, you will not be able to ever
	end the game with a win or loss.
	----------------------------------------
	== first ==
	an integer

	If 0, player M (Red) gets to play first
	in  every  game. If 1, player H (Green)
	gets to play first. For  other  values,
	the  player is choosen  randomly before
	every new game.
	----------------------------------------
	== precalc ==
	boolean

	If True,  games of dim 4 x 4 against AI,
	where M plays first (first = 0) will use
	precalculated values for first two moves
	by AI to significantly speed up gameplay
	----------------------------------------
	== rdmz ==
	boolean

	If False, AI chooses the first choice in
	the  array of  best  moves. If  True, AI
	will randomly  choose one  choice in the
	array of best moves. Makes for a more
	interesting gameplay!
	----------------------------------------

	"""

	board_dimensions				= (4,4)
	minimum_coins_aligned_to_win	= 3
	first							= 0
	precalc							= True
	rdmz							= True