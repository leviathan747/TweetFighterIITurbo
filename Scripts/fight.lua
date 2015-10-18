framecount = 0
lastP1hit = 0
lastP1move = 0
lastP2hit = 0
lastP2move = 0

function p1move()
   x = {}
   if (framecount-lastP1move) > 0 and (lastP1move - lastP1hit) <= 50 then
      x["right"] = true
      print("P1 Moved\n")
      lastP1move = framecount
      return x
   elseif (framecount-lastP1hit) > 20 and (lastP1move - lastP1hit) > 50 then
      x["B"] = true
      print("P1 Punched\n")
      lastP1hit = framecount
      return x
   end
   return x
end

function p2move()
   x = {}
   if (framecount-lastP2move) > 0 and (lastP2move - lastP2hit) <= 50 then
      x["left"] = true
      print("P2 Moved\n")
      lastP2move = framecount
      return x
   elseif (framecount-lastP2hit) > 20 and (lastP2move - lastP2hit) > 50 then
      x["B"] = true
      print("P2 Punched\n")
      lastP2hit = framecount
      return x
   end
   return x
end

function fn()
   framecount = framecount + 1
   y = {}
   y = p1move()
   z = {}
   z = p2move()
   joypad.set(1, y)
   joypad.set(2, z)
end

function fn2()
   A = {}
   A["B"] = true
   A["down"] = true
   A["left"] = true
   B = {}
   B["right"] = true
   --joypad.set(1, B)
   if (framecount - lastP1hit) >= 2 then
      joypad.set(1, A)
      lastP1hit = framecount
      print("Hit")
   else
      --joypad.set(1, B)
      --print("Move")
   end
   print("done")
   framecount = framecount + 1
end

count = 0
function fn3()
   A = {}
   A["right"] = true
   if count == 180 then
      A["A"] = true
      count = 0
   end
   joypad.set(1, A)
   count = count + 1
   framecount = framecount + 1
end

emu.registerbefore(fn3)