#!/usr/bin/env bash

# Builds the app and prepares distribution folder, using
# the given argument as the app entry point to be used by pyinstaller

# configured to use pyinstaller with options for Windows env

if [[ "$#" -ne 1 ]]; then
  echo "This script builds the app, intended for distribution."
  echo "Intended for developer usage only."
  echo "Pass one and only one argument: the name of the python script" \
       "that serves as the entry point to the app, residing in the src dir."
  echo "For example: ./build.sh main.py"
  exit 1
fi

if [ -x "$(command -v pyinstaller)" ]; then
  # this script must reside in project root dir
  ROOT="$(dirname $0)"
  DISTDIR="$ROOT"/dist/dtm-simulator
  pyinstaller --distpath "$DISTDIR" \
              --workpath "$ROOT"/build \
              --specpath "$ROOT" \
              --noconsole \
              --onefile \
              --name dtm-simulator \
              "$ROOT"/src/"$1"
  # copy license into dist dir if not exists
  if ! [ -f "$DISTDIR"/LICENSE.txt ]; then
    cp "$ROOT"/LICENSE.txt "$DISTDIR"
    echo "LICENSE.txt copied into dist dir"
  fi
  # insert readme into dist dir if not exists
  if ! [ -f "$DISTDIR"/README.txt ]; then
    READMEFILE="$DISTDIR"/README.txt
    touch "$READMEFILE"
    echo "DTM Simulator" >> "$READMEFILE"
    echo "by Joel Tengco" >> "$READMEFILE"
    echo "" >> "$READMEFILE"
    echo "A tool that can help design and" \
         "test deterministic Turing machines." >> "$READMEFILE"
    echo "" >> "$READMEFILE"
    echo "Run the application with dtm-simulator.exe" >> "$READMEFILE"
    echo "Go to https://github.com/clovenski/dtm-simulator#notes" \
         "for help on using this application." >> "$READMEFILE"

    echo "README.txt inserted into dist dir"
  fi
else
  echo "pyinstaller is not installed"
fi
