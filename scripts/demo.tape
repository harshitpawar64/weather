Output assets/demo.gif

Require "weather"

Set Shell bash
Set Width 1100
Set Height 1200
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
Type "export PS1='❯ '" Enter
Type "clear" Enter
Show

Type "weather -l 'New York'" Sleep 500ms Enter

Sleep 5s
