import pygame
import os
import gtts
from jnius import autoclass, PythonJavaClass, java_method
import requests
from plyer import notification



# Acesse as classes relevantes do Android
PythonActivity = autoclass('org.kivy.android.PythonActivity')
InputMethodManager = autoclass('android.view.inputmethod.InputMethodManager')
Context = autoclass('android.content.Context')



def App():
	return pygame
	
def Voz(string):
    voz = gtts.gTTS(string, lang='pt-br');
    voz.save('audio.mp3');
    pygame.mixer.music.load('audio.mp3');
    pygame.mixer.music.play();


class Interface:
    def __init__(self):
        self.app = pygame;
        self.app.init();
        self.app.mixer.init();
        self.clock = pygame.time.Clock();
    def Window(self, size, name:str):
        screen = self.app.display.set_mode(size);
        self.app.display.set_caption(name);
        return screen
    def Run(self,fps:int):
        self.app.display.flip()
        self.clock.tick(fps)
    def Popup(self,title:str,text:str):
        notification.notify(title=title,message=text)
    def Event_init(self):
        self.events = pygame.event.get()
        return self.events
    def Events(self, events):
        for event in events:
            if event.type == self.app.QUIT:
                self.app.quit()
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_BACKSPACE:
                    info = {'click':False,'event':event}
                    return info  # Remove o último caractere
            
                 else:
                    
                    info = {'click':False,'event':event}
                    return info
            if event.type == self.app.MOUSEBUTTONDOWN:
                info = {'click':True,'event':event}
                return info
            
class Image:
    def __init__(self,window,image_dir:str):
        self.window = window
        self.app = pygame;
        self.padding = {'x':100,'y':100};
        self.pos = {'x':0,'y':0};
        self.image = self.app.image.load(image_dir);
        self.image = self.app.transform.scale(self.image,(self.padding['x'],self.padding['y']))
        self.mask = self.app.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
    def Draw(self):
        self.image = self.app.transform.scale(self.image,(self.padding['x'],self.padding['y']))
        self.mask = self.app.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos['x'],self.pos['y']
        self.window.blit(self.image,self.rect.topleft)
        
class Music:
    def __init__(self, music_dir):
        self.app = pygame;
        self.music_dir = music_dir;
        self.app.mixer.music.load(self.music_dir);
    def Play(self,loop):
        if loop:
            self.app.mixer.music.play(-1);
        else:
            self.app.mixer.music.play();
            
class Div:
    def __init__(self,window):
        self.window = window;
        self.app = pygame;
        self.window = window;
        self.color = '#000000';
        self.padding = {'x':100,'y':50};
        self.pos={'x':0,'y':0};
        self.rect = None;
        self.radius = False;
        self.radius_size = 0;
    def Draw(self):
        self.rect = self.app.Rect(self.pos['x'],self.pos['y'],self.padding['x'],self.padding['y']);
        self.app.draw.rect(self.window, self.color,self.rect)
        
class Progress_Bar:
    def __init__(self,window, progress):
        self.window = window;
        self.app = pygame
        self.color = '#0AADDD'
        self.background = '#000000'
        self.pos = {'x':0,'y':0}
        self.padding = {'x':620,'y':40}
        if progress == None:
            self.progress = 0
        else:
            self.progress = progress
    def Draw(self):
        self.rect = self.app.Rect(self.pos['x'],self.pos['y'],self.padding['x'],self.padding['y']);
        self.rect_2 = self.app.Rect(self.pos['x']+5,self.pos['y']+7,self.progress,self.padding['y']-15);
        self.app.draw.rect(self.window, self.background,self.rect)
        self.app.draw.rect(self.window, self.color,self.rect_2)
        
class Text_Input:
    def __init__(self, window, text:str):
        self.window = window
        self.text = text;
        self.text_show = text
        if len(text) > 35:
            self.text_show = text[:len(text)//2]+'...'
        self.color = '#E4EAEC';
        self.text_color = '#000000';
        self.padding={'x':200,'y':50};
        self.pos = {'x':0,'y':0};
        self.font_size = 36
        self.text_style = None
        self.font = pygame.font.Font(self.text_style, self.text_size);
        self.rect = None;
        self.active = False;


    def Paste(self):
        context = autoclass('org.kivy.android.PythonActivity').mActivity
        clipboard_manager = context.getSystemService(Context.CLIPBOARD_SERVICE)
    
        if clipboard_manager.hasPrimaryClip():
            clip_data = clipboard_manager.getPrimaryClip()
            item = clip_data.getItemAt(0)
            clipboard_text = str(item.getText())
            return clipboard_text
        
        return None
    
    
    def OpenKeyBoard(self):
        context = PythonActivity.mActivity
        input_manager = context.getSystemService(Context.INPUT_METHOD_SERVICE)
        input_manager.toggleSoftInput(InputMethodManager.SHOW_FORCED, 0)
    
    def Draw(self):
        self.rect = pygame.Rect(self.pos['x'],self.pos['y'],self.padding['x'], self.padding['y']);
        pygame.draw.rect(self.window, self.color,self.rect);
        
        text_surface = self.font.render(self.text_show, True, self.text_color);
        self.window.blit(text_surface, (self.pos['x']+10, self.pos['y']+10));
        
        
      
        
class Label:
    def __init__(self,window):
        self.text = '';
        self.text_color = 'black';
        self.window = window;
        self.pos = {'x':0,'y':0};
        self.text_size = 36
        self.text_style = None
        
        self.font = pygame.font.Font(self.text_style, self.text_size);
   
    def Draw(self):
        text_surface = self.font.render(self.text, True, self.text_color);
        self.window.blit(text_surface, (self.pos['x'], self.pos['y']));
        
        
        
        
class Button:
    def __init__(self, window):
        pygame.sprite.Sprite.__init__(self)
        self.text = 'button';
        self.window = window;
        self.color = '#0AADDD';
        self.color_text = '#000000'
        self.padding = {'x':100,'y':40}
        self.pos = {'x': 0, 'y': 0};
        self.radius = False; 
        self.radius_size = 25
        self.rect = None;
        self.text_size = 36
        self.text_style = None
        ''
        self.active = False;
    
    def Draw(self):
        self.font = pygame.font.Font(self.text_style, self.text_size);
        self.rect = pygame.Rect(self.pos['x'],self.pos['y'],self.padding['x']+len(self.text*2),self.padding['y']);

        pygame.draw.rect(self.window, self.color, self.rect)
        if self.radius:
            pygame.draw.circle(self.window, self.color, (self.rect.left+5,self.rect.top+20),self.radius_size)
            pygame.draw.circle(self.window, self.color, (self.rect.right-5,self.rect.top+20),self.radius_size)
        if len(self.text) >= 15:
        	self.text = self.text[:len(self.text)//2]+'...'
        text_surface = self.font.render(self.text, True, self.color_text);
        self.text_num = len(self.text)
        self.window.blit(text_surface, (self.padding['x']-self.padding['x']//2-self.text_num*2, self.pos['y']+self.padding['y']//2-self.text_num*2));

if __name__ == '__main__':
    pass