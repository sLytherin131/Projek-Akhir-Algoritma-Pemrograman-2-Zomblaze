import pygame
import sys

# Inisialisasi pygame
pygame.init()

# Ukuran layar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ZOMBLAZE")

# Warna
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Font
font_title = pygame.font.Font(None, 60)
font_menu = pygame.font.Font(None, 40)

# Membuat teks judul
title_text = font_title.render("ZOMBLAZE", True, WHITE)
title_text_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))

# Membuat teks menu
menu_texts = ["New Game", "Continue", "Exit Game"]
menu_text_surfaces = []
menu_text_rects = []
for i, text in enumerate(menu_texts):
    text_surface = font_menu.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + i * 60))
    menu_text_surfaces.append(text_surface)
    menu_text_rects.append(text_rect)

# Loop utama
running = True
while running:
    # Mengatur warna latar belakang
    screen.fill(RED)

    # Menampilkan teks judul
    screen.blit(title_text, title_text_rect)

    # Menampilkan teks menu
    for i in range(len(menu_texts)):
        screen.blit(menu_text_surfaces[i], menu_text_rects[i])

    # Memperbarui tampilan layar
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(menu_text_rects)):
                if menu_text_rects[i].collidepoint(mouse_pos):
                    if i == 0:  # New Game
                        print("Memulai permainan baru...")
                        # Tulis kode untuk memulai permainan di sini
                    elif i == 1:  # Continue
                        print("Melanjutkan permainan...")
                        # Tulis kode untuk melanjutkan permainan di sini
                    elif i == 2:  # Exit Game
                        print("Keluar dari permainan...")
                        running = False
                        pygame.quit()
                        sys.exit()
