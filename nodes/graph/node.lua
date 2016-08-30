--RasPegacy v0.1
--Graph Display Child

gl.setup(720, 446)

util.resource_loader{
    "boost.png",
    "opress.png",
    "gothic.ttf",
}

local lines = {}
local last = 0

function splitme(str)
    local splitted = {}
    last = 0
    for par in string.gmatch(str, "[^\n]") do
        splitted[#splitted + 1] = par
        last = last + 1
    end
    last = last - 1
    return splitted
end

util.file_watch("boost.txt", function(content)
    lines = splitme(content)
end)

function node.render()
    gl.clear(0.01,0,0.1,0.3)
    gothic:write(88, 10, "BOOST", 10, 1, 1, 1)
    gothic:write(268, 10,"OIL PRESSURE", 10, 1, 1, 1)
    boost:draw(10, 21, 200, 168)
    opress:draw(203, 21, 403, 168)
    gothic:write(10, 220, "Booost:", 10, 1, 1, 1)
    for i, line in ipairs(lines) do
        --print(tostring(line))
        if i == last then
            gothic:write(60, 220, line, 10, 1, 1, 1)
        end
    end
end
