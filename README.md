# Computationally Creative Dungeon Generation

This project is a system written in python, designed to create levels or 'dungeons' for zelda like games.
It takes heavy inspiration from the youtube series [Boss Keys](https://www.youtube.com/watch?v=ouO1R6vFDBo&list=PLc38fcMFcV_ul4D6OChdWhsNsYY3NA5B2) created by Mark Brown. This series specifically explores the level
design in the legend of zelda games created by nintendo. However, due to the legal and technical difficulty
associated with integrating code with a legend of zelda game we chose to use a different game for this project.

## Examples

Below are several examples of the output of this system. Click on the images to see videos of gameplay.

[![Example Level Set](https://github.com/bjatkin/dungeon-design/blob/master/images/LevelSetThumbnail.png)](https://www.youtube.com/watch?v=OMKOFWbV2nM)
[![Example Puzzle Script Level](https://github.com/bjatkin/dungeon-design/blob/master/images/PuzzleScriptThumbnail.png)](https://www.youtube.com/watch?v=a96jft9shLM)
[![Example Sokoban Level](https://github.com/bjatkin/dungeon-design/blob/master/images/SokobanThumbnail.png)](https://www.youtube.com/watch?v=3zBTDilPgyc)

## Chips Challenge

One of the engines used in the development of this project is [Chips Challenge](https://en.wikipedia.org/wiki/Chip%27s_Challenge). This is a 1990's era top down puzzle game. In order to integrate this game with our system
we use SuperCC, and Tile World. Both of these are reprogramed versions of the original designed to work on 
modern hardware. SuperCC was used for macOS development and Tile World was used for PC development.

## Puzzle Script

One goal of this system was to make a system that was game agnostic. In other words, the goal was to create a
system that could create interesting level designs in games other than Chips Challenge. In order to achieve this
we used a game prototyping project called [Puzzle Script](https://www.puzzlescript.net/). This is a great project
for creating small simple prototypes of puzzle games. We created a small game with similar mechanics to
chips challenge in order to develop the abstraction layer that would let the system design levels for multiple
games.

## System Overview

![System Design](https://github.com/bjatkin/dungeon-design/blob/master/images/SystemDesign.png)
This system uses several 'Aesthetic Settings' in order to determining how a level should be generated. The goal is that
these settings control the broad strokes of the levels generation rather than being overly prescriptive on how
the final level looks. These settings are used to generate both a level graph (inspired by GMTK's level graphs). As well
as a level space. These 2 objects are then combined into a fully realized level. This final level is then
evaluated to ensure the level is winnable. Unwinnable levels are rejected and winable levels are passed to the analyser
where levels are reviewed to determine their quality. We use several quality metrics to determine the 'difficulty'
and 'fun-ness' of each level in this step. Levels are finally organized by difficulty to give the player a fun set of
levels with a gradual challenge ramp up.

## Level Graphs

![Level Graph](https://github.com/bjatkin/dungeon-design/blob/master/images/LevelGraph.png)


Level graphs are a key portion of the system and were inspired by GMTK's 
[Boss Keys youtube series](https://www.youtube.com/watch?v=ouO1R6vFDBo&list=PLc38fcMFcV_ul4D6OChdWhsNsYY3NA5B2) 
This graph represents the abstract critical path through a level. Squares represent barriers that players must overcome
and circles represent 'keys' that allow players to overcome an obstacle. Each barrier can have one or more keys and each
key must map to exactly one barrier. Barriers can be anything from any enemy to a puzzle to a actual door that
must be unlocked. Keys can be actual keys but can also be other weapons or items that allow the player to overcome
a barrier. The red lines in the diagram represent the connection between keys and associated barriers. Black lines
represent the path a player can take through the graph. These graphs don't prescribe the physical layout, but rather
an order in which keys and barriers can be encountered in the level.

## Level Space

![Level Space](https://github.com/bjatkin/dungeon-design/blob/master/images/LevelSpace.png)


The level space is the physical space that the player will move around. This space has no information about the
level graph but rather is generated as its own separate step. Each level consists of different sized/ shaped
rooms with various connections. With some additional 'noise' added to keep each room unique and interesting.
This space is eventually converted into a graph and the level space and level graph are merged using 
[subgraph Isomorphism](https://en.wikipedia.org/wiki/Subgraph_isomorphism_problem).

## System Output

The final output of this system is either a .dat file or an HTML file. the .dat file can be used to player the generated
levels in either SuperCC or Tile World. The file follows the conventions of the original chips challenge level files.
HTML files contain all the code to play the small game created using [Puzzle Script](https://www.puzzlescript.net/). This
file will also contain the levels generated by the system.

## Rating System

A small rating system was included in this project to make it easy to see how tweaks to the aesthetic settings
modify the quality of the produced levels. Currently this system is fairly limited and only supports ratings 
from the two creators of the project.

## Configuring This Project

This project can be configured by creating a config.json file in the working directory of the project.
example-config.json is provided as an example of what this file should contain.

## Full Project Writeup

This project contains a pdf writeup on how this project qualify itself as computationally creative.
you can find the full paper [here](https://github.com/bjatkin/dungeon-design/blob/master/Project_Writeup.pdf)

#### Future Work:
  * Add enemies
  * Allow the user to provide some interesting layout information
  * Rate a bunch of levels and try to figure out what makes a level good


