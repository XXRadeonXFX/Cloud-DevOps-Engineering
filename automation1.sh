#!/bin/bash

# Part 1: Unstaged
echo "-----------here is the git status-----------"
git status



# Part 2: Staged 
echo "----------Files are staged now------------" 
git add .
git status

# Part 3: Commit
echo "---------Commiting changes----------------"
git commit -m $1
echo "This is your commit message {$1}"

# Part 4 : Push
echo " pushing changes ........!"
git push 
 
