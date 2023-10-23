import pygame
import sys
import time
import random
import pickle
GREY=(111,111,111)
WHITE=(255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen_size = (800,800)
game_size=(15,15)
cube_height=screen_size[0]/game_size[0]
cube_width=screen_size[1]/game_size[1]
chess_vec=[[],[]]
candidate_pos_list=[[],[]]
real_candidate_list=[]
pos_dic={}
class one_pos():
	def __init__(self,pos_x,pos_y):
		self.pos_x=pos_x
		self.pos_y=pos_y
		self.pos=(pos_x,pos_y)
		self.occupied=0
		self.from_count=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
		self.blocked=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
		self.neighbor_pos=[(pos_x,pos_y+1),(pos_x+1,pos_y+1),(pos_x+1,pos_y),(pos_x+1,pos_y-1),(pos_x,pos_y-1),(pos_x-1,pos_y-1),(pos_x-1,pos_y),(pos_x-1,pos_y+1)]
	def occupy(self,occupied):
		self.occupied=occupied
		for i in [0,1]:
			if self.pos in candidate_pos_list[i]:
				candidate_pos_list[i].remove(self.pos)
		if self.pos in real_candidate_list:
			real_candidate_list.remove(self.pos)
		for i in range(8):
			if self.neighbor_pos[i][0]>=0 and self.neighbor_pos[i][0]<game_size[0] and self.neighbor_pos[i][1]>=0 and self.neighbor_pos[i][1]<game_size[1]:
				count_sum=self.from_count[occupied-1][i]+self.from_count[occupied-1][(i+4)%8]+1
				if pos_dic[self.neighbor_pos[i]].occupied==0:
					pos_dic[self.neighbor_pos[i]].from_count[occupied-1][i]=count_sum
					if self.neighbor_pos[i] not in candidate_pos_list[occupied-1]:
						candidate_pos_list[occupied-1].append(self.neighbor_pos[i])
				if pos_dic[self.neighbor_pos[i]].occupied==occupied:
					dt_x=self.neighbor_pos[i][0]-self.pos_x
					dt_y=self.neighbor_pos[i][1]-self.pos_y
					for j in range(2,max(game_size[0],game_size[1])):
						temp_pos=(self.pos_x+j*dt_x,self.pos_y+j*dt_y)
						if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
							break 
						if pos_dic[temp_pos].occupied==occupied:
							continue
						if pos_dic[temp_pos].occupied==0:							
							pos_dic[temp_pos].from_count[occupied-1][i]=count_sum
						break
		for i in range(8):
			dt_x=self.neighbor_pos[i][0]-self.pos_x
			dt_y=self.neighbor_pos[i][1]-self.pos_y
			labE=0
			keep_j=-1
			for j in range(1,6):
				temp_pos=(self.pos_x+j*dt_x,self.pos_y+j*dt_y)
				if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
					keep_j=j
					break
				if pos_dic[temp_pos].occupied==0:
					labE=1
				if labE==1 and pos_dic[temp_pos].occupied==occupied:
					keep_j=j
					break
			if keep_j!=-1:
				for j2 in range(1,keep_j):
					temp_pos2=(self.pos_x+j2*dt_x,self.pos_y+j2*dt_y)
					if pos_dic[temp_pos2].occupied==0:
						pos_dic[temp_pos2].blocked[occupied%2][i]=1
						pos_dic[temp_pos2].blocked[occupied%2][(i+4)%8]=1
		for i in range(4):
			if self.from_count[occupied-1][i]+self.from_count[occupied-1][(i+4)%8]>=4:
				return occupied
		return -1
def draw_lines(screen):
	for i in range(1,game_size[0]):
		pygame.draw.aaline(screen, WHITE,(i*cube_height,0),(i*cube_height,screen_size[1]),5)
	for i in range(1,game_size[1]):
		pygame.draw.aaline(screen, WHITE,(0,i*cube_width),(screen_size[0],i*cube_width),5)
def draw_cubes(screen):
	for each in chess_vec[0]:
		pygame.draw.rect(screen,[0,0,0],[(each[1])*cube_width,(each[0])*cube_height,cube_width,cube_height],0)
	for each in chess_vec[1]:
		pygame.draw.rect(screen,[255,255,255],[(each[1])*cube_width,(each[0])*cube_height,cube_width,cube_height],0)
saved_list=[]
def save():
	data=pickle.dumps((candidate_pos_list,pos_dic,real_candidate_list))
	saved_list.append(data)
def load():
	global pos_dic
	global candidate_pos_list
	global real_candidate_list
	(candidate_pos_list,pos_dic,real_candidate_list)=pickle.loads(saved_list[-1])
'''
def evaluate(turn):
	val=0
	ene_turn=(turn+1)%2
	for each in candidate_pos_list[turn]:
		count1=-1
		for i in range(4):
			sum1=(pos_dic[each].from_count[turn][i]+pos_dic[each].from_count[turn][(i+4)%8])
			if sum1==1:
				val+=1
			else:
				val+=sum1*sum1/2
			count1+=sum1
		if count1>1:
			count1+=1
		#val+=count1
	for each in candidate_pos_list[ene_turn]:
		count2=1
		for i in range(4):
			sum2=pos_dic[each].from_count[ene_turn][i]+pos_dic[each].from_count[ene_turn][(i+4)%8]
			if sum2==1:
				val-=1
			else:
				val-=sum2*sum2/2
			count2-=sum2
		#if count2<=-2:
		#	count2-=1
		#val+=count2
	return val
'''
def evaluate(turn,next_turn):
	val=0
	ene_turn=(turn+1)%2
	over_count1=0
	for each in candidate_pos_list[turn]:			
		count1=-1
		for i in range(4):
			if pos_dic[each].blocked[turn][i]==1:
				break
			sum1=(pos_dic[each].from_count[turn][i]+pos_dic[each].from_count[turn][(i+4)%8])
			if sum1>=4:
				if next_turn==turn:
					return 10001
				else:
					over_count1+=1
					break
			if sum1==1:
				val+=1
			else:
				val+=sum1*sum1/2
			count1+=sum1
		if count1>=2:
			count1+=1
		if count1>-1:
			val+=count1
	over_count2=0
	for each in candidate_pos_list[ene_turn]:
		count2=1
		for i in range(4):
			if pos_dic[each].blocked[ene_turn][i]==1:
				continue
			sum2=pos_dic[each].from_count[ene_turn][i]+pos_dic[each].from_count[ene_turn][(i+4)%8]
			if sum2>=4:
				if next_turn==ene_turn:
					return -10001
				else:
					over_count2+=1
					break
			if sum2==1:
				val-=1
			else:
				val-=sum2*sum2/2
			count2-=sum2
		if count2<=-2:
			count2-=1
		if count2<1:
			val+=count2
	if next_turn==ene_turn:		
		if over_count2>=2:
			return -10001
		if over_count1>=2:
			return 10001
	if next_turn==turn:
		if over_count1>=2:
			return 10001	
		if over_count2>=2:
			return -10001
	t=next_turn
	for each in candidate_pos_list[t]:
		for i in range(4):
			if pos_dic[each].from_count[t][i]+pos_dic[each].from_count[t][(i+4)%8]==3:
				dt_x=pos_dic[each].neighbor_pos[i][0]-each[0]
				dt_y=pos_dic[each].neighbor_pos[i][1]-each[1]
				labi=0
				for j in range(1,max(game_size[1],game_size[1])):
					temp_pos=(each[0]+j*dt_x,each[1]+j*dt_y)
					if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
						labi=1
						break 
					if pos_dic[temp_pos].occupied==t+1:
						continue
					if pos_dic[temp_pos].occupied==0:							
						break
					labi=1
					break
				if labi==0:
					for j in range(-1,-max(game_size[1],game_size[1]),-1):
						temp_pos=(each[0]+j*dt_x,each[1]+j*dt_y)
						if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
							labi=1
							break 
						if pos_dic[temp_pos].occupied==t+1:
							continue
						if pos_dic[temp_pos].occupied==0:
							break
						labi=1
						break
				if labi==0:
					if t==turn:
						return 10001
					if t==ene_turn:
						return -10001
	return val
def simu_choice(turn,depth,min_lim=100000):
	ene_turn=(turn+1)%2
	if depth==0:
		valu=evaluate(turn,turn)
		return (valu,(-1,-1))
	if depth==1:
		maxi=-100000
		choici_keep=(-1,-1)
		save()
		for each in real_candidate_list.copy():
			win_d=pos_dic[each].occupy(turn+1)
			if win_d>0:
				saved_list.pop()
				return (10001,each)
			vv=evaluate(turn,ene_turn)
			if vv>maxi:
				maxi=vv
				choici_keep=each
			load()
		saved_list.pop()
		return (maxi,choici_keep)
	max_value=-100000
	choice_keep=(-1,-1)
	ene_turn=(turn+1)%2
	save()
	for each in real_candidate_list.copy():
		win_d=pos_dic[each].occupy(turn+1)
		if win_d>0:
			saved_list.pop()
			return (10001,each)
		for each2 in pos_dic[each].neighbor_pos:
			if each2[0]>=0 and each2[0]<game_size[0] and each2[1]>=0 and each2[1]<game_size[1]:
				if pos_dic[each2].occupied==0:
					for each22 in pos_dic[each2].neighbor_pos:
						if each22[0]>=0 and each22[0]<game_size[0] and each22[1]>=0 and each22[1]<game_size[1]:
							if pos_dic[each22].occupied==0:
								if each22 not in real_candidate_list:
									real_candidate_list.append(each22)
		save()
		min_value=100000
		jian2=0
		for each3 in real_candidate_list:
			win_d2=pos_dic[each3].occupy(ene_turn+1)
			if win_d2>0:
				min_value=-10001
				break
			val2=simu_choice(turn,depth-2,min_value)[0]
			load()
			if val2==-1000000:
				continue
			if val2<max_value:
				jian2=1
				break
			if val2<min_value:
				min_value=val2
		saved_list.pop()
		load()
		if min_value>min_lim:
			saved_list.pop()
			return (-1000000,(-1,-1))
		if jian2==1:
			continue
		if min_value!=100000 and min_value>max_value:
			max_value=min_value
			choice_keep=each
	saved_list.pop()
	return (max_value,choice_keep)
def AI_choice(turn,depth):
	ene_turn=(1+turn)%2
	for t in [turn,ene_turn]:
		for each in candidate_pos_list[t]:
			for i in range(4):
				if pos_dic[each].from_count[t][i]+pos_dic[each].from_count[t][(i+4)%8]>=4:
					return each
	'''
	posi_pos=[]
	for t in [turn,ene_turn]:
		for each in candidate_pos_list[t]:
			for i in range(4):
				if pos_dic[each].from_count[t][i]+pos_dic[each].from_count[t][(i+4)%8]==3:
					dt_x=pos_dic[each].neighbor_pos[i][0]-each[0]
					dt_y=pos_dic[each].neighbor_pos[i][1]-each[1]
					labi=0
					for j in range(1,max(game_size[1],game_size[1])):
						temp_pos=(each[0]+j*dt_x,each[1]+j*dt_y)
						if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
							labi=1
							break 
						if pos_dic[temp_pos].occupied==t+1:
							continue
						if pos_dic[temp_pos].occupied==0:							
							break
						labi=1
						break
					if labi==0:
						for j in range(-1,-max(game_size[1],game_size[1]),-1):
							temp_pos=(each[0]+j*dt_x,each[1]+j*dt_y)
							if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
								labi=1
								break 
							if pos_dic[temp_pos].occupied==t+1:
								continue
							if pos_dic[temp_pos].occupied==0:
								break
							labi=1
							break
					if labi==0:
						if t == turn:
							return each
						posi_pos.append(each)
	max_val=-1000
	pos_keep=(-1,-1)
	save()
	for each in posi_pos:
		pos_dic[each].occupy(turn+1)
		val=evaluate(turn,turn)
		if val>max_val:
			max_val=val
			pos_keep=each
		load()
	saved_list.pop()
	if pos_keep!=(-1,-1):
		return pos_keep
	'''
	'''
	t=turn
	for each in candidate_pos_list[t]:
		for i in range(4):
			if pos_dic[each].from_count[t][i]+pos_dic[each].from_count[t][(i+4)%8]==3:
				dt_x=pos_dic[each].neighbor_pos[i][0]-each[0]
				dt_y=pos_dic[each].neighbor_pos[i][1]-each[1]
				labi=0
				for j in range(1,max(game_size[1],game_size[1])):
					temp_pos=(each[0]+j*dt_x,each[1]+j*dt_y)
					if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
						labi=1
						break 
					if pos_dic[temp_pos].occupied==t+1:
						continue
					if pos_dic[temp_pos].occupied==0:							
						break
					labi=1
					break
				if labi==0:
					for j in range(-1,-max(game_size[1],game_size[1]),-1):
						temp_pos=(each[0]+j*dt_x,each[1]+j*dt_y)
						if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
							labi=1
							break 
						if pos_dic[temp_pos].occupied==t+1:
							continue
						if pos_dic[temp_pos].occupied==0:
							break
						labi=1
						break
				if labi==0:
					return each
	'''
	real_candidate_list.clear()
	for i in range (2):
		for each in candidate_pos_list[i]:
			if pos_dic[each].occupied==0:
				if each not in real_candidate_list:
					real_candidate_list.append(each)
				for each2 in pos_dic[each].neighbor_pos:
					if each2[0]>=0 and each2[0]<game_size[0] and each2[1]>=0 and each2[1]<game_size[1]:
						if pos_dic[each2].occupied==0:
							if each2 not in real_candidate_list:
								real_candidate_list.append(each2)

	s_choice=simu_choice(turn,depth)[1]
	return s_choice
if __name__ == "__main__":
	DEPTH=2
	for i in range(game_size[0]):
		for j in range(game_size[1]):
			a_pos=one_pos(i,j)
			pos_dic[(i,j)]=a_pos
	pygame.init()
	screen = pygame.display.set_mode(screen_size, 0, 32)
	pygame.display.set_caption("gobang")
	FPS=30
	clock = pygame.time.Clock()
	turn=0
	win_lab=0
	while True:
		clock.tick(FPS)
		if win_lab==0:
			l=0
			if turn==0 and pygame.mouse.get_pressed()[0]:
				l=1
				pos=pygame.mouse.get_pos()
				pos_=(int(pos[1]/cube_height),int(pos[0]/cube_width))
			if turn==1:
				l=1
				pos_=AI_choice(1,DEPTH)
			if l==1:
				if pos_dic[pos_].occupied==0:
					chess_vec[turn].append(pos_)
					win_detect=pos_dic[pos_].occupy(turn+1)
					print(evaluate(1,(turn+1)%2))
					if win_detect>0:
						print('player',turn+1,' win')
						win_lab=1
					turn=(turn+1)%2
		screen.fill(GREY)
		draw_lines(screen)
		draw_cubes(screen)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
