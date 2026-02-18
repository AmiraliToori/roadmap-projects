#!/usr/bin/env bash

# ─── Catppuccin Mocha Palette (Purple Flavor) ───────────────────────────────
readonly CLR_RESET='\033[0m'
readonly CLR_BOLD='\033[1m'
readonly CLR_DIM='\033[2m'
readonly CLR_ITALIC='\033[3m'

# Catppuccin Mocha colors (true ANSI 256 / 24-bit approximations)
readonly CLR_MAUVE='\033[38;2;203;166;247m'    # Mauve (primary purple)
readonly CLR_LAVENDER='\033[38;2;180;190;254m' # Lavender
readonly CLR_PINK='\033[38;2;245;194;231m'     # Pink
readonly CLR_RED='\033[38;2;243;139;168m'      # Red
readonly CLR_PEACH='\033[38;2;250;179;135m'    # Peach
readonly CLR_GREEN='\033[38;2;166;227;161m'    # Green
readonly CLR_TEAL='\033[38;2;148;226;213m'     # Teal
readonly CLR_SKY='\033[38;2;137;220;235m'      # Sky
readonly CLR_TEXT='\033[38;2;205;214;244m'     # Text
readonly CLR_SUBTEXT0='\033[38;2;166;173;200m' # Subtext0
readonly CLR_SUBTEXT1='\033[38;2;186;194;222m' # Subtext1
readonly CLR_OVERLAY0='\033[38;2;108;112;134m' # Overlay0
readonly CLR_SURFACE0='\033[38;2;49;50;68m'    # Surface0
readonly CLR_BASE='\033[38;2;30;30;46m'        # Base
readonly CLR_CRUST='\033[38;2;17;17;27m'       # Crust

readonly BG_MAUVE='\033[48;2;203;166;247m'
readonly BG_SURFACE0='\033[48;2;49;50;68m'
readonly BG_BASE='\033[48;2;30;30;46m'
readonly BG_CRUST='\033[48;2;17;17;27m'

# ─── Nerd Font Glyphs ──────────────��────────────────────────────────────────
readonly GLYPH_DNS="󰇖 "      # nf-md-dns
readonly GLYPH_SHIELD="󰒃 "   # nf-md-shield_check
readonly GLYPH_ARROW=" "    # nf-cod-arrow_right
readonly GLYPH_CHECK=" "    # nf-fa-check_circle
readonly GLYPH_CROSS=" "    # nf-cod-error
readonly GLYPH_STAR=" "     # nf-fa-star
readonly GLYPH_DOT=""       # nf-oct-dot_fill
readonly GLYPH_PROMPT="❯"    # prompt char
readonly GLYPH_WARN=" "     # nf-fa-warning
readonly GLYPH_GEAR=" "     # nf-cod-gear
readonly GLYPH_EXIT="󰍃 "     # nf-md-exit_to_app
readonly GLYPH_GLOBE="󰖟 "    # nf-md-web
readonly GLYPH_LINK=" "     # nf-fa-link
readonly GLYPH_SEPARATOR=""  # powerline separator
readonly GLYPH_RSEPARATOR="" # powerline reverse separator
readonly GLYPH_TOP_LEFT="╭"
readonly GLYPH_BOT_LEFT="╰"
readonly GLYPH_VERTICAL="│"
readonly GLYPH_HORIZONTAL="─"

# ─── Helper Functions ────────────────────────────────────────────────────────

print_separator() {
  local width=58
  printf "${CLR_OVERLAY0}"
  printf "  "
  for ((i = 0; i < width; i++)); do printf "${GLYPH_HORIZONTAL}"; done
  printf "${CLR_RESET}\n"
}

print_header() {
  printf "\n"
  printf "${CLR_BOLD}${CLR_MAUVE}  ${GLYPH_DNS}  resolv-it ${CLR_RESET}"
  printf "${CLR_DIM}${CLR_SUBTEXT0}── DNS Manager${CLR_RESET}\n"
  print_separator
}

