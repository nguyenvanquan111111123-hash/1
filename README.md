local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")
local player = Players.LocalPlayer

-- ===== KEY VERIFICATION SYSTEM =====
local correctKey = "Quỳnh"
local keyVerified = false

-- Create key verification GUI
local keyGui = Instance.new("ScreenGui")
keyGui.Name = "KeyVerification"
keyGui.Parent = game.CoreGui
keyGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

local keyFrame = Instance.new("Frame")
keyFrame.Parent = keyGui
keyFrame.AnchorPoint = Vector2.new(0.5, 0.5)
keyFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
keyFrame.Size = UDim2.new(0, 500, 0, 280)
keyFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 30)
keyFrame.BorderSizePixel = 2
keyFrame.BorderColor3 = Color3.fromRGB(0, 255, 255)

-- ===== BACKGROUND IMAGE =====
local bgImage = Instance.new("ImageLabel")
bgImage.Name = "Background"
bgImage.Parent = keyFrame
bgImage.Position = UDim2.new(0, 0, 0, 0)
bgImage.Size = UDim2.new(1, 0, 1, 0)
bgImage.BackgroundTransparency = 1
bgImage.Image = "rbxassetid://125338466430995"
bgImage.ZIndex = 0
bgImage.ImageTransparency = 0.2

local titleLabel = Instance.new("TextLabel")
titleLabel.Parent = keyFrame
titleLabel.Position = UDim2.new(0, 0, 0, 15)
titleLabel.Size = UDim2.new(1, 0, 0, 50)
titleLabel.BackgroundTransparency = 1
titleLabel.Text = "Key free"
titleLabel.TextColor3 = Color3.fromRGB(0, 255, 255)
titleLabel.Font = Enum.Font.GothamBlack
titleLabel.TextScaled = true
titleLabel.ZIndex = 2

local keyInput = Instance.new("TextBox")
keyInput.Parent = keyFrame
keyInput.Position = UDim2.new(0.05, 0, 0.35, 0)
keyInput.Size = UDim2.new(0.9, 0, 0.4, 0)
keyInput.BackgroundColor3 = Color3.fromRGB(40, 40, 50)
keyInput.BorderSizePixel = 1
keyInput.BorderColor3 = Color3.fromRGB(0, 255, 255)
keyInput.Text = ""
keyInput.PlaceholderText = "Nhập key của bạn..."
keyInput.TextColor3 = Color3.fromRGB(255, 255, 255)
keyInput.PlaceholderColor3 = Color3.fromRGB(150, 150, 150)
keyInput.Font = Enum.Font.Gotham
keyInput.TextSize = 18
keyInput.TextWrapped = true
keyInput.TextScaled = false
keyInput.ZIndex = 2

local submitBtn = Instance.new("TextButton")
submitBtn.Parent = keyFrame
submitBtn.Position = UDim2.new(0.05, 0, 0.83, 0)
submitBtn.Size = UDim2.new(0.4, 0, 0.12, 0)
submitBtn.BackgroundColor3 = Color3.fromRGB(0, 200, 100)
submitBtn.BorderSizePixel = 0
submitBtn.Text = "Xác Nhận"
submitBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
submitBtn.Font = Enum.Font.GothamBlack
submitBtn.TextScaled = true
submitBtn.ZIndex = 2

local closeBtn = Instance.new("TextButton")
closeBtn.Parent = keyFrame
closeBtn.Position = UDim2.new(0.55, 0, 0.83, 0)
closeBtn.Size = UDim2.new(0.4, 0, 0.12, 0)
closeBtn.BackgroundColor3 = Color3.fromRGB(200, 0, 0)
closeBtn.BorderSizePixel = 0
closeBtn.Text = "Thoát"
closeBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
closeBtn.Font = Enum.Font.GothamBlack
closeBtn.TextScaled = true
closeBtn.ZIndex = 2

