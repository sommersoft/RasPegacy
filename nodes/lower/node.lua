--RasPegacy v0.1
--Lower Child
--Extra Info: AFR, Coolant Temp, etc.

gl.setup(720, 140)

node.alias("lower")

local font = resource.load_font("Exo2.otf")
local cool = "--"
local tps = "--"
local maf = "--"

util.data_mapper{
    ["set/coolant"] = function(new_cool)
        cool = tostring(new_cool)
        --print("cool", cool)
    end;
    ["set/tps"] = function(new_tps)
        tps = tostring(new_tps)
        --print("tps", tps)
    end;
    ["set/maf"] = function(new_maf)
        maf = tostring(new_maf)
        --print("maf", maf)
    end;
    ["set/intake"] = function(new_intake)
        intake = tostring(new_intake)
        --print("maf", maf)
    end;
    ["set/calc_load"] = function(new_load)
        calc_load = tostring(new_load)
        --print("maf", maf)
    end;
}

function node.render()
    gl.clear(0, 0, 0, 1)
    -- If I implement time based color swapping, will need to pass time here as well
    --if tonumber(clk) < 2000 then
    --    gl.clear(0, 0, 0, 0)
    --end

    -- Write status message
    font:write(30, 15, "COOLANT TEMP: " .. cool, 20, 1, 1, 1, 1)
    font:write(250, 15, "MAF: " .. maf, 20, 1, 1, 1, 1)
    font:write(420, 15, "THROTTLE POS: " .. tps, 20, 1, 1, 1, 1)
    
    font:write(30, 45, "INTAKE AIR TEMP: " .. intake, 20, 1, 1, 1, 1)
    font:write(280, 45, "CALCULATED LOAD: " .. calc_load, 20, 1, 1, 1, 1)
    
    
end
