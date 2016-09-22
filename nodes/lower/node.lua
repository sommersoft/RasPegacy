--RasPegacy v0.1
--Status Bar Child
--Git is painful...

gl.setup(720, 140)

node.alias("lower")

local font = resource.load_font("Exo2.otf")

util.data_mapper{
    ["lower/msg"] = function(new_msg)
        --print("MSG", new_msg)
        if new_msg ~= nil then
            msg = new_msg
        else
            msg = " "
        end
    end;
}


function node.render()
    gl.clear(1, 1, 1, 1)
    -- If I implement time based color swapping, will need to pass time here as well
    --if tonumber(clk) < 2000 then
    --    gl.clear(0, 0, 0, 0)
    --end

    -- Write status message
    font:write(WIDTH/2, HEIGHT/2, "LOWER NODE", 20, 1, 1, 1, 1)
    
end
