-- Roblox Player Locator GUI
-- For use in Roblox experiences you own / are authorized to develop.
-- Install: StarterPlayer > StarterPlayerScripts > LocalScript

local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer

local highlights = {}
local currentTarget = nil

local function make(className, props, parent)
    local obj = Instance.new(className)
    for key, value in pairs(props) do
        obj[key] = value
    end
    obj.Parent = parent
    return obj
end

local gui = make("ScreenGui", {
    Name = "PlayerLocatorGUI",
    ResetOnSpawn = false,
    IgnoreGuiInset = true,
}, LocalPlayer:WaitForChild("PlayerGui"))

local main = make("Frame", {
    Name = "Main",
    Size = UDim2.fromOffset(360, 330),
    Position = UDim2.new(0.5, -180, 0.5, -165),
    BackgroundColor3 = Color3.fromRGB(25, 25, 32),
    BorderSizePixel = 0,
}, gui)

make("UICorner", {CornerRadius = UDim.new(0, 12)}, main)

local title = make("TextLabel", {
    Size = UDim2.new(1, -50, 0, 45),
    Position = UDim2.fromOffset(15, 5),
    BackgroundTransparency = 1,
    Text = "Player Locator",
    TextColor3 = Color3.fromRGB(255, 255, 255),
    TextSize = 22,
    Font = Enum.Font.GothamBold,
    TextXAlignment = Enum.TextXAlignment.Left,
}, main)

local close = make("TextButton", {
    Size = UDim2.fromOffset(34, 34),
    Position = UDim2.new(1, -42, 0, 10),
    BackgroundColor3 = Color3.fromRGB(55, 55, 65),
    Text = "X",
    TextColor3 = Color3.fromRGB(255, 255, 255),
    TextSize = 16,
    Font = Enum.Font.GothamBold,
}, main)
make("UICorner", {CornerRadius = UDim.new(0, 8)}, close)

local search = make("TextBox", {
    Size = UDim2.new(1, -30, 0, 42),
    Position = UDim2.fromOffset(15, 58),
    BackgroundColor3 = Color3.fromRGB(40, 40, 50),
    PlaceholderText = "Enter username...",
    PlaceholderColor3 = Color3.fromRGB(160, 160, 170),
    Text = "",
    TextColor3 = Color3.fromRGB(255, 255, 255),
    TextSize = 16,
    Font = Enum.Font.Gotham,
    ClearTextOnFocus = false,
}, main)
make("UICorner", {CornerRadius = UDim.new(0, 8)}, search)

local status = make("TextLabel", {
    Size = UDim2.new(1, -30, 0, 32),
    Position = UDim2.fromOffset(15, 105),
    BackgroundTransparency = 1,
    Text = "Type a username, then press Locate.",
    TextColor3 = Color3.fromRGB(190, 190, 200),
    TextSize = 14,
    Font = Enum.Font.Gotham,
    TextXAlignment = Enum.TextXAlignment.Left,
}, main)

local locate = make("TextButton", {
    Size = UDim2.new(0.48, -5, 0, 42),
    Position = UDim2.fromOffset(15, 145),
    BackgroundColor3 = Color3.fromRGB(70, 120, 255),
    Text = "Locate",
    TextColor3 = Color3.fromRGB(255, 255, 255),
    TextSize = 16,
    Font = Enum.Font.GothamBold,
}, main)
make("UICorner", {CornerRadius = UDim.new(0, 8)}, locate)

local clear = make("TextButton", {
    Size = UDim2.new(0.48, -5, 0, 42),
    Position = UDim2.new(0.52, 0, 0, 145),
    BackgroundColor3 = Color3.fromRGB(55, 55, 65),
    Text = "Clear Highlight",
    TextColor3 = Color3.fromRGB(255, 255, 255),
    TextSize = 16,
    Font = Enum.Font.GothamBold,
}, main)
make("UICorner", {CornerRadius = UDim.new(0, 8)}, clear)

local refresh = make("TextButton", {
    Size = UDim2.new(1, -30, 0, 38),
    Position = UDim2.fromOffset(15, 198),
    BackgroundColor3 = Color3.fromRGB(45, 45, 55),
    Text = "Refresh Player List",
    TextColor3 = Color3.fromRGB(255, 255, 255),
    TextSize = 15,
    Font = Enum.Font.Gotham,
}, main)
make("UICorner", {CornerRadius = UDim.new(0, 8)}, refresh)

