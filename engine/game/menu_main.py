import webbrowser

browser = webbrowser.get()


def menu_main(self):
    if self.start_game_button.event:  # preset map list menu
        self.start_battle("1", "1", "1")

    elif self.quit_button.event or self.esc_press:  # open quit game confirmation input
        self.activate_input_popup(("confirm_input", "quit"), "Quit Game?", self.confirm_ui_popup)
