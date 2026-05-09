#!/bin/bash
# Script to automatically update AI learning roadmap
cd "/Users/daniel.chang/Desktop/ai/scripts"
python3 gen_roadmap.py
echo "Roadmap updated at $(date)" >> "/Users/daniel.chang/Desktop/ai/roadmap_update.log"