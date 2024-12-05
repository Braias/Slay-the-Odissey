import pygame.mixer as pm


pm.init()

hit = pm.Sound(file="assets/hitHurt.wav")

victory = pm.Sound(file="sounds/victory_sound.wav")
victory.play()