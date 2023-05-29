import pygame
import sys
import os
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ZOMBLAZE")

# Load assets
asset_path = "assets"
background_image = pygame.image.load(os.path.join(asset_path, "back.png"))

# Font
font_title = pygame.font.Font(None, 60)
font_menu = pygame.font.Font(None, 40)

# Membuat teks judul
title_text = font_title.render("ZOMBLAZE", True, (255, 255, 255))
title_text_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))

# Membuat teks menu
menu_texts = ["New Game", "Continue", "Exit Game"]
menu_text_surfaces = []
menu_text_rects = []
for i, text in enumerate(menu_texts):
    text_surface = font_menu.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + i * 60))
    menu_text_surfaces.append(text_surface)
    menu_text_rects.append(text_rect)

# Load karakter
character_path = "assets/images/karakter"
character_image = pygame.image.load(os.path.join(character_path, "PMC_Stand.bmp"))
character_rect = character_image.get_rect(center=(screen_width // 2, screen_height // 2))

# Load zombie
zombie_path = "assets/images/zombies"
zombie_image = pygame.image.load(os.path.join(zombie_path, "zombie1.png"))
zombie_image = pygame.transform.scale(zombie_image, character_rect.size)  # Mengubah ukuran zombie menjadi sama dengan karakter

# Kecepatan karakter dan zombie
character_speed = 1
zombie_speed = character_speed

# Status tombol
key_status = {
    pygame.K_w: False,
    pygame.K_a: False,
    pygame.K_s: False,
    pygame.K_d: False
}

# Fungsi untuk menampilkan menu
def show_menu():
    screen.fill((0, 0, 0))

    # Menampilkan teks judul
    screen.blit(title_text, title_text_rect)

    # Menampilkan teks menu
    for i in range(len(menu_texts)):
        screen.blit(menu_text_surfaces[i], menu_text_rects[i])

    pygame.display.flip()

# pause menu teks
pause_text = font_menu.render("Pause Menu", True, (255, 255, 255))
pause_text_rect = pause_text.get_rect(center=(screen_width // 2, screen_height // 4))
resume_text = font_menu.render("Resume", True, (255, 255, 255))
resume_text_rect = resume_text.get_rect(center=(screen_width // 2, screen_height // 2))
save_text = font_menu.render("Save Game", True, (255, 255, 255))
save_text_rect = save_text.get_rect(center=(screen_width // 2, screen_height // 2 + 60))
exit_text = font_menu.render("Exit", True, (255, 255, 255))
exit_text_rect = exit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 120))

# Fungsi untuk menampilkan menu saat tombol Esc ditekan
def show_pause_menu():
    screen.fill((0, 0, 0))
    screen.blit(pause_text, pause_text_rect)
    screen.blit(resume_text, resume_text_rect)
    screen.blit(save_text, save_text_rect)
    screen.blit(exit_text, exit_text_rect)
    pygame.display.flip()

# Loop utama
running = True
menu_active = True
pause_menu_active = False
new_game_selected = False  # Menandakan apakah tombol New Game sudah dipilih
zombie_timer = pygame.time.get_ticks()  # Timer untuk spawn zombie
zombies = []  # Daftar zombie yang muncul
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_active:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(len(menu_text_rects)):
                    if menu_text_rects[i].collidepoint(mouse_pos):
                        if i == 0:  # New Game
                            menu_active = False
                            new_game_selected = True
                            screen = pygame.display.set_mode((screen_width, screen_height))
                            pygame.display.flip()
                            # Tulis kode untuk memulai permainan di sini
                        elif i == 1:  # Continue
                            print("Melanjutkan permainan...")
                            # Tulis kode untuk melanjutkan permainan di sini
                        elif i == 2:  # Exit Game
                            print("Keluar dari permainan...")
                            running = False
                            pygame.quit()
                            sys.exit()
            elif pause_menu_active:
                mouse_pos = pygame.mouse.get_pos()
                if resume_text_rect.collidepoint(mouse_pos):
                    pause_menu_active = False
                elif save_text_rect.collidepoint(mouse_pos):
                    print("Save game...")
                    # Tulis kode untuk menyimpan permainan di sini
                elif exit_text_rect.collidepoint(mouse_pos):
                    menu_active = True
                    pause_menu_active = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not menu_active:
                    if pause_menu_active:
                        pause_menu_active = False
                    else:
                        pause_menu_active = True
            elif event.key in key_status:
                key_status[event.key] = True

        elif event.type == pygame.KEYUP:
            if event.key in key_status:
                key_status[event.key] = False

    if menu_active:
        show_menu()
    elif pause_menu_active:
        show_pause_menu()
    else:
        screen.fill((0, 0, 0))
        if new_game_selected:
            screen.blit(background_image, (0, 0))

        # Pergerakan karakter
        character_dx = 0
        character_dy = 0

        if key_status[pygame.K_w]:
            character_dy -= character_speed
        if key_status[pygame.K_a]:
            character_dx -= character_speed
        if key_status[pygame.K_s]:
            character_dy += character_speed
        if key_status[pygame.K_d]:
            character_dx += character_speed

        character_rect.x += character_dx
        character_rect.y += character_dy

        screen.blit(character_image, character_rect)

        # Spawning zombie
        current_time = pygame.time.get_ticks()
        if current_time - zombie_timer >= 60000:  # Muncul 1-2 zombie setiap 1 menit
            zombie_timer = current_time
            num_zombies = random.randint(1, 2)
            for _ in range(num_zombies):
                zombie_rect = zombie_image.get_rect()
                zombie_rect.center = (character_rect.x + random.randint(-50, 50), character_rect.y + random.randint(-50, 50))
                zombies.append(zombie_rect)

        # Pergerakan zombie
        for zombie_rect in zombies:
            if zombie_rect.x < character_rect.x:
                zombie_rect.x += zombie_speed
            elif zombie_rect.x > character_rect.x:
                zombie_rect.x -= zombie_speed
            if zombie_rect.y < character_rect.y:
                zombie_rect.y += zombie_speed
            elif zombie_rect.y > character_rect.y:
                zombie_rect.y -= zombie_speed

            screen.blit(zombie_image, zombie_rect)

        pygame.display.flip()
