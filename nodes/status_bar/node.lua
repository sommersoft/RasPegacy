--RasPegacy v0.1
--Status Bar Child

gl.setup(720, 40)

node.alias("status_bar")

-- good place to display Raspberry Pi and/or Subaru logo(s)
--title = resource.load_image("title.png")

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
    --title:draw(x, y, WIDTH, HEIGHT, 1)

    -- Write status message
    font:write(10, 2, msg, 18, 1, 1, 1, 1)
    
end


