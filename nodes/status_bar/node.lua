--RasPegacy v0.1
--Status Bar Child

gl.setup(720, 40)

node.alias("status_bar")

-- good place to display Raspberry Pi and/or Subaru logo(s)
RPi = resource.load_image("RPi_small.png")
Subaru = resource.load_imange("Subaru_Logo.png")

util.data_mapper{
    ["sbar/msg"] = function(new_msg)
        --print("MSG", new_msg)
        msg = new_msg
    end;
}


function node.render()
    gl.clear(0.23, 0.24, 0.26, 0.6)
    -- If I implement time based color swapping, will need to pass time here as well
    --if tonumber(clk) < 2000 then
    --    gl.clear(0, 0, 0, 0)
    --end

    -- Draw logo(s)
    RPi:draw(681, 1, 719, 41, 1)
<<<<<<< HEAD
=======
    Subaru:draw(610, 1, 678, 39, 1)
>>>>>>> a0d0a1fb4f44fcf1850dcc2f2d0bacbf3e7bf739

    -- Write status message
    font:write(10, 2, msg, 18, 1, 1, 1, 1)
    
end


