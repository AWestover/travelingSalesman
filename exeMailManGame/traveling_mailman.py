# Check packages_states or whatever to fix ai bug
# Add postal service mandatory start point?

import pygame
import sys
import os
import numpy as np
from pygame.locals import *
import random
import time

from os.path import join

mail_box_dims = [100, 100]
screen_dims = [1400, 700]
screen_color = [10, 255, 255]
images_loc = "PythonImagesAndVideos"
man_img_paths = []
for i in range(1, 5):
    man_img_paths.append(os.path.join(images_loc, "mailman" + str(i) + ".png"))
mail_img_paths = [os.path.join(images_loc, "mailboxbefore.png"), os.path.join(images_loc, "mailboxafter.png")]
fire_dims = [100, 100]
fire_img_path = os.path.join(images_loc, "fire.png")
robot_img_paths = []
for i in range(1, 5):
    robot_img_paths.append(os.path.join(images_loc, "robot" + str(i) + ".png"))
box_img_path = os.path.join(images_loc, "box.png")
box_dims = [100, 100]
logo_path = os.path.join(images_loc, 'logo.jpg')
logo_image = pygame.image.load(logo_path)
postal_path = os.path.join(images_loc, 'postoffice.png')
post_office_image = pygame.image.load(postal_path)
post_office_dims = [235, 142]
post_office_loc = [0, screen_dims[1]*0.1]
post_office_center = [post_office_loc[0] + post_office_dims[0]/2, post_office_loc[1] + post_office_dims[1]/2]
map_img_loc = os.path.join(images_loc, 'background.jpg')
map_image = pygame.image.load(map_img_loc)


def collide_post_office(pos, dims):
    beg_x_in = int(post_office_loc[0]) <= int(pos[0]) <= int(post_office_loc[0]) + int(post_office_dims[0])
    beg_y_in = int(post_office_loc[1]) <= int(pos[1]) <= int(post_office_loc[1]) + int(post_office_dims[1])
    end_x_in = int(post_office_loc[0]) <= int(pos[0]) + int(dims[0]) <= int(post_office_loc[0]) + int(post_office_dims[0])
    end_y_in = int(post_office_loc[1]) <= int(pos[1]) + int(dims[1]) <= int(post_office_loc[1]) + int(post_office_dims[1])
    if (beg_x_in or end_x_in) and (beg_y_in or end_y_in):
        return True
    else:
        return False


class MailMan(object):
    def __init__(self):
        self.pos = [screen_dims[0]/2, screen_dims[1]/2]
        self.pos = post_office_center[:]
        self.vel = [0, 0]
        self.thrust = 0.001
        self.dims = [50, 70]
        self.images = [pygame.image.load(man_img_paths[i]) for i in range(0, 4)]
        self.images = [pygame.transform.scale(self.images[i], (self.dims[0], self.dims[1])) for i in range(0, 4)]
        for i in range(0, 4):
            self.images.append(pygame.transform.flip(self.images[i], True, False)) #backkwards
        self.ani_scene = 3
        self.animating = 0

    def check_keys(self):
        self.animating = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]: # down key
            self.vel[1] = self.thrust # move down
        elif key[pygame.K_UP]: # up key
            self.vel[1] = -1*self.thrust # move up
        if key[pygame.K_RIGHT]: # right key
            self.animating = 8
            self.vel[0] = self.thrust # move right
        elif key[pygame.K_LEFT]: # left key
            self.animating = 4
            self.vel[0] = -1*self.thrust # move left
        if key[pygame.K_e]:
            pygame.quit()
            sys.exit()
        elif key[pygame.K_p]:
            self.vel = [0, 0]
        if key[pygame.K_f]:
            self.thrust = 0.004
        if key[pygame.K_s]:
            self.thrust = 0.001

    def draw(self, surface):
        surface.blit(self.images[int(self.ani_scene)], (self.pos[0], self.pos[1]))

    def update(self, dt):
        if (self.pos[0] > 0 or self.vel[0] > 0) and (self.pos[0] < screen_dims[0] - self.dims[0] or self.vel[0] < 0):
            self.pos[0] += dt*self.vel[0]
        if (self.pos[1] > 0 or self.vel[1] > 0) and (self.pos[1] < screen_dims[1] - self.dims[1] or self.vel[1] < 0):
            self.pos[1] += dt*self.vel[1]
        self.vel = np.multiply(self.vel, 0.7)
        if self.animating != 0:
            if self.animating == 8:
                self.ani_scene = (self.ani_scene + 0.01) % 4 + 4
            elif self.animating == 4:
                self.ani_scene = (self.ani_scene + 0.01) % 4
        else:
            self.ani_scene = 3


