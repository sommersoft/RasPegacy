--RasPegacy v0.1
--Lower Child
--Extra Info: AFR, Coolant Temp, etc.

gl.setup(720, 140)

node.alias("lower")

local font = resource.load_font("Exo2.otf")

util.data_mapper{
    ["lower/coolant"] = function(new_cool)
        --print("MSG", new_msg)
        cool = tostring(new_cool)
    end;
    ["lower/tps"] = function(new_tps)
        --print("MSG", new_msg)
        tps = tostring(new_tps)
    end;
    ["lower/maf"] = function(new_maf)
        --print("MSG", new_msg)
        maf = tostring(new_maf)
    end;
}

function node.render()
    gl.clear(0, 0, 0, 1)
    -- If I implement time based color swapping, will need to pass time here as well
    --if tonumber(clk) < 2000 then
    --    gl.clear(0, 0, 0, 0)
    --end

    -- Write status message
    font:write(300, 10, "LOWER VALUES", 20, 1, 1, 1, 1)
    font:write(30, 30, "COOLANT TEMP: " .. cool, 20, 1, 1, 1, 1)
    font:write(80, 30, "MAF: " .. maf, 20, 1, 1, 1, 1)
    font:write(130, 30, "THROTTLE POS: " .. tps, 20, 1, 1, 1, 1)
    
end
