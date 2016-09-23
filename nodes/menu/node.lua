--RasPegacy v0.1
--Menu Child

gl.setup(720, 40)

node.alias("menu")

bg = resource.load_image("bg_top.png")
title = resource.load_image("title.png")

local json = require "json"
local font = resource.load_font("Exo2.otf")
util.file_watch("menu.json", function(content)
    menu = json.decode(content)
    cur = menu.current
    steps = string.format(cur.step1 .. cur.step2 .. cur.step3 .. '.png')
    menpic = resource.load_image(steps)
end)

local clk = "00:00"
local tmp = "0"
util.data_mapper{
    ["clock/clk"] = function(new_clk)
        --print("CLK", new_clk)
        if new_clk ~= nil then
            clk = new_clk
        else
            clk = "--"
        end
    end;
    ["clock/tmp"] = function(new_tmp)
        --print("TMP", new_tmp)
        if new_tmp ~= nil then
            tmp = new_tmp
        else
            tmp = "--"
        end
    end;
}


function node.render()
    gl.clear(0, 0, 0, 1)
    --if tonumber(clk) < 2000 then
    --    gl.clear(0, 0, 0, 0)
    --end

    -- Load menu background
    bg:draw(0, 0, 720, 40, 1)
    -- Load Title (alpha determined by if menu is active [json "current:step1"]
    title:draw(241, 0, WIDTH, HEIGHT, 1)

    -- Load menu items (menu selection based on json file "current";file is selected by [steps]
    -- which corresponds to the file names [i.e. "000.png" is the top most menu level)
    menpic:draw(0, 0, 240, 40)

    -- Draw clock
    font:write(WIDTH - 50, 2, clk, 18, 1, 1, 1, 1)
    font:write(WIDTH - 190, 2, 'Out: XX°  In: ' .. tmp .. '°', 18, 1, 1, 1, 1)
    
end