print_bye() {
  printf "\n"
  printf "  ${CLR_MAUVE}${GLYPH_EXIT} ${CLR_LAVENDER}${CLR_ITALIC}Goodbye!${CLR_RESET}"
  printf " ${CLR_SUBTEXT0}Until next time...${CLR_RESET}\n\n"
}

print_warn() {
  printf "  ${CLR_PEACH}${GLYPH_WARN}  ${CLR_TEXT}%s${CLR_RESET}\n" "$1"
}

print_error() {
  printf "  ${CLR_RED}${GLYPH_CROSS}  ${CLR_TEXT}%s${CLR_RESET}\n" "$1"
}

print_success() {
  printf "  ${CLR_GREEN}${GLYPH_CHECK}  ${CLR_TEXT}%s${CLR_RESET}\n" "$1"
}

# ─── Privilege Check ─────────────────────────────────────────────────────────

if [[ $UID != 0 ]]; then
  printf "\n"
  printf "  ${CLR_RED}${GLYPH_SHIELD} ${CLR_BOLD} Permission Denied${CLR_RESET}\n"
  printf "  ${CLR_SUBTEXT0}Please run the script with ${CLR_PEACH}sudo${CLR_SUBTEXT0} privileges.${CLR_RESET}\n\n"
  exit 1
fi

set -euo pipefail

HOME=/home/glados/

CONFIG_FOLDER="$HOME/.config/resolv-it"

mkdir -p $CONFIG_FOLDER
touch "$CONFIG_FOLDER/config.toml"

declare -a array=()
content=$(cat "$CONFIG_FOLDER/config.toml")

# ─── Core Functions ──────────────────────────────────────────────────────────

function extract_current_dns {
  local current_dns_line=$(grep '^DNS' /etc/systemd/resolved.conf)
  local current_dns_address=$(echo "$current_dns_line" | grep -Eo '\b=(.+) (.+)\b' | sed 's/=//g')
  printf "$current_dns_address"
}

function extract_available_items {
  local line="$1"
  local counter="$2"

  local name=$(echo "$line" | grep -Eo '^(.+)=' | sed 's/=//')
  local dns_address=$(echo "$line" | grep -Eo '\"(.+) (.+)\"' | sed 's/\"//g')

  local current_dns_address=$(extract_current_dns)

  if [[ $dns_address == $current_dns_address ]]; then
    local counter_of_current_dns=$counter
  else
    local counter_of_current_dns=""
  fi

  array=("$counter" "$name" "$dns_address" "$counter_of_current_dns")
}

function display_dns_addresses {
  local counter="${array[0]}"
  local name="${array[1]}"
  local dns_address="${array[2]}"
  local counter_of_current_dns="${array[3]}"

  if [[ "$counter" == "$counter_of_current_dns" ]]; then
    # Active DNS entry — highlighted
    printf "  ${BG_SURFACE0}${CLR_MAUVE}${CLR_BOLD} ${GLYPH_STAR} ${counter} "
    printf "${CLR_RESET}${BG_SURFACE0}${CLR_LAVENDER}${GLYPH_SEPARATOR}${CLR_RESET} "
    printf "${BG_SURFACE0}${CLR_BOLD}${CLR_MAUVE}%-16s${CLR_RESET}" "$name"
    printf "${BG_SURFACE0} ${CLR_PINK}${GLYPH_GLOBE} ${CLR_TEXT}%-36s${CLR_RESET}" "$dns_address"
    printf "${BG_SURFACE0} ${CLR_GREEN}${GLYPH_CHECK}${CLR_RESET}"
    printf "\n"
  else
    # Inactive DNS entry
    printf "  ${CLR_OVERLAY0}  ${CLR_SUBTEXT1}${counter} "
    printf "${CLR_OVERLAY0}${GLYPH_SEPARATOR}${CLR_RESET} "
    printf "${CLR_TEXT}%-16s${CLR_RESET}" "$name"
    printf " ${CLR_SKY}${GLYPH_GLOBE} ${CLR_SUBTEXT0}%-36s${CLR_RESET}" "$dns_address"
    printf "\n"
  fi
}

