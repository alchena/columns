#Alan Chen 16976197
#columnsgame_view
import pygame
import columns_model

class ColumnsGame():
    def __init__(self):
        self._running = True
        #contains all the information needed for the view
        self._state = columns_model.ColumnsState()
        
    def run(self) -> None:
        '''
        Main loop for playing the game
        '''
        pygame.init()

        try:
            #initial size of 600,600
            self._resize_display((600,600))
            clock = pygame.time.Clock()
            
            while self._running:
                #running at a low framerate, 30 frames was too fast
                clock.tick(1)
                self._handle_events()
                self._redraw()
                
        #ends the game whenever a game over error is raised
        except columns_model.GameOver:
            #stops the self._running loop
            self._end_game()
            
            #drawing game over message
            surface = pygame.display.get_surface()
            self._draw_game_over_message(surface)
            pygame.display.flip()

            #the display is kept open until the
            #user closes the program
            try:
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
            finally:
                pygame.quit()
                    
                
        finally:
            pygame.quit()
                



    def _resize_display(self, size: (int,int)) -> None:
        '''
        Makes it so that you can resize the display
        '''
        pygame.display.set_mode(size, pygame.RESIZABLE)
        
    def _handle_events(self) -> None:
        '''
        Handles only 4 events, left and right arrow,
        space bar, and clicking on the exit button.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #rotates faller if spacebar is pressed
                self._state.rotate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                #moves the faller to the right if the right arrow key is pressed
                self._state.move_right()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                #moves the faller to the left if left arrow key is pressed
                self._state.move_left()
                
        #if no events the faller continues to fall
        self._state.tick()

            
    def _end_game(self) -> None:
        '''
        Stops the game from running
        '''
        self._running = False

    def _redraw(self) -> None:
        '''
        draws the board to the pygame display
        '''
        surface = pygame.display.get_surface()

        surface.fill(pygame.Color(128,128, 128))
        self._draw_jewels()
        
        pygame.display.flip()

    def _draw_jewels(self) -> None:
        '''
        loops through a list that contains Jewel objects
        and calls _draw_jewels on them
        '''
        for jewel in self._state.all_jewels():
            self._draw_jewel(jewel)
            
    def _draw_jewel(self, jewel: columns_model.Jewel) -> None:
        '''
        Converts the fractional coordinates found in the Jewel Object
        to pixel coordinates, and creates a rectangle given
        the information by the Jewel object.
        '''
        #values needed for pixel coord. conversion
        surface = pygame.display.get_surface()
        surface_height = surface.get_height()
        surface_width = surface.get_width()

        #top left fractional coordinates        
        topleft_frac_x, topleft_frac_y = jewel.top_left_coord()

        #fractional width and height of the rectangle        
        frac_width = jewel.width()
        frac_height = jewel.height()

        #color of the rectangle
        jewel_color_r, jewel_color_g, jewel_color_b = jewel.color()

        #conversions
        topleft_pixel_x = topleft_frac_x * surface_width
        topleft_pixel_y = topleft_frac_y * surface_height
        pixel_width = frac_width * surface_width
        pixel_height = frac_height * surface_height

        #creating the rectangle
        jewel_rect = pygame.Rect(
            topleft_pixel_x, topleft_pixel_y,
            pixel_width, pixel_height)

        #drawing rhe rectangle
        pygame.draw.rect(
            surface,
            pygame.Color(jewel_color_r, jewel_color_g, jewel_color_b),
            jewel_rect)       

    def _draw_game_over_message(self, surface: pygame.Surface):
        '''
        Draws the words gameover to the top left corner of the display
        '''
        font = pygame.font.SysFont(None, 24)
        text_image = font.render('GAMEOVER', True, pygame.Color(255, 255, 255))
        surface.blit(text_image, (10, 10))
        
if __name__ == "__main__":
    ColumnsGame().run()
