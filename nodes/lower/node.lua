--RasPegacy v0.1
--Lower Child
--Extra Info: AFR, Coolant Temp, etc.

gl.setup(720, 140)

node.alias("lower")

local font = resource.load_font("Exo2.otf")

util.data_mapper{
    ["lower/coolant"] = function(new_cool)
        --print("MSG", new_msg)
        if new_cool ~= nil then
            cool = tostring(new_cool)
        else
            cool = " "
        end
    end;
    ["lower/tps"] = function(new_tps)
        --print("MSG", new_msg)
        if new_tps ~= nil then
            tps = tostring(new_tps)
        else
            tps = " "
        end
    end;
    ["lower/maf"] = function(new_maf)
        --print("MSG", new_msg)
        if new_maf ~= nil then
            maf = tostring(new_maf)
        else
            maf = " "
        end
    end;
}

function node.render()
    gl.clear(0, 0, 0, 1)
    -- If I implement time based color swapping, will need to pass time here as well
    --if tonumber(clk) < 2000 then
    --    gl.clear(0, 0, 0, 0)
    --end

    -- Write status message
    font:write(30, 20, "COOLANT TEMP: " + cool, 20, 1, 1, 1, 1)
    font:write(80, 20, "MAF: " + maf, 20, 1, 1, 1, 1)
    font:write(130, 20, "THROTTLE POS: " + tps, 20, 1, 1, 1, 1)
    
end
