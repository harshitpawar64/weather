Output assets/onboarding.gif

Require "weather"

Set Shell bash
Set Width 1200
Set Height 600
Set FontSize 20
Set FontFamily "CaskaydiaCove Nerd Font"
Set Theme "Dracula"
Set Padding 10
Set WindowBar "Colorful"
Set BorderRadius 10
Set Margin 20
Set MarginFill "#282a36"
Set Framerate 60
Set TypingSpeed 75ms

Hide
Type "source .venv/bin/activate" Enter
Type "export XDG_CONFIG_HOME=$(mktemp -d)" Enter
Type "export XDG_CACHE_HOME=$(mktemp -d)" Enter
Type "export PS1='❯ '" Enter
Type "clear" Enter
Show

Type "weather setup" Sleep 500ms Enter

# Confirm detected location
Sleep 1.5s Type "y" Sleep 1s Enter

# Select metric units
Sleep 1.5s Type "metric" Sleep 1s Enter

# Display setup complete
Sleep 3s
