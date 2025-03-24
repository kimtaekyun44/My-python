import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Penguin Running in Antarctica")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)  # 하늘색

# 펭귄 이미지 로드
penguin_img = pygame.image.load("penguin.webp")  # 펭귄 이미지 파일 경로
penguin_img = pygame.transform.scale(penguin_img, (100, 100))

# 배경 이미지 로드
background_img = pygame.image.load("antarctica.png")  # 남극 배경 이미지 경로
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 펭귄 초기 위치
penguin_x = 50
penguin_y = SCREEN_HEIGHT - 150
penguin_speed = 5

# 메인 루프
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 업데이트
    screen.blit(background_img, (0, 0))  # 배경 그리기

    # 펭귄 이동
    penguin_x += penguin_speed
    if penguin_x > SCREEN_WIDTH:
        penguin_x = -100  # 화면 밖으로 나가면 다시 시작

    # 펭귄 그리기
    screen.blit(penguin_img, (penguin_x, penguin_y))

    # 화면 새로고침
    pygame.display.flip()

    # 프레임 설정
    clock.tick(30)

# 종료
pygame.quit()
sys.exit()
