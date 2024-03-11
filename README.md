# 3D Crafting game
#### Video Demo:  <https://www.youtube.com/watch?v=L68m5XXR2-s>
#### Description:
#### `Final project for cs50p. A 3D first person crafting game developed using panda3d game engine.`
### Features Implemented:
1. Initial Game Design Document to serve as basic requirements document
2. FPS camera movement
3. WASD and turbo controls for player movement
4. Actor behind the camera (Will come in handy for pvp mode)
5. Cross hair in the middle of screen casts ray to 3d select objects
6. Bullet Physics for movement and mouse rotation
7. Player and Terrain collision allow jumps by player under gravity
8. Alternate color card tiles for terrain floor
9. Crafting System
    - Join items by specifying the faces you want joined
    - Adjust position and rotation of individual selected items manually
10. Colliders attached to each item to detect ray cast on the items 
11. Colliders encompass the visble boundary of the items
12. Reset rotation functionality is used wherever needed
13. Select and unselect items
14. Inventory system
    - Select inventory items from the inventory to place in the scene
    - Select multiple copies or unique items from given 203 assets
    - Inventory items presented in the dialogue with their name
15. Press `ctrl+left-click` at some point to bring the previously selected item close to the player

### Implementation details:
- **Game Design Document:** The document rests in the root directory by the name `game_design.md`. It is a rough requirement document describing the design of the overall software. Although all the requirements were not fulfilled as planned but most of the features were based on this document.

- **Assets:** All the assets are in the `assets/` directory. Characters and Item assets are part of Kenny's asset pack freely available to use for commercial and non-commercial uses. For items, there are 2 text files in root directory that include the assets file names. These files are used to load all the assets in the game.

- **Object Oriented Design:** The project is structured using a modular approach in classes and subclasses. The `main` function in `project.py` instantiates a Game object as is required by the panda3d engine. The Game class inherits from `DirectObject.DirectObject` which enables us to access the global space variables available through panda3d to make lot of things easier during development. Most commonly used object is `taskMgr` which contains all the tasks or functions that are supposed to run each frame of the game.

- **Player movement and Physics:** Player is a bullet object and a cylinderical collider shape wraps the player object. The `base.cam` node is reparented to player(cam acts as a child of player node), so the camera and player move together. Player is a character model not in the scene view as it is rendered behind the camera to give a first person view. The player actor will be visible to other players in later versions involving multiplayer feature. The terrain's floor is an infinite bullet plane over which the player can walk and jump. Player walks in different directions based on key inputs or camera positioning by applying velocity in specified direction or angular force to rotate the player's direction based on mouse movement.

- **Collsions and Ray Casting:** An infinte ray is casted perpendicular to the screen right from the middle of the crosshair when left mouse click event is registered. The item objects have colliders wraping their visible geometry. The ray collides with multiple items and the item collided with the ray that is closest to the screen is selected. You can then manually set the position of item selected. Once you select 2 items, a dialogue box appears where you can select the 2 faces you want to join and the items join on those faces. Pusher handler can be used to avoid merging of two items and push them away. But this feature isn't desirable. The collision between player and floor is handled using bullet collision which is different from the panda's built-in collision system. Collsion masks for bullet collision don't effect the panda3d's collision masks.

- **GUI:** The Inventroy and Crafting dialogue boxes are implemented in `Gui.py` where both dialogue boxes inherit from the Gui class which includes common properties and methods to help show mouse cursor when dialogue appears on screen. Cursor is hidden and mouse task is added again to `taskMgr` when dialogue box disappears from te screen. Same functionality is used in both child classes at appropriate places in the program.

- **Future Development:**
    - Reset rotation function call in `press_once()` should be implemented properly. Right now, it just takes the index 1 element of the list to reset its 'HPR' back to the original face orientations when `reset=True`. This probably is the reason why joining faces after rotating items sometimes shows unexpected results.
    - Some Save option for player's crafted model to save positions, names and rotations of items in permanent memory.
    - When pusher handler is active, items should collide with each other and stop moving into one another without bouncing or pushing back.
    - Collsion of items with player.
    - Rotation of items should be disabled along some given axis if rotation means collision with some collider. Be it floor, player or some other item.
    - If an item is being attached on some side where an item is already attached, there should be restriction to set the item to the face where both items do not intersect with each other.
    - In current version, `rotation_rules` are specified to rotate the item in certain ways before joining the faces to help ease the `Item.attach()` join faces just by specifying their name. However, this approach feels a bit inefficient.
    - Refactor and improve overall code's efficiency.