local list = make("ScrollingFrame", {
    Size = UDim2.new(1, -30, 0, 75),
    Position = UDim2.fromOffset(15, 245),
    BackgroundColor3 = Color3.fromRGB(32, 32, 40),
    BorderSizePixel = 0,
    ScrollBarThickness = 5,
    CanvasSize = UDim2.fromOffset(0, 0),
}, main)
make("UICorner", {CornerRadius = UDim.new(0, 8)}, list)
local layout = make("UIListLayout", {Padding = UDim.new(0, 3)}, list)

local function removeHighlight(player)
    if highlights[player] then
        highlights[player]:Destroy()
        highlights[player] = nil
    end
end

local function clearHighlights()
    for player, highlight in pairs(highlights) do
        highlight:Destroy()
        highlights[player] = nil
    end
    currentTarget = nil
end

local function highlightPlayer(player)
    clearHighlights()
    if not player.Character then
        status.Text = "Player found, but their character is not loaded."
        return
    end

    local h = Instance.new("Highlight")
    h.Name = "LocatorHighlight"
    h.Adornee = player.Character
    h.FillTransparency = 0.45
    h.OutlineTransparency = 0
    h.Parent = player.Character
    highlights[player] = h
    currentTarget = player
    status.Text = "Located: " .. player.Name
end

local function findPlayer(text)
    local needle = string.lower(text:gsub("^%s+", ""):gsub("%s+$", ""))
    if needle == "" then return nil end

    for _, player in ipairs(Players:GetPlayers()) do
        if string.lower(player.Name) == needle or string.lower(player.DisplayName) == needle then
            return player
        end
    end

    for _, player in ipairs(Players:GetPlayers()) do
        if string.find(string.lower(player.Name), needle, 1, true) then
            return player
        end
    end
    return nil
end

local function rebuildList()
    for _, child in ipairs(list:GetChildren()) do
        if child:IsA("TextButton") then child:Destroy() end
    end

    local players = Players:GetPlayers()
    table.sort(players, function(a, b) return a.Name:lower() < b.Name:lower() end)

    for _, player in ipairs(players) do
        local button = make("TextButton", {
            Size = UDim2.new(1, -8, 0, 30),
            BackgroundColor3 = Color3.fromRGB(45, 45, 55),
            Text = player.Name .. "  (" .. player.DisplayName .. ")",
            TextColor3 = Color3.fromRGB(235, 235, 240),
            TextSize = 13,
            Font = Enum.Font.Gotham,
        }, list)
        make("UICorner", {CornerRadius = UDim.new(0, 6)}, button)
        button.MouseButton1Click:Connect(function()
            search.Text = player.Name
            highlightPlayer(player)
        end)
    end

    task.wait()
    list.CanvasSize = UDim2.fromOffset(0, layout.AbsoluteContentSize.Y + 5)
    status.Text = tostring(#players) .. " players in this server."
end

locate.MouseButton1Click:Connect(function()
    local player = findPlayer(search.Text)
    if player then
        highlightPlayer(player)
    else
        status.Text = "No matching player found in this server."
    end
end)

clear.MouseButton1Click:Connect(function()
    clearHighlights()
    status.Text = "Highlight cleared."
end)

refresh.MouseButton1Click:Connect(rebuildList)
close.MouseButton1Click:Connect(function()
    gui.Enabled = false
end)

Players.PlayerAdded:Connect(rebuildList)
Players.PlayerRemoving:Connect(function(player)
    removeHighlight(player)
    rebuildList()
end)

-- Make the window draggable on desktop.
local UserInputService = game:GetService("UserInputService")
local dragging = false
local dragStart
local startPos

title.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = true
        dragStart = input.Position
        startPos = main.Position
    end
end)

title.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = false
    end
end)

UserInputService.InputChanged:Connect(function(input)
    if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
        local delta = input.Position - dragStart
        main.Position = UDim2.new(
            startPos.X.Scale, startPos.X.Offset + delta.X,
            startPos.Y.Scale, startPos.Y.Offset + delta.Y
        )
    end
end)

rebuildList()
