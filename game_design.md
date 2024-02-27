<!-- Rough layout of requirements -->
<!-- It might not be considered a design doc but still make stuff easier for me -->

Game design document:
	- Gameplay
		○ Sandbox
		○ Finite terrain
		○ Fps cam
		○ Level based
		○ pvp…no?
			§ Let other person trade stuff while both are competing - creating game theory paradox
	- Goal
		○ Build a certain object within time limit
		○ The object(house or whatever) could be built/crafted with individual elements
		○ find hidden individual elements in the finite world
		○ Levels based on different objects that you have to build
		
	- Specifics
		○ Start with basic stuff in inventory
		○ Look objective: what to create
		○ Read cook book
		○ Figure what elements do you need
		○ Find elements
		○ Remove unnecessary stuff from inventory
		○ Inventory has space limit
		○ Stuff combines to form stuff which combines to form … the objective
		
	- Specifics narrowed down:
		○ Level1:
			§ Objective: house
			§ Time: 2 min
			§ Terrain: plain, finite
			§ Environment: env0
			§ Hiding places: predefined and objects placed for level0
			§ Inventory management: real time storage a dict maybe
			§ Crafting system in inventory
			
			
			
		○ Assets available:
			§ Dungeon stuff: 203
			§ Medieval: 55 - mostly tower walls
			§ Characters: 4
			
		○ Questions: - what how where
			§ Will I be designing the house
				□ Design the end objective of the level - house for level0
				□ Blender procedurally or manually
				□ panda3d rendering
					® Minecraft like system - this one maybe
			§ How hide stuff
			§ inventory UI
			§ 2d GUI system
			§ What elements builds what - if end product has no features of parent components
			§ If end product has parent features - list all these end products
				□ Design these end products in blender
			§ Predefined environment structure or procedural like minecraft?
				□ Will be Predefined -> plan where stuff will be hidden
			§ Environment design!?
			§ levels
				□ Each level has different what?
					® Environment, hiding spot, theme, hazards and traps(challenges)
				□ Is environment gonna be different for each level?
					® A little bit - will decide later
				□ hiding places be different for each level?
					® Same environment
						◊ All hidden places defined but things hidden in which spot defined by level
					® Different environment
                        ◊ Hidden spots according to environment