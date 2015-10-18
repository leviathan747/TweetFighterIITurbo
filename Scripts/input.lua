rnd1 = {}
rnd2 = {}

function readFile(filename, t)
	io.input("C:\\Users\\Kyle Krynski\\Desktop\\snes9x-1.51-rerecording-v7-win32\\Input\\" .. filename)
	cmd1 = io.read("*all")

	if t == 1 then
		x = rnd1
	else
		x = rnd2
	end

	length = string.len(cmd1)
	z = 1
	for i=1,length, 3 do
		x[z] = string.sub(cmd1, i, i+2)
		z = z + 1
		--print(string.sub(x[i], 1, 1) .. ", " .. tonumber(string.sub(x[i], 2, 3)))
	end
end

readFile("in1.txt", 1)
readFile("in2.txt", 2)

j = 1
while rnd1[j] ~= nil do
	print(rnd1[j] .. ", " .. rnd2[j])
	j = j + 1
end