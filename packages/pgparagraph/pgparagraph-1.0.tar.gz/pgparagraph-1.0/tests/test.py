from pgparagraph import Paragraph, ModifierName, TextAlign
import pygame, sys

W, H, BG = 1200,800, [30]*3
pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.Clock()

string = "ciao ciao ciao\ncioa sd ad sa\nhdkjsa\nh dhask hdkas <b><m fs=50>hdkjsah dkashd</m></b> k\nasdh ashk\nda shhdkas dka"
paragraph = Paragraph(string,align=TextAlign.right, start_i=0, end_i=-1)
paragraph.modifiers_holder.add_modifier(ModifierName.fg_color, 10, 42, (0,255,0))
paragraph.modifiers_holder.add_modifier(ModifierName.font_size, 40,45, 80)
paragraph.parse_rich_text()

surf, rect, data = paragraph.render(wraplength=300, get_chars_data=False)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill(BG)
    
    rect.topleft = (20,20)
    screen.blit(surf, rect)
    
    clock.tick(0)
    pygame.display.flip()
    pygame.display.set_caption(f"{clock.get_fps():.0f} FPS")