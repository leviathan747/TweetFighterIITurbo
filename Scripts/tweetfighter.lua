startcount = 2500
gamecount = 0
p1movetime = 0
p2movetime = 0
p1burntime = 0
p2burntime = 0


--****************ROUND COMMANDS***************--
rnd1 = {}
rnd2 = {}
rnd3 = {}
roundNum = 1
attackNum = 1

--****************MOVE BUTTONS***************--

--Constants to make players move
movep1 = {}
movep1["right"] = true
movep2 = {}
movep2["left"] = true

--Constants for jabs
mid_jab_lite = {}
mid_jab_lite["Y"] = true
mid_jab_hard = {}
mid_jab_hard["X"] = true
low_jab_lite = {}
low_jab_lite["down"] = true
low_jab_lite["Y"] = true

--Constants for straight kicks
mid_kick_lite = {}
mid_kick_lite["B"] = true
mid_kick_hard = {}
mid_kick_hard["A"] = true
low_kick_lite = {}
low_kick_lite["down"] = true
low_kick_lite["B"] = true
low_kick_hard = {}
low_kick_hard["down"] = true
low_kick_hard["A"] = true

--Constants for spin kicks
mid_spin_kick = {}
mid_spin_kick["R"] = true
low_spin_kick = {}
low_spin_kick["down"] = true
low_spin_kick["R"] = true

--Constants for punches
mid_punch = {}
mid_punch["L"] = true
upper_cut = {}
upper_cut["down"] = true
upper_cut["L"] = true

--Constants for throw
throw = {}
throw["right"] = true
throw["A"] = true


--****************FUNCTION TO DETERMINE MOVES***************--
function setMoves()
	gamecount = emu.framecount()
	P1 = {}
	P2 = {}
	rnd = rnd1
	--Wait for movie to be ready
	if gamecount >= startcount then
		--When movie is set, get both characters in range fighting
		if gamecount < (startcount+15) then
                	P1 = movep1
			P2 = movep2
		else  --Now start taking in commands and executing
			--Check for the end of a round
			r,g,b = gui.getpixel(65, 40)
			if r < 240 then
				roundNum = roundNum + 1
				attackNum = 1
				startcount = gamecount + 150
				return
			end
			--print(r .. ", " .. g .. ", " .. b)
			
			--Check which round it is
			if roundNum == 2 then
				rnd = rnd2
			elseif roundNum == 3 then
				rnd = rnd3
			end
			--Figure out whose turn it is to attack
			if string.sub(rnd[attackNum], 1, 1) == "a" then    --Player 1 attacks
				
			else		--Player 2 attacks
				
			end

			--Choose move to execute
			
			attackNum = attackNum + 1
		end
		joypad.set(1, P1)
		joypad.set(2, P2)
        end
	--print(gamecount)
end


--****************FUNCTION TO DETERMINE MOVES***************--
function readFile(filename, t)
	io.input("C:\\Users\\Kyle Krynski\\Desktop\\snes9x-1.51-rerecording-v7-win32\\Input\\" .. filename)
	cmd1 = io.read("*all")
	if t == 1 then
		x = rnd1
	elseif t == 2 then
		x = rnd2
	else
		x = rnd3
	end
	length = string.len(cmd1)
	z = 1
	for i=1,length, 3 do
		x[z] = string.sub(cmd1, i, i+2)
		z = z + 1
	end
end


--****************MAIN PROGRAM AREA***************--
--Read each round input file
--readFile("rnd1.txt", 1)
--readFile("rnd2.txt", 2)
--readFile("rnd3.txt", 3)


--Start the listener
emu.registerbefore(setMoves)

