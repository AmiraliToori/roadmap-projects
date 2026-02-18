#!/usr/bin/env bash

ESC=$'\x1b'

reset="${ESC}[0m"
bold="${ESC}[1m"

txt="${ESC}[38;2;205;214;244m"
muted="${ESC}[38;2;108;112;134m"

mauve="${ESC}[38;2;203;166;247m"
blue="${ESC}[38;2;137;180;250m"
green="${ESC}[38;2;166;227;161m"
yellow="${ESC}[38;2;249;226;175m"
red="${ESC}[38;2;243;139;168m"

clear
printf "${mauve}    ______ _ __       ${blue}   ______                __            ${reset}\n"
printf "${mauve}   / ____/(_) /__     ${blue}  / ____/________  ____ _/ /_____  _____${reset}\n"
printf "${mauve}  / /_   / / / _ \\    ${blue} / /   / ___/ _ \\/ __ \`/ __/ __ \\/ ___/${reset}\n"
printf "${mauve} / __/  / / /  __/    ${blue}/ /___/ /  /  __/ /_/ / /_/ /_/ / /    ${reset}\n"
printf "${mauve}/_/    /_/_/\\___/     ${blue}\\____/_/   \\___/\\__,_/\\__/\\____/_/     ${reset}\n"
printf "\n"
printf "${muted}────────────────────────────────────────────────────────────${reset}\n\n"

sleep 0.5

printf "${txt}What kind of script do you want to create?\n\n${reset}"

printf "${blue}  1.${reset} ${txt}Python${reset}\n"
printf "${blue}  2.${reset} ${txt}Lua${reset}\n"
printf "${blue}  3.${reset} ${txt}Shell (Bash)${reset}\n"
printf "${blue}  4.${reset} ${txt}Custom${reset}\n\n"
printf "${blue}Enter q for exit.${reset}\n\n"

read -rp "${mauve}❯${reset} " option

if [[ "$option" =~ "q" ]]; then
  printf "\n${red}${bold}󰩈 Bye Bye...${reset}\n"
  sleep 1.5
  exit 0
elif (($option != 1)) && (($option != 2)) && (($option != 3)) && (($option != 4)); then
  printf "\n${red}${bold}✖ Invalid input${reset}\n"
  sleep 3
  exit 1
fi

sleep 0.5

read -rp "${blue}󰈔 Enter a name for your file:${reset} " file_name

function create_file {

  local format="$1"
  local file_name="$2"
  local first_line="$3"

  local complete_file_name="$file_name.$format"

  if [[ -f "$complete_file_name" ]]; then
    printf "\n${yellow}⚠ File already exists:${reset} ${txt}%s${reset}\n" "$complete_file_name"
    sleep 3
    exit 1
  fi

  touch "$complete_file_name"
  chmod u+x "$complete_file_name"

  if [ -n "$first_line" ]; then
    echo "$first_line" >>$complete_file_name
  fi

  if (($? == 0)); then
    printf "\n${green}${bold}✔ Created:${reset} ${txt}%s${reset}\n" "$complete_file_name"
  else
    printf "\n${red}${bold}✖ Something went wrong${reset}\n"
    exit 1
  fi
}

case "$option" in
"1")
  format="py"
  create_file "$format" "$file_name" "#!/usr/bin/env python3"
  ;;
"2")
  format="lua"
  create_file "$format" "$file_name" "#!/usr/bin/env lua"
  ;;
"3")
  format="sh"
  create_file "$format" "$file_name" "#!/usr/bin/env bash"
  ;;
"4")
  read -rp "${blue}󰏪 Enter a format for your file:${reset} " format
  create_file "$format" "$file_name"
  ;;
esac

printf "\n"
read -rp "${mauve} Edit it now?${reset} ${muted}(y/n)${reset} " edit_option

if [[ "$edit_option" =~ "y" ]] || [[ "$edit_option" =~ "yes" ]]; then
  printf "${blue}󰈹 Opening…${reset}\n"
  sleep 2
  $EDITOR "$file_name.$format"
elif [[ "$edit_option" =~ "n" ]] || [[ "$edit_option" =~ "no" ]]; then
  printf "${muted}󰩈 Done.${reset}\n"
  sleep 2
  exit 0
else
  printf "${red}${bold}✖ Invalid choice${reset}\n"
  exit 1
fi