local statusLabel = Instance.new("TextLabel")
statusLabel.Parent = keyFrame
statusLabel.Position = UDim2.new(0, 0, 0.75, 0)
statusLabel.Size = UDim2.new(1, 0, 0, 20)
statusLabel.BackgroundTransparency = 1
statusLabel.Text = ""
statusLabel.TextColor3 = Color3.fromRGB(255, 100, 100)
statusLabel.Font = Enum.Font.Gotham
statusLabel.TextScaled = true
statusLabel.ZIndex = 2

-- Rainbow colors for key frame
local rainbowColorsKey = {
    Color3.fromRGB(255, 0, 0),
    Color3.fromRGB(255, 127, 0),
    Color3.fromRGB(255, 255, 0),
    Color3.fromRGB(0, 255, 0),
    Color3.fromRGB(0, 0, 255),
    Color3.fromRGB(75, 0, 130),
    Color3.fromRGB(148, 0, 211)
}

-- Rainbow effect on key frame border
local keyFrameConnection
keyFrameConnection = RunService.Heartbeat:Connect(function()
    if keyFrame and keyFrame.Parent then
        local colorIndex = math.floor(tick() / 0.3) % 7 + 1
        keyFrame.BorderColor3 = rainbowColorsKey[colorIndex]
    end
end)

-- Make key frame draggable
local dragging = false
local dragStart = Vector2.new(0, 0)

keyFrame.InputBegan:Connect(function(input, gameProcessed)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = true
        dragStart = input.Position
    end
end)

keyFrame.InputEnded:Connect(function(input, gameProcessed)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = false
    end
end)

game:GetService("UserInputService").InputChanged:Connect(function(input, gameProcessed)
    if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
        local delta = input.Position - dragStart
        keyFrame.Position = keyFrame.Position + UDim2.fromOffset(delta.X, delta.Y)
        dragStart = input.Position
    end
end)

submitBtn.MouseButton1Down:Connect(function()
    if keyInput.Text == correctKey then
        keyVerified = true
        statusLabel.Text = "✓ Key chính xác!"
        statusLabel.TextColor3 = Color3.fromRGB(0, 255, 100)
        task.wait(1)
        if keyFrameConnection then
            keyFrameConnection:Disconnect()
        end
        keyGui:Destroy()
    else
        statusLabel.Text = "✗ Key không chính xác!"
        keyInput.Text = ""
        task.wait(2)
        statusLabel.Text = ""
    end
end)

closeBtn.MouseButton1Down:Connect(function()
    if keyFrameConnection then
        keyFrameConnection:Disconnect()
    end
    keyGui:Destroy()
    game:Shutdown()
end)

keyInput.FocusLost:Connect(function(enterPressed)
    if enterPressed then
        submitBtn:FireEvent("MouseButton1Down")
    end
end)

-- Wait for key verification
repeat task.wait() until keyVerified

-- ===== RAINBOW RAIN EFFECT AFTER KEY VERIFICATION =====
local rainbowColors = {
    Color3.fromRGB(255, 0, 0),
    Color3.fromRGB(255, 127, 0),
    Color3.fromRGB(255, 255, 0),
    Color3.fromRGB(0, 255, 0),
    Color3.fromRGB(0, 0, 255),
    Color3.fromRGB(75, 0, 130),
    Color3.fromRGB(148, 0, 211)
}

local function createRainDrop(colorIndex)
    if not player.Character or not player.Character:FindFirstChild("HumanoidRootPart") then return end
    
    local raindrop = Instance.new("Part")
    raindrop.Anchored = true
    raindrop.CanCollide = false
    raindrop.Shape = Enum.PartType.Ball
    raindrop.Size = Vector3.new(0.8, 0.8, 0.8)
    raindrop.Color = rainbowColors[colorIndex]
    raindrop.Material = Enum.Material.Neon
    
    local playerPos = player.Character.HumanoidRootPart.Position
    local offsetX = math.random(-30, 30)
    local offsetZ = math.random(-30, 30)
    raindrop.Position = playerPos + Vector3.new(offsetX, 50, offsetZ)
    
    raindrop.Parent = workspace
    
    local tween = TweenService:Create(
        raindrop,
        TweenInfo.new(3, Enum.EasingStyle.Linear, Enum.EasingDirection.In),
        {Position = playerPos + Vector3.new(offsetX, -30, offsetZ)}
    )
    tween:Play()
    
    game:GetService("Debris"):AddItem(raindrop, 3.5)
