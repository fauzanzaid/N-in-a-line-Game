class Config():
	
	"""
	----------------------------------------
	INSTRUCTIONS
	----------------------------------------
	== board_dimensions ==
	(num_of_rows, num_of_columns)
	
	You can make the  board as  large as you
	want. However, AI player will take a lot
	of time to caculate  moves if board size
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
	in  every  game. If 0, player H (Green)
	gets to play first. For  other  values,
	the  player is choosen  randomly before
	every new game.
	----------------------------------------

	"""

	board_dimensions				= (4,4)
	minimum_coins_aligned_to_win	= 3
	first							= 0
	precalc							= True
	rdmz							= True