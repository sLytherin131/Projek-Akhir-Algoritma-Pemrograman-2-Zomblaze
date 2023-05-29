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

# Load backsound
backsound_path = "assets/sounds/backsound.mp3"
pygame.mixer.music.load(backsound_path)
pygame.mixer.music.set_volume(0.5)  # Set volume ke 50%
pygame.mixer.music.play(-1)  # Putar backsound secara berulang

# Load assets
asset_path = "C:/Users/Acer/Documents/Projek UAS/assets/images"
main_menu_image = pygame.image.load(os.path.join(asset_path, "mainmenu.png"))
background_image = pygame.image.load(os.path.join(asset_path, "Sample.png"))
pause_menu_image = pygame.image.load(os.path.join(asset_path, "mainmenu.png"))

# Font
font_title = pygame.font.Font(None, 60)
font_menu = pygame.font.Font(None, 40)
font_hp = pygame.font.Font(None, 30)

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
character_image = pygame.image.load(os.path.join(character_path, "PMC_Stand.png"))
character_rect = character_image.get_rect(center=(screen_width // 2, screen_height // 2))

# Load zombie
zombie_path = "assets/images/zombies"
zombie_image = pygame.image.load(os.path.join(zombie_path, "zombie1.png"))
zombie_image = pygame.transform.scale(zombie_image, character_rect.size)  # Mengubah ukuran zombie menjadi sama dengan karakter

# Load health bar
health_bar_width = 200
health_bar_height = 20
health_bar_outer_rect = pygame.Rect(10, screen_height - health_bar_height - 10, health_bar_width, health_bar_height)
health_bar_inner_rect = health_bar_outer_rect.inflate(-6, -6)

# Kecepatan karakter dan zombie
character_speed = 1
zombie_speed = 1

# Status tombol
key_status = {
    pygame.K_w: False,
    pygame.K_a: False,
    pygame.K_s: False,
    pygame.K_d: False
}

# Fungsi untuk menampilkan menu
def show_menu():
    screen.blit(main_menu_image, (0, 0))
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

# Fungsi untuk mendapatkan posisi acak di sekitar player
def get_random_position_around_player(player_rect):
    x = player_rect.x + random.randint(-100, 100)
    y = player_rect.y + random.randint(-100, 100)
    return x, y

# Fungsi untuk mengurangi health point player
def decrease_player_health(amount):
    global player_hp
    player_hp -= amount
    if player_hp < 0:
        player_hp = 0

# Fungsi untuk mendeteksi tabrakan antara dua objek (player dan zombie)
def detect_collision(player_rect, zombie_rect):
    return player_rect.colliderect(zombie_rect)

# Loop utama
running = True
menu_active = True
pause_menu_active = False
new_game_selected = False  # Menandakan apakah tombol New Game sudah dipilih
zombie_timer = pygame.time.get_ticks()  # Timer untuk spawn zombie
zombies = []  # Daftar zombie yang muncul
player_hp = 100  # Health Point awal
collision_timer = 0  # Timer untuk mengatur waktu antara tabrakan dengan zombie
collision_cooldown = 1000  # Waktu cooldown antara tabrakan dengan zombie (dalam milidetik)
portal_active = False  # Menandakan apakah portal aktif atau tidak
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
        screen.fill((0, 0, 0))
        menu_background_image = pygame.image.load("C:/Users/Acer/Documents/Projek UAS/assets/images/mainmenu.png")
        screen.blit(menu_background_image, (0, 0))

        # Menampilkan teks judul
        screen.blit(title_text, title_text_rect)

        # Menampilkan teks menu
        for i in range(len(menu_texts)):
            screen.blit(menu_text_surfaces[i], menu_text_rects[i])

        pygame.display.flip()
    elif pause_menu_active:
        show_pause_menu()
    elif new_game_selected:
        screen.fill((0, 0, 0))
        
        # Check if player position reaches the new biome
        if character_rect.x > 758 and character_rect.y < -8:
            # Reset player position and clear zombies
            character_rect.x = screen_width // 2
            character_rect.y = screen_height // 2
            zombies = []
            # Set new background image
            background_image = pygame.image.load(os.path.join(asset_path, "new_biome.png"))

        screen.blit(background_image, (0, 0))

        # Menggerakkan karakter
        if key_status[pygame.K_w]:
            character_rect.y -= character_speed
        if key_status[pygame.K_s]:
            character_rect.y += character_speed
        if key_status[pygame.K_a]:
            character_rect.x -= character_speed
        if key_status[pygame.K_d]:
            character_rect.x += character_speed
            
        # Mendapatkan posisi x dan y player
        player_x = character_rect.x
        player_y = character_rect.y

        print("Player position:", player_x, player_y)
        
        # Cek jika pemain memasuki daerah portal
        if player_x > 758 and player_y < -8:
            portal_active = True

        # Menggambar karakter
        screen.blit(character_image, character_rect)

        # Menggambar zombie
        for zombie_rect in zombies:
            screen.blit(zombie_image, zombie_rect)

        # Menggambar health bar
        pygame.draw.rect(screen, (255, 0, 0), health_bar_outer_rect)
        pygame.draw.rect(screen, (0, 255, 0), health_bar_inner_rect)

        # Menampilkan health point player
        hp_text = font_hp.render(f"HP: {player_hp}", True, (255, 255, 255))
        hp_text_rect = hp_text.get_rect(center=(health_bar_outer_rect.centerx, health_bar_outer_rect.centery))
        screen.blit(hp_text, hp_text_rect)

        pygame.display.flip()

        # Menghasilkan zombie secara acak
        current_time = pygame.time.get_ticks()
        if current_time - zombie_timer >= 3000:
            zombie_x, zombie_y = get_random_position_around_player(character_rect)
            zombie_rect = zombie_image.get_rect(center=(zombie_x, zombie_y))
            zombies.append(zombie_rect)
            zombie_timer = current_time

        # Memeriksa tabrakan dengan zombie
        if not portal_active:
            for zombie_rect in zombies:
                if detect_collision(character_rect, zombie_rect):
                    if current_time - collision_timer >= collision_cooldown:
                        decrease_player_health(10)
                        collision_timer = current_time

        # Menangani kematian pemain
        if player_hp <= 0:
            print("Game Over")
            new_game_selected = False
            menu_active = True
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.flip()
            # Tulis kode untuk menampilkan layar game over di sini

    pygame.display.update()
    
# Hentikan backsound dan bersihkan sumber daya audio
pygame.mixer.music.stop()
pygame.mixer.quit()