end

local rainStartTime = tick()
local colorRotation = 1
while tick() - rainStartTime < 8 do
    for i = 1, 15 do
        createRainDrop(colorRotation)
        colorRotation = colorRotation % 7 + 1
    end
    task.wait(0.15)
end

-- ===== INTRO GUI =====
local gui = Instance.new("ScreenGui")
gui.Name = " VannQuann "
gui.IgnoreGuiInset = true
gui.ResetOnSpawn = false
gui.Parent = player:WaitForChild("PlayerGui")

local msg = Instance.new("TextLabel")
msg.Parent = gui
msg.AnchorPoint = Vector2.new(0.5,0.5)
msg.Position = UDim2.new(0.5,0,0.5,0)
msg.Size = UDim2.new(0,600,0,120)
msg.BackgroundTransparency = 1
msg.Text = " VannQuann Roblox "
msg.TextColor3 = Color3.fromRGB(0,255,255)
msg.Font = Enum.Font.GothamBlack
msg.TextScaled = true
msg.TextStrokeTransparency = 0
msg.TextStrokeColor3 = Color3.fromRGB(0,0,0)
msg.TextTransparency = 1

local function createFirework()
    if not player.Character or not player.Character:FindFirstChild("HumanoidRootPart") then return end
    local part = Instance.new("Part")
    part.Anchored = true
    part.CanCollide = false
    part.Size = Vector3.new(0.5,0.5,0.5)
    part.Position = player.Character.HumanoidRootPart.Position + Vector3.new(math.random(-10,10),math.random(5,15),math.random(-10,10))
    part.Transparency = 1
    part.Parent = workspace

    local firework = Instance.new("ParticleEmitter")
    firework.Texture = "rbxassetid://243660364"
    firework.Rate = 50
    firework.Lifetime = NumberRange.new(1)
    firework.Speed = NumberRange.new(10)
    firework.SpreadAngle = Vector2.new(360,360)
    firework.Color = ColorSequence.new(Color3.fromRGB(math.random(100,255),math.random(100,255),math.random(100,255)))
    firework.Parent = part

    game.Debris:AddItem(part,2)
end

local appear = TweenService:Create(msg, TweenInfo.new(1.5, Enum.EasingStyle.Quad), {TextTransparency=0})
appear:Play()
appear.Completed:Wait()

local startTime = tick()
while tick()-startTime < 5 do
    msg.TextColor3 = Color3.fromRGB(math.random(0,255),math.random(180,255),math.random(200,255))
    createFirework()
    task.wait(0.25)
end

local vanish = TweenService:Create(msg, TweenInfo.new(2, Enum.EasingStyle.Sine), {TextTransparency=1})
vanish:Play()
vanish.Completed:Wait()
gui:Destroy()

-- ===== MAIN UI WITH TOGGLE =====
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Parent = game.CoreGui
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

-- Store player avatar
local playerAvatarUrl = "https://www.roblox.com/bust-thumbnails/image?userId=" .. player.UserId .. "&width=420&height=420&format=Png"

local toggleConnection
local menuVisible = true
local avatarContainer = nil

-- ===== RAINBOW EFFECT FOR MAIN MENU =====
local rainbowColorsUI = {
    Color3.fromRGB(255, 0, 0),
    Color3.fromRGB(255, 127, 0),
    Color3.fromRGB(255, 255, 0),
    Color3.fromRGB(0, 255, 0),
    Color3.fromRGB(0, 0, 255),
    Color3.fromRGB(75, 0, 130),
    Color3.fromRGB(148, 0, 211)
}