class Mailbox(object):
    def __init__(self, pos, dims):
        self.pos = pos
        self.dims = dims
        self.images = [pygame.image.load(mail_img) for mail_img in mail_img_paths]
        self.images = [pygame.transform.scale(self.images[i], (int(dims[0]), int(dims[1]))) for i in range(0,2)]
        self.state = 0

    def collide(self, pos, dims, player):
        beg_x_in = int(self.pos[0]) <= int(pos[0]) <= int(self.pos[0]) + int(self.dims[0])
        beg_y_in = int(self.pos[1]) <= int(pos[1]) <= int(self.pos[1]) + int(self.dims[1])
        end_x_in = int(self.pos[0]) <= int(pos[0]) + int(dims[0]) <= int(self.pos[0]) + int(self.dims[0])
        end_y_in = int(self.pos[1]) <= int(pos[1]) + int(dims[1]) <= int(self.pos[1]) + int(self.dims[1])
        if (beg_x_in or end_x_in) and (beg_y_in or end_y_in):
            if player == 'mailman':
                self.state = 1
            return True
        else:
            return False

    def draw(self, surface):
        surface.blit(self.images[self.state], (self.pos[0], self.pos[1]))


def draw_box(pos, dims, surface):
    box_image = pygame.image.load(box_img_path)
    box_image = pygame.transform.scale(box_image, (int(dims[0]), int(dims[1])))
    surface.blit(box_image, (pos[0], pos[1]))


class Fire(object):
    def __init__(self, pos, dims):
        self.pos = pos
        self.dims = dims
        self.image = pygame.image.load(fire_img_path)
        self.image = pygame.transform.scale(self.image, (int(dims[0]), int(dims[1])))

    def collide(self, mailman_pos, mailman_dims):
        beg_x_in = self.pos[0] < mailman_pos[0] < self.pos[0] + self.dims[0]
        beg_y_in = self.pos[1] < mailman_pos[1] < self.pos[1] + self.dims[1]
        end_x_in = self.pos[0] < mailman_pos[0] + mailman_dims[0] < self.pos[0] + self.dims[0]
        end_y_in = self.pos[1] < mailman_pos[1] + mailman_dims[1] < self.pos[1] + self.dims[1]
        if (beg_x_in or end_x_in) and (beg_y_in or end_y_in):
            return True
        else:
            return False

    def draw(self, surface):
        surface.blit(self.image, (self.pos[0], self.pos[1]))


def a_to_b_vels(vel_tot, pta, ptb):
    a = (ptb[0]-pta[0])
    b = (ptb[1]-pta[1])
    c = np.linalg.norm([a, b]) + 1
    return [vel_tot*a/c, vel_tot*b/c]


def gen_distances(points: list) -> list:  # kinda like an adjacency matrix, really redundant
    return [[np.linalg.norm(np.subtract(pt1, pt2)) for pt2 in points] for pt1 in points]


def switcher(path, num_towns, pt_dists):
    for i in range(0, num_towns):
        for j in range(0, num_towns):
            seg1 = [path[i], path[i+1]]
            seg2 = [path[j], path[j+1]]
            if seg1[0] != seg2[0] and seg1[0] != seg2[1] and seg2[0] != seg1[1]:
                # no mods necessary because must go back to start, ie len(path) = num_towns +1
                # fix more efficent distance calculations
                # original_dist = pt_dists[seg1[0]][seg1[1]] + pt_dists[seg2[0]][seg2[1]]
                # new_dist = pt_dists[seg1[0]][seg2[1]] + pt_dists[seg2[0]][seg1[1]]
                original_dist_stupid = path_dist(path, pt_dists)
                proposed_path = index_switcher(path, i+1, j+1)
                new_dist_stupid = path_dist(proposed_path, pt_dists)
                if original_dist_stupid > new_dist_stupid:
                    path = proposed_path
    return path


def path_dist(path: list, pt_dists: list) -> float or int:
    total_dist = 0
    for i in range(0, len(path)-1):
        total_dist += pt_dists[path[i]][path[i+1]]
    total_dist += pt_dists[path[-1]][path[0]]
    return total_dist


def smallest_positive(array: list, used: list) -> int:
    min_val = np.inf
    for i in range(0, len(array)):
        if min_val > array[i] > 0 and i not in used:
            min_val = array[i]
    if min_val in array:
        return array.index(min_val)
    else:
        return None


def index_switcher(path, i, j):
    out_path = path[:]
    out_path[i] = path[j]
    out_path[j] = path[i]
    return out_path


