import pygame

class Button():
	def __init__(self, pos, size, text, font):
		self.size = pygame.Vector2(size)
		self.pos = pygame.Vector2(pos) - self.size / 2
		self.font = font

		self.button_surface = pygame.Surface(size, pygame.SRCALPHA)
		self.button_surface.set_alpha(100)
		pygame.draw.rect(self.button_surface, (0,0,0), pygame.Rect((0,0), self.size))
		
		self.text_surface = self.font.render(text, True, (255, 255, 255))
		self.text_pos = pos - pygame.Vector2(self.text_surface.get_size()) / 2
		self.is_hovering = False

	def draw(self, surface: pygame.Surface):
		surface.blit(self.button_surface, self.pos)
		self.text_surface.set_alpha(255 if self.is_hovering else 150)
		surface.blit(self.text_surface, self.text_pos)

	def on_mouse_motion(self, mouse_pos: pygame.Vector2):
		self.is_hovering = self.pos.x < mouse_pos.x < self.pos.x + self.size.x \
			and self.pos.y < mouse_pos.y < self.pos.y + self.size.y