local function startRainbowEffect(window)
    if toggleConnection then
        toggleConnection:Disconnect()
    end
    
    toggleConnection = RunService.Heartbeat:Connect(function()
        if menuVisible and window and window.Root and window.Root.Parent then
            local colorIndex = math.floor(tick() / 0.2) % 7 + 1
            window.Root.BorderColor3 = rainbowColorsUI[colorIndex]
            window.Root.BorderSizePixel = 3
        end
    end)
end

-- Rainbow effect on avatar border
local function startAvatarRainbowEffect()
    if toggleConnection then
        toggleConnection:Disconnect()
    end
    
    toggleConnection = RunService.Heartbeat:Connect(function()
        if not menuVisible and avatarContainer and avatarContainer.Parent then
            local colorIndex = math.floor(tick() / 0.2) % 7 + 1
            avatarContainer.BorderColor3 = rainbowColorsUI[colorIndex]
        end
    end)
end

-- Create avatar button with rainbow border AND click handler
local function createAvatarButton(toggleMenuFunc)
    avatarContainer = Instance.new("Frame")
    avatarContainer.Name = "AvatarContainer"
    avatarContainer.Parent = ScreenGui
    avatarContainer.Position = UDim2.new(0.1, 0, 0.15, 0)
    avatarContainer.Size = UDim2.new(0, 80, 0, 80)
    avatarContainer.BackgroundColor3 = Color3.fromRGB(0, 0, 0)
    avatarContainer.BorderSizePixel = 3
    avatarContainer.BorderColor3 = Color3.fromRGB(0, 255, 255)
    
    -- Corner radius for container
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(1, 0)
    corner.Parent = avatarContainer
    
    local avatarLabel = Instance.new("ImageLabel")
    avatarLabel.Name = "PlayerAvatar"
    avatarLabel.Parent = avatarContainer
    avatarLabel.Position = UDim2.new(0, 0, 0, 0)
    avatarLabel.Size = UDim2.new(1, 0, 1, 0)
    avatarLabel.BackgroundTransparency = 1
    avatarLabel.Image = playerAvatarUrl
    
    -- Make avatar circular
    local avatarCorner = Instance.new("UICorner")
    avatarCorner.CornerRadius = UDim.new(1, 0)
    avatarCorner.Parent = avatarLabel
    
    -- ADD CLICK HANDLER IMMEDIATELY
    avatarContainer.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            toggleMenuFunc()
        end
    end)
    
    return avatarContainer
end

local function createMainWindow()
    -- Load Fluent
    local Fluent = loadstring(game:HttpGet("https://github.com/dawid-scripts/Fluent/releases/latest/download/main.lua"))()
    
    local Window = Fluent:CreateWindow({
        Title=" VanQuan ",
        SubTitle="Blox Fruit",
        TabWidth=157,
        Size=UDim2.fromOffset(450,300),
        Acrylic=true,
        Theme="Light",
        MinimizeKey=Enum.KeyCode.End
    })

    local Tabs = {
        Main0=Window:AddTab({Title="Thông Tin"}),
        Main1=Window:AddTab({Title="Script Blox fruit"}),
        Main2=Window:AddTab({Title=" Attack on Titan"}),
    }

    -- Tab 0
    Tabs.Main0:AddButton({Title="Discord",Description="vannquann_85053",Callback=function() 
        setclipboard("https://discord.gg/JZ9M7GJ5H")
        Fluent:Notify({Title = "Thành Công", Content = "Discord link đã được sao chép!", Duration = 2})
    end})

    Tabs.Main0:AddParagraph({
        Title = "Thông Tin",
        Content = "Script đã được xác thực thành công!\nKey: Quỳnh\nMỗi lần khởi động cần nhập key.\n\nNhấn avatar để ẩn menu và nhấn lại để hiện menu."
    })

    -- Tab 1
    Tabs.Main1:AddButton({Title="GravityHub",Callback=function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/Dev-GravityHub/BloxFruit/refs/heads/main/Main.lua"))()
    end})

    Tabs.Main1:AddButton({Title="AbacaxiHubOfc",Callback=function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/real33ms/BloxFruits/refs/heads/main/AbacaxiHubOfc.lua"))()
    end})

    Tabs.Main1:AddButton({Title="KhaBanhHubV2",Callback=function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/longhihilonghihi-hub/KhaBanhHubV2/refs/heads/main/obf_m92m5V2G0rk2XM6IPP1L1O701401kdJLV4V5nEyYclj029p00N3SyRWn7S1ax4Uz.lua.txt"))()
    end})

    Tabs.Main1:AddButton({Title="AnDepZaiHubBeta",Callback=function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/AnDepZaiHub/AnDepZaiHubBeta/refs/heads/main/AnDepZaiHubBeta.lua"))()
    end})

    Tabs.Main1:AddButton({Title="QuantumOnyx",Callback=function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/flazhy/QuantumOnyx/refs/heads/main/QuantumOnyx.lua"))()
    end})

    Tabs.Main1:AddButton({Title="Xeter v4",Callback=function()
        getgenv().Version = "V4"
        getgenv().Team = "Marines"
        loadstring(game:HttpGet("https://raw.githubusercontent.com/TlDinhKhoi/Xeter/refs/heads/main/Main.lua"))() 
    end})

    Tabs.Main1:AddButton({Title="BaconHub",Callback=function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/vinh129150/hack/refs/heads/main/BaconHub.lua"))()
    end})

    Tabs.Main1:AddButton({Title="Vxezehub",Callback=function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/Dex-Bear/Vxezehub/refs/heads/main/BF-Main.lua"))()
    end})

    Tabs.Main1:AddButton({Title="redzHub",Callback=function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/huy384/redzHub/refs/heads/main/redzHub.lua"))()
    end})

    -- Tab 2 - SET AS DEFAULT
    Tabs.Main2:AddButton({Title="Tekkit hub",Callback=function()
        loadstring(game:HttpGet("https://api.luarmor.net/files/v4/loaders/705e7fe7aa288f0fe86900cedb1119b1.lua"))()
    end})
     
    Tabs.Main2:AddButton({Title="Kira hub",Callback=function()
        --[[
	WARNING: Heads up! This script has not been verified by ScriptBlox. Use at your own risk!
]]
loadstring(game:HttpGet("https://raw.githubusercontent.com/OhhMyGehlee/Sol14/refs/heads/main/k"))()

---Works In Solara and Other More Executors!!
    end})

    Tabs.Main2:AddButton({Title="HopBoss",Callback=function()
        repeat wait() until game:IsLoaded() and game.Players.LocalPlayer 
        getgenv().team = "Pirates"
        loadstring(game:HttpGet("https://raw.githubusercontent.com/vinh129150/hack/refs/heads/main/HopBoss.lua"))()
    end})

    -- Select Tab 2 as default
    Window:SelectTab(Tabs.Main2)

    return Window
end

local Window

-- Toggle function
local function toggleMenu()
    if menuVisible then
        -- Hide menu and show avatar
        menuVisible = false
        if toggleConnection then
            toggleConnection:Disconnect()
        end
        
        if Window and Window.Root then
            Window.Root.Visible = false
        end
        
        createAvatarButton(toggleMenu)
        startAvatarRainbowEffect()
    else
        -- Show menu and hide avatar
        menuVisible = true
        if avatarContainer and avatarContainer.Parent then
            avatarContainer:Destroy()
            avatarContainer = nil
        end
        
        if Window and Window.Root then
            Window.Root.Visible = true
        end
        
        startRainbowEffect(Window)
    end
end

repeat task.wait() until game:IsLoaded()
Window = createMainWindow()
startRainbowEffect(Window)

print("✓ Script loaded successfully! Enjoy!")
