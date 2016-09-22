--RasPegacy v0.1
--Basic Round Gauge Child

gl.setup(720, 260)

--local res = util.auto_loader()
local gothic = resource.load_font "Exo2.otf"
util.resource_loader{
    "needle.png",
}
local json = require "json"
util.file_watch("view.json", function(content)
    view = json.decode(content)
    cur = view.view
    steps = string.format(cur.top .. cur.mid .. cur.color .. '.png')
    res = resource.load_image(steps)
end)

local function gauge(conf)
    local x = conf.x
    local y = conf.y
    local size = conf.size or 240
    local value = 0
    local needle_rot = 0
    local function draw()
        --print("rotate:" .. tostring(needle_rot))
        res:draw(x-size/2, y-size/2, x+size/2, y+size/2)
        gl.pushMatrix()
        gl.translate(x+0.5, y+0.5)
        gl.rotate(-135 + 271 * needle_rot, 0, 0, 1)
        needle:draw(-size/2, -size/2, size/2, size/2,0.8)
        gl.popMatrix()
        gothic:write(x-12, y+(y/8), value, 18, 1, 1, 1, 1)
    end

    local function set(new_value)
        value = new_value
        --print("value:" .. tostring(value))
    end
    local function needle_set(new_value)
        needle_rot = new_value
    end

    return {
    draw = draw;
    set = set;
    needle_set = needle_set;
    }
end

node.alias("gauge")

local gauges = {
    boost = gauge{
        x = 120;
        y = 140;
        size = 240;
    };
    opress = gauge{
        x = 360;
        y = 140;
        size = 240;
    };
    val1 = gauge{
        x = 600;
        y = 140;
        size = 240;
    };
}

util.data_mapper{
    ["(.*)/set"] = function(gauge, value)
        gauges[gauge].set(tonumber(value))
    end;
    ["(.*)/needle_rot"] = function(gauge, needle_rot)
        gauges[gauge].needle_set(tonumber(needle_rot))
    end;
}

function node.render()
    gl.clear(0,0,0,0)
    -- Draw gauges
    for _, gauge in pairs(gauges) do
        gauge.draw()
    end   
    -- Static text
    gothic:write(93, 210, "BOOST", 16, 1, 1, 1, 1)
    gothic:write(30, 200, "-20", 14, 1, 1, 1, 1)
    gothic:write(192, 200, "20", 14, 1, 1, 1, 1)
    
    gothic:write(305, 210, "OIL PRESS", 16, 1, 1, 1, 1)
    gothic:write(270, 200, "0", 14, 1, 1, 1, 1)
    gothic:write(430, 200, "250", 14, 1, 1, 1, 1)
    
    gothic:write(560, 210, "VAL1", 16, 1, 1, 1, 1)
    gothic:write(515, 200, "0", 14, 1, 1, 1, 1)
    gothic:write(670, 200, "YES", 14, 1, 1, 1, 1)
    
end
