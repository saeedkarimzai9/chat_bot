# Roblox Player Locator GUI

A Roblox-side GUI for experiences you own or are authorized to develop.

## Install

1. Open your Roblox experience in Roblox Studio.
2. In Explorer, open **StarterPlayer > StarterPlayerScripts**.
3. Insert a **LocalScript**.
4. Copy the contents of `PlayerLocator.client.lua` into that LocalScript.
5. Press **Play** to test.

## Features

- Search players by username or display name.
- Click a player from the server list.
- Highlight the selected player's character.
- Refresh the player list.
- Clear the highlight.
- Draggable desktop GUI.
- Recreates in each place when installed in that place's StarterPlayerScripts.

This is intentionally a Roblox Studio / experience-side implementation. It does not inject into or modify games that you do not control.
