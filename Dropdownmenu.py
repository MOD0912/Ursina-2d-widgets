import ursina as ur

class DropdownMenu(ur.Entity):
    """
    A dropdown menu for selecting options.
    
    Scale behaves kinda weird. it's a 4:1 ratio, so if you want a 1:1 scale, set it to (0.25, 0.0625)

    :text: The text displayed on the main button.
    :options: A list of options to display in the dropdown.
    :commands: A list of functions to execute when an option is selected, if not given, it will print the selected option.
    :position: The position of the dropdown menu in the world.
    :scale: The scale of the dropdown menu.
    :color: Not implemented. Why would you want to change the color?! It is beautiful as it is.
    :border: Whether to add a border around the dropdown menu.
    :lr_border: Whether to add a border on the left and right side of the dropdown menu. Is ignored if border is set to True.
    :change_color: Whether to change the color of the options in the dropdown menu. If set to True, it will alternate between #262626 and #333333.
    """
    def __init__(self, parent:ur.Entity=ur.scene, text:str="Select Option", options:list=["Option1", "Option2"], commands:list=[], position:tuple|int=(0, 0), scale:tuple|int=(4, 1), color:ur.color=ur.color.white, border:bool=True, lr_border:bool=True, change_color:bool=True, **kwargs):
        super().__init__(parent=parent, position=position, scale=scale)
        if type(position) == int:
            position = (position, position)
        else:
            if len(position) == 1:
                position = (position[0], position[0])
                
        if type(scale) == int:
            scale = (scale, scale/4)
        else:
            if len(scale) == 1:
                scale = (scale[0], scale[0]/4)  
                
        if scale[0] != 0 and scale[1] != 0:
            self.x_scale = scale[0]
            self.y_scale = scale[1]
        else:
            self.x_scale = 1
            self.y_scale = self.x_scale / 4
            
        self.scale = (self.x_scale/4, self.y_scale)
        self.button_text = text  # Store the text for the button
        self.border_value = border
        self.lr_border = lr_border
        self.options = options
        self.commands = commands
        color = "#262626"

        self.widget()
        # Create dropdown menu as a local entity with zero position offset
        # This ensures consistent positioning regardless of the parent's position
        self.dropdown_menu = ur.Entity(parent=self, enabled=False, position=(0, 0, 0))
        
        while len(self.options) > len(self.commands):
            self.commands.append(lambda: print(f"selected option {self.options[len(self.commands)]}"))
        if len(self.options) < len(self.commands):
            raise ValueError("More commands than options")
        for x, i in enumerate(map(lambda x, y: (x, y), self.options, self.commands)):
            if change_color:
                color = "#262626" if color == "#333333" else "#333333"
                print(color)
            c = ur.color.hex(color)
            self.add_option(i[0], i[1], x, c)
        num_options = len(self.options)
        
        if self.border_value:
            self.border((4, 0.1), (0, -1.1, -0.01))
            self.border((4, 0.1), (0, 0.1-(num_options + 1.2), -0.01)) 
            self.border((0.1, num_options + 0.1), (-4/2 -0.05, -(num_options + 0.2)/2 - 1, -0.01))
            self.border((0.1, num_options + 0.1), (4/2, -(num_options + 0.2)/2 - 1, -0.01))
            
        if not self.border_value and self.lr_border:
            self.border((0.1, num_options), (-4/2 -0.05, -(num_options + 0.2)/2 - 1, -0.01))
            self.border((0.1, num_options), (4/2, -(num_options + 0.2)/2 - 1, -0.01))


    def widget(self):
        bg = ur.Entity(parent=self, model=ur.Quad(aspect=1, radius=0.2, scale=(4, 1)), color="#5e5e5e", position=(0, 0, 0))
        fg = ur.Entity(parent=self, model=ur.Quad(aspect=1, radius=0.2, scale=(3.9, 0.9)), color="#333333", position=(0, 0, -0.001))
        self.text = ur.Text(
            parent=self,
            text=self.button_text,  # Use the text from the constructor
            color=ur.color.white,
            position=(-self.x_scale*(4/self.x_scale)*0.4375, 0, -0.002),
            origin=(-.5, 0),
            scale=self.x_scale*(4/self.x_scale)*3.75,
        )
        self.text.default_resolution = 1080 * self.text.size
        button = ur.Button(
            parent=self,
            model=ur.Quad(aspect=1, radius=0.2, scale=(1, 0.9)),
            text='v',
            text_size=self.x_scale*0.375,
            position=(self.x_scale*(4/self.x_scale)*0.37, 0, -0.002),
            color="#5e5e5e",
            on_click=self.toggle,
            highlight_color=ur.color.hex("#5e5e5e"),
        )
        
        

    def add_option(self, text, on_click, i, color):
        # Create a button for each option
        ur.Button(
            text=text,
            text_size=0.375*self.x_scale,
            parent=self.dropdown_menu,
            position=(0, -(i + 1.6), 0),  # Original button positioning
            scale=(4, 1),
            model='quad',
            color=color,  # Button color
            on_click=lambda text=text, on_click=on_click: self.on_option_selected(text, on_click),
        )

    def toggle(self):
        # Toggle the dropdown menu visibility
        self.dropdown_menu.enabled = not self.dropdown_menu.enabled
        
    def border(self, scale, position):
        """Create a border around the dropdown menu options"""

        border = ur.Entity(
            parent=self.dropdown_menu,
            model='quad',
            color=ur.color.white,
            scale=scale,  # Make it thicker for visibility
            position=position
        )
        
       
    def on_option_selected(self, option, command):
        # Execute the corresponding command if it exists
        index = self.options.index(option)
        if index < len(self.commands) and self.commands[index]:
            self.commands[index]()
        # Close the dropdown menu after selection
        self.text.text = option
        self.dropdown_menu.enabled = False
    
        command()

if __name__ == '__main__':
    app = ur.Ursina()
    ur.window.title = 'Dropdown Menu Example'
    main_button = DropdownMenu(
        text="Select Option",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        commands=[
            lambda: print("Option 1 selected"),
            lambda: print("Option 2 selected"),
            lambda: print("Option 3 selected"),
            lambda: print("Option 4 selected"),

        ],
        position=(3, 3),
        scale=(2, 0.5),
        color="#555555",
        border=True,
        lr_border=True,
    )
    main_button = DropdownMenu(
        text="Select Option",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        commands=[
            lambda: print("Option 1 selected"),
            lambda: print("Option 2 selected"),
            lambda: print("Option 3 selected"),
            lambda: print("Option 4 selected"),

        ],
        position=(0),
        scale=2,
        color="#555555",
        border=False,
        lr_border=True,
        change_color=False,

    )

    app.run()