class AiRacer(object):
    def __init__(self):
        self.pos = [screen_dims[0]/2, screen_dims[1]/2]
        self.pos = post_office_center[:]
        self.vel = [0, 0]
        self.thrust = 0.0003
        self.dims = [50, 70]
        self.images = [pygame.image.load(robot_img_paths[i]) for i in range(0, 4)]
        self.images = [pygame.transform.scale(self.images[i], (self.dims[0], self.dims[1])) for i in range(0, 4)]
        for i in range(0, 4):
            self.images.append(pygame.transform.flip(self.images[i], True, False))
        self.ani_scene = 3
        self.animating = 0

    def move_sequence(self, mailboxes):
        self.animating = 0
        pts = [[a_mail_box.pos[0] + mail_box_dims[0]/2, a_mail_box.pos[1] + mail_box_dims[1]/2] for a_mail_box in mailboxes]
        pts = [post_office_loc] + pts
        pt_dists = gen_distances(pts)
        path = [0]
        for i in range(0, len(pts)-1):
            path.append(smallest_positive(pt_dists[path[-1]], path))
        path.append(0)
        path = switcher(path, len(pts), pt_dists)
        greedy_points_order = [path[i] for i in range(0, len(pts))] + [path[0]]
        return greedy_points_order[1:len(greedy_points_order)]

    def draw(self, surface):
        surface.blit(self.images[int(self.ani_scene)], (self.pos[0], self.pos[1]))

    def update(self, dt):
        if self.vel[0] < 0:
            self.animating = 4
        if self.vel[0] > 0:
            self.animating = 8
        if (self.pos[0] >= 0 or self.vel[0] >= 0) and (self.pos[0] <= screen_dims[0] - self.dims[0] or self.vel[0] <= 0):
            self.pos[0] += dt*self.vel[0]
        if (self.pos[1] >= 0 or self.vel[1] >= 0) and (self.pos[1] <= screen_dims[1] - self.dims[1] or self.vel[1] <= 0):
            self.pos[1] += dt*self.vel[1]
        if self.animating != 0:
            if self.animating == 8:
                self.ani_scene = (self.ani_scene + 0.01) % 4 + 4
            elif self.animating == 4:
                self.ani_scene = (self.ani_scene + 0.01) % 4
        else:
            self.ani_scene = 3

    def gen_vel(self, packages_states, ai_path):
        ai_center = [self.pos[0] + self.dims[0]/2, self.pos[1] + self.dims[1]/2]
        if False in packages_states:
            next_town = packages_states.index(False)
            self.vel = a_to_b_vels(self.thrust, ai_center, [ai_path[next_town][0], ai_path[next_town][1]])
            return self.vel
        elif False not in packages_states and not ai_returned:
            next_town = -1
            self.vel = a_to_b_vels(self.thrust, ai_center, [ai_path[next_town][0], ai_path[next_town][1]])
            return self.vel


def end_program():
    pygame.quit()
    sys.exit()
    return False


def generate_level(number):
    mailboxes = []
    num_boxes = number  # Adjust later
    for i in range(0, num_boxes):
        mailboxes.append(Mailbox([random.randint(screen_dims[0]*0.1, screen_dims[0]*0.9), random.randint(screen_dims[1]*0.1, screen_dims[1]*0.9)], mail_box_dims))
    fires = []
    for i in range(0, int(num_boxes/2)):
        fires.append(Fire([random.randint(screen_dims[0]*0.1, screen_dims[0]*0.9), random.randint(screen_dims[1]*0.1, screen_dims[1]*0.9)], fire_dims))
    ai_speed = np.arctan(number)*0.0007*0.5
    return [mailboxes, fires, ai_speed]


def display_scene(mailboxes, fires, scene, surface, number):
    draw_text('Level : ' + str(number), font, surface, 25, 5, (200, 100, 20))
    for mailbox in mailboxes:
        mailbox.draw(surface)
    for fire in fires:
        fire.draw(surface)


def advance_level(mail_box_states, returned):
    if False not in mail_box_states and returned:
        return 1
    else:
        return 0


def draw_text(display_string, font, surface, xpos, ypos, color):
    text_display = font.render(display_string, 1, color)
    text_rect = text_display.get_rect()
    text_rect.topleft = (xpos, ypos)
    surface.blit(text_display, text_rect)


pygame.init()
window = pygame.display.set_mode((screen_dims[0], screen_dims[1]), RESIZABLE)
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)
mailman = MailMan()
ai = AiRacer()
clock = pygame.time.Clock()
dt = 1500
running = True
number = 0
returned = True
ai_returned = True
mail_box_states = []
scene = 'start'
pygame.mixer.music.load(os.path.join(images_loc, "MailmanSongLong.mp3"))
pygame.mixer.music.play(-1)

