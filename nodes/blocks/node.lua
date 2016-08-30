--RasPegacy v0.1
--GL Blocks Gauge Child

gl.setup(720, 446)

local font = resource.load_font "Exo2.otf"
util.resource_loader{
    "black.png",
    "yellow.png",
    "red.png",
}

local function block(conf)
    local x = conf.x
    local y = conf.y
    local size = conf.size or 240
    local nam = conf.nam
    local value = 0
    local pct = 0
    local function draw()
        local new_value = string.format('%s', tostring(value * 100))
        -- Figure out the percentage of each value to determine which color block to display
        -- Max boost: 17.5psi, Max Opressure: 105, Max Val1: 100
        if nam == "bst" then
            --print "BOOOOOOSTTTT!!!!!!"
            pct = value / 17.5
            new_value = tostring(value)
        else
            pct = value
            new_value = string.format('%s', tostring(value * 100))
        end
        if pct < 0.6 then
            --black background
            --local black = resource.load_image("black.png")
            black:draw(x-size/2, y-size/2, x+size/2, y+size/2)
            --black:dispose()
        elseif pct > 0.6 then
            if pct < 0.8 then
                --yellow background
                --local yellow = resource.load_image("yellow.png")
                yellow:draw(x-size/2, y-size/2, x+size/2, y+size/2)
                --yellow:dispose()
            else
                --red background
                --local red = resource.load_image("red.png")
                red:draw(x-size/2, y-size/2, x+size/2, y+size/2)
                --red:dispose()
            end
        end
        font:write(x-size/4, y-size/8, string.sub(new_value, 0, 5), 52, 1, 1, 1, 1)
    end

    local function set(new_value)
        value = new_value
    end

    return {
        draw = draw;
        set = set;
    }
end

node.alias("blocks")

local blocks = {
    boost = block{
        x = 119;
        y = 200;
        size = 240;
        nam = "bst";
    };
    opress = block{
        x = 361;
        y = 200;
        size = 240;
        nam = "oprs";
    };
    val1 = block{
        x = 602;
        y = 200;
        size = 240;
        nam = "v1"
    };
}

util.data_mapper{
    ["(.*)/set"] = function(block, value)
        blocks[block].set(tonumber(value))
    end
}

function node.render()
    gl.clear(0,0,0,0)
    font:write(80, 20, "BOOST", 20, 1, 1, 1, 1)
    font:write(290, 20, "OIL PRESSURE", 20, 1, 1, 1, 1)
    font:write(550, 20, "VAL1", 20, 1, 1, 1, 1)
    for i, block in pairs(blocks) do
        block.draw(i)
    end    
end


