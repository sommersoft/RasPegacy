--RasPegacy v0.1
--Status Bar Child
--Git is painful...

gl.setup(720, 40)

node.alias("status_bar")

-- good place to display Raspberry Pi and/or Subaru logo(s)
bg = resource.load_image("bg_bottom.png")
RPi = resource.load_image("RPi_small.png")
Subaru = resource.load_image("Subaru_Logo.png")

local font = resource.load_font("Exo2.otf")

local msg = " "
util.data_mapper{
    ["sbar/msg"] = function(new_msg)
        --print("MSG", new_msg)
        msg = new_msg
    end;
}


function node.render()
    gl.clear(0, 0, 0, 1)
    -- If I implement time based color swapping, will need to pass time here as well
    --if tonumber(clk) < 2000 then
    --    gl.clear(0, 0, 0, 0)
    --end

    -- Draw background and logo(s)
    bg:draw(0, 0, 720, 40, 1)
    RPi:draw(681, 1, 719, 39, 1)
    Subaru:draw(608, 1, 676, 39, 1)

    -- Write status message
    if msg then
        font:write(10, 2, msg, 18, 1, 1, 1, 1)
    end
    
end