while running:
    window.fill((screen_color[0], screen_color[1], screen_color[2]))
    # handle every event since the last frame.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = end_program()

    if scene == 'start':
        window.fill((0, 255, 0))
        draw_text('Hello. You are a mailman.', font, window, 25, 5, (2, 3, 240))
        draw_text('Your job is to visit a lot of mailboxes and deliver the mail to them.', font, window, 25, 35, (2, 3, 240))
        draw_text('Avoid the fires, they will kill you. Also you must complete the mail route before your competitor VPS does or you will die of starvation.', font, window, 25, 65, (2, 3, 240))
        draw_text('Simple walk to each mail box to drop the mail, but beware, you must take an efficient route or you may not win...', font, window, 25, 95, (2, 3, 240))
        draw_text('(This game was inspired by the classic traveling salesman problem)', font, window, 25, 155, (2, 3, 240))
        draw_text('Type "s" to begin', font, window, 25, 125, (2, 3, 240))
        window.blit(logo_image, (screen_dims[0]*0.2, screen_dims[1]*0.3))
        key = pygame.key.get_pressed()
        if key[pygame.K_s]:  # down key
            scene = 'play'

    elif scene == 'play':
        # window.blit(map_image, (0, 0))
        window.blit(post_office_image, (post_office_loc[0], post_office_loc[1]))
        if advance_level(mail_box_states, returned):
            number += 1
            level_attributes = generate_level(number)
            mailboxes = level_attributes[0]
            fires = level_attributes[1]
            ai.thrust = level_attributes[2]
            mail_box_states = [False]*len(mailboxes)
            returned = False
            ai_returned = False
            packages_states = [False]*len(mailboxes)
            ai_path_indices = ai.move_sequence(mailboxes)
            needed_pts = [post_office_loc] + [mailbox.pos for mailbox in mailboxes]
            ai_path = [needed_pts[ai_path_index] for ai_path_index in ai_path_indices]

            ai.pos = post_office_center[:]
            mailman.pos = post_office_center[:]
            ai.gen_vel(packages_states, ai_path)

        returned = collide_post_office(mailman.pos, mailman.dims)
        ai_returned = collide_post_office(ai.pos, ai.dims)

        if False not in packages_states and ai_returned:
            mailman.draw(window)
            ai.draw(window)
            display_scene(mailboxes, fires, 'play', window, number)
            draw_text('Oh no. You lost to VPS!', big_font, window, 25, 35, (2, 3, 240))
            pygame.display.update()
            time.sleep(2)
            scene = 'end'
        else:
            ai.gen_vel(packages_states, ai_path)

        for i in range(0, len(mailboxes)):
            if mailboxes[i].collide(mailman.pos, mailman.dims, 'mailman'):
                mail_box_states[i] = True
            if mailboxes[i].collide(ai.pos, ai.dims, 'ai'):
                packages_states[ai_path_indices.index(i+1)] = True
                draw_box(ai.pos, box_dims, window)

        for i in range(0, len(fires)):
            if fires[i].collide(mailman.pos, mailman.dims):
                draw_text('Oh no. You got burned!', big_font, window, 25, 35, (2, 3, 24))
                display_scene(mailboxes, fires, 'play', window, number)
                mailman.draw(window)
                ai.draw(window)
                pygame.display.update()
                time.sleep(2)
                scene = 'end'
        if ai.vel == [0.0, 0.0]:
            ai.gen_vel(packages_states, ai_path)
        mailman.check_keys()
        mailman.update(dt)
        mailman.draw(window)
        ai.update(dt)
        ai.draw(window)
        display_scene(mailboxes, fires, 'play', window, number)

    elif scene == 'end':
        window.fill((255, 0, 0))
        draw_text('Oh no. You died!', font, window, 25, 5, (2, 3, 240))
        draw_text('Luckily you can come back alive.', font, window, 25, 30, (2, 3, 240))
        draw_text('Type "r" to restart', font, window, 25, 125, (2, 3, 240))
        draw_text('Also if you are tired of this game you can quit', font, window, 25, 155, (2, 3, 240))
        draw_text('Type "q" to quit', font, window, 25, 185, (2, 3, 240))
        window.blit(logo_image, (screen_dims[0]*0.2, screen_dims[1]*0.3))
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            scene = 'play'
            number = 0
            returned = True
            ai_returned = True
            mail_box_states = []

        elif key[pygame.K_q]:
            running = end_program()

    pygame.display.update()
    clock.tick(dt)
