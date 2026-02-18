#!/usr/bin/env bash

set -euo pipefail

# ==============================================================================
#  THEME: CATPPUCCIN MOCHA & ICONS
# ==============================================================================
esc=$'\033'
reset="${esc}[0m"
bold="${esc}[1m"

# Colors
mauve="${esc}[38;2;203;166;247m"
blue="${esc}[38;2;137;180;250m"
green="${esc}[38;2;166;227;161m"
yellow="${esc}[38;2;249;226;175m"
red="${esc}[38;2;243;139;168m"
text="${esc}[38;2;205;214;244m"
overlay="${esc}[38;2;108;112;134m"
mantle="${esc}[38;2;24;24;37m"

# Glyphs (Nerd Font)
icon_usb=" "
icon_disk=" "
icon_mount=" "
icon_unmount=" "
icon_arrow=""
icon_warn=" "
icon_exit=" "

function display_header {
  clear
  printf "${mauve}    __  __                   _            ${reset}\n"
  printf "${mauve}   |  \/  | ___  _   _ _ __ | |_ ___ _ __ ${reset}\n"
  printf "${blue}   | |\/| |/ _ \| | | | '_ \| __/ _ \ '__|${reset}\n"
  printf "${blue}   | |  | | (_) | |_| | | | | ||  __/ |   ${reset}\n"
  printf "${mauve}   |_|  |_|\___/ \__,_|_| |_|\__\___|_|   ${reset}\n"
  printf "${overlay}   ──────────────────────────────────────${reset}\n\n"
}

function display_status {
  local status_list="$1"

  if [ -z "$status_list" ]; then
    printf " ${red}${icon_warn} There is no removable device attached.${reset}\n"
    exit 1
  fi

  local counter=1

  while IFS= read -r line; do
    eval "$line"

    if [[ -n $MODEL ]]; then
      # Disk/Device Header Line
      printf "\n ${mauve}${icon_usb} %s${reset} ${overlay}(%s)${reset}\n" "$NAME" "$MODEL"
    elif [[ -n $LABEL ]]; then

      # Partition Line logic preserved
      if [[ -z $MOUNTPOINT ]]; then
        STATUS="${overlay}${icon_unmount} Unmounted${reset}"
      else
        STATUS="${green}${icon_mount} Mounted${reset}  "
      fi

      # Fancy column alignment
      printf "   ${blue}%s.${reset} ${icon_disk} ${text}%-10s${reset} ${overlay}%-6s${reset} ${yellow}%-6s${reset} ${text}%-12s${reset} %b\n" \
        "$counter" "$NAME" "$FSTYPE" "$SIZE" "$LABEL" "$STATUS"
      
      counter=$((counter + 1))
    fi

  done <<<"$status_list"
}

function mount_unmount_partition {
  local partitions="$1"
  local number=$2

  local counter=1

  while IFS= read -r line; do
    eval "$line"
    if [[ "$number" =~ "$counter" ]]; then
      printf "\n ${overlay}Processing...${reset}\n"
      
      if [[ -z $MOUNTPOINT ]]; then
        # Logic preserved: Mounting
        udisksctl mount -b $NAME > /dev/null
        printf " ${green}✔ MOUNTED${reset} at ${blue}/media/glados/%s${reset}.\n" "$LABEL"
      else
        # Logic preserved: Unmounting
        udisksctl unmount -b $NAME > /dev/null
        printf " ${green}✔ EJECTED SAFELY${reset} the ${blue}/media/glados/%s${reset}.\n" "$LABEL"
      fi
      sleep 1.5 
    fi

    counter=$((counter + 1))

  done <<<"$partitions"
}

# ==============================================================================
#  MAIN LOOP
# ==============================================================================

while true; do

  removeable_devices_lines="$(lsblk -pP -o NAME,RM,SIZE,FSTYPE,MODEL,LABEL,MOUNTPOINT,TYPE | awk '$2 == "RM\=\"1\"" {print}' 2>/dev/null)"
  partitions="$(awk '$8 == "TYPE\=\"part\"" {print}' 2>/dev/null <<<"$removeable_devices_lines")"
  partition_counts=$(wc -l <<<$partitions)
  
  display_header
  display_status "$removeable_devices_lines"

  printf "\n ${overlay}Write '${red}q${overlay}' for exit.${reset}"
  printf "\n\n"

  # Colored prompt
  printf "${blue} ${icon_arrow} Enter the device to mount or unmount:${reset} " 
  read -r option

  if [[ $option =~ "q" ]]; then
    printf "\n ${mauve}${icon_exit} Bye!${reset}\n"
    exit 0
  elif [[ $option -gt $partition_counts ]] || [[ $option -le 0 ]]; then
    printf "\n ${red}${icon_warn} Invalid option!${reset}\n"
    sleep 1
    exit 1
  elif [[ $option -le $option ]] && [[ $option -ge 1 ]]; then
    mount_unmount_partition "$partitions" $option
  fi

done