function main_page {
  print_header
  printf "\n"
  printf "  ${CLR_DIM}${CLR_OVERLAY0}    # ${CLR_OVERLAY0}${GLYPH_SEPARATOR}${CLR_RESET}"
  printf " ${CLR_DIM}${CLR_OVERLAY0}%-16s${CLR_RESET}" "NAME"
  printf "   ${CLR_DIM}${CLR_OVERLAY0}%-36s${CLR_RESET}\n" "ADDRESS"
  print_separator
  local counter=1
  while IFS= read line; do
    if ! [[ "$line" =~ "[DNS]" ]]; then
      extract_available_items "$line" "$counter"
      display_dns_addresses
      counter=$((counter + 1))
    fi
  done <<<"$content"
  max_counter=$counter
  printf "\n"
}

function submit_selected_dns {
  local dns_name="$1"
  local dns_address="$2"

  cp /etc/systemd/resolved.conf /etc/systemd/resolved.conf.bak

  local resolv_line=$(tail -n 2 /etc/systemd/resolved.conf | grep -Eo "^# resolv-it")

  if [[ -n "$resolv_line" ]]; then
    local lines=$(wc -l /etc/systemd/resolved.conf | awk '{print $1}')
    lines=$((lines - 2))
    head -n "$lines" /etc/systemd/resolved.conf >/etc/systemd/resolved.conf.bak
    cat /etc/systemd/resolved.conf.bak >/etc/systemd/resolved.conf
  fi

  echo "# resolv-it $dns_name" >>/etc/systemd/resolved.conf
  echo "DNS=$dns_address" >>/etc/systemd/resolved.conf

  systemctl restart systemd-resolved
  ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf

  printf "\n"
  print_success "${CLR_BOLD}${CLR_MAUVE}${dns_name}${CLR_RESET}${CLR_TEXT} activated ${CLR_DIM}${CLR_SUBTEXT0}(${dns_address})${CLR_RESET}"
  printf "  ${CLR_SUBTEXT0}${GLYPH_LINK}  Symlinked ${CLR_DIM}/etc/resolv.conf${CLR_RESET}\n"
  printf "  ${CLR_SUBTEXT0}${GLYPH_GEAR}  Restarted ${CLR_DIM}systemd-resolved${CLR_RESET}\n"
}

function set_selected_dns {
  local option="$1"
  local counter=1
  while IFS= read line; do
    if ! [[ "$line" =~ "[DNS]" ]]; then
      extract_available_items "$line" "$counter"
      if [[ $counter -eq $option ]]; then
        local name=${array[1]}
        local dns_address=${array[2]}
        submit_selected_dns "$name" "$dns_address"
      fi
      counter=$((counter + 1))
    fi
  done <<<"$content"
}

# ─── Main Loop ───────────────────────────────────────────────────────────────

function main {
  while true; do
    clear
    main_page
    printf "  ${CLR_MAUVE}${GLYPH_PROMPT}${CLR_RESET} ${CLR_TEXT}Select a DNS "
    printf "${CLR_DIM}${CLR_SUBTEXT0}(${CLR_PEACH}q${CLR_SUBTEXT0} to quit)${CLR_RESET}"
    printf "${CLR_MAUVE} ${GLYPH_ARROW} ${CLR_RESET}"
    read -r option

    local counter_of_current_dns=${array[3]}
    if [[ $option =~ 'q' ]] || [[ $option =~ 'exit' ]] || [[ $option =~ 'quit' ]]; then
      print_bye
      exit 0
    elif [[ "$option" =~ "[a-zA-Z]+" ]]; then
      print_error "Invalid option!"
      sleep 1
      continue
    elif [[ $option == $counter_of_current_dns ]]; then
      print_warn "That DNS is already active."
      sleep 1
      continue
    elif [ $option -le 0 ]; then
      print_error "Invalid option!"
      sleep 1
      continue
    elif [ $option -gt $max_counter ]; then
      print_error "Invalid option!"
      sleep 1
      continue
    else
      set_selected_dns "$option"
      sleep 2
    fi
  done
}

main
