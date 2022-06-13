import pygame
import random
pygame.init()




#to store all values needed later on the program 
#instead of using global variables
class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    
    BACKGROUND_COLOR = WHITE

    #to be used in drawing bars
    GRADIENTS = [
        (85,123,131),
        (57, 174, 169),
        (162,213,171)
    ]

    FONT = pygame.font.SysFont('courier', 20)
    LARGE_FONT = pygame.font.SysFont('courier', 30,True,True)
    SIDE_PAD = 100 #100 pixels in total as padding 
    TOP_PAD = 150 #top padding

    #lst is list to be sorted
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)


    #set attributes to use later
    def set_list(self, lst):
        self.lst = lst

        #get minimum and maximum values
        self.min_val = min(lst)
        self.max_val = max(lst)
        
        #need to calculate width of each bar
        # thus we need to calculate total available area
        # then divide by length of array
        self.block_width = round(self.width - self.SIDE_PAD) / len(lst) 
        # bar height based on values
        # use interpolation to cap bar height
        self.block_height = int((self.height- self.TOP_PAD) / (self.max_val - self.min_val))
        # where to start drawing
        self.start_x = self.SIDE_PAD // 2




def draw(draw_info, algo_name):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name}", 1, draw_info.RED)
    draw_info.window.blit(title, (draw_info.width/2-title.get_width()/2, 5))


    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2-controls.get_width()/2, 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | Q - Quick Sort | S - Selection Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2-sorting.get_width()/2, 75))
    
    draw_list(draw_info)
    pygame.display.update()


# to draw list
def draw_list(draw_info, color_positions = {}, clear_bg= False):
    # look through each element in list
    # determine height and x coordinate
    # draw rectangle to represent it in different colors
    lst = draw_info.lst
    
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                    draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        #get gradients 0,1,2
        #thus each 3 elements have different colors
        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        #draw rectangle to represent bar
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

#generate starting list to sort
def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val) #random number between min and max
        lst.append(val)
    return lst

def partition(arr,l,h,draw_info):
    i = ( l - 1 )
    x = arr[h]
  
    for j in range(l , h):
        if   arr[j] <= x:
  
            # increment index of smaller element
            i = i+1
            arr[i],arr[j] = arr[j],arr[i]
            draw_list(draw_info,{arr[i]:draw_info.GREEN,arr[j]:draw_info.RED}, True)
            pygame.event.wait(10)
  
    arr[i+1],arr[h] = arr[h],arr[i+1]
    return (i+1)

def quick_sort(draw_info):
    arr = draw_info.lst
    l=0
    h=len(arr)-1
    size = h-l+1
    stack = [0] * (size)
    # initialize top of stack
    top = -1
  
    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h
  
    # Keep popping from stack while is not empty
    while top >= 0:
        
        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        # Set pivot element at its correct position in
        # sorted array
        p = partition( arr, l, h ,draw_info)
        #yield True
        # If there are elements on left side of pivot,
        # then push left side to stack
        if p-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1
            draw_list(draw_info,{arr[top-1]:draw_info.GREEN,arr[top]:draw_info.RED}, True)
            #pygame.event.wait(5)
            yield True
        
        # If there are elements on right side of pivot,
        # then push right side to stack
        if p+1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h
            draw_list(draw_info,{arr[top-1]:draw_info.GREEN,arr[top]:draw_info.RED}, True)
            #pygame.event.wait(5)
            yield True

    return arr
    

def insertion_sort(draw_info):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            sort = i>0 and lst[i-1] > current
            draw_list(draw_info, {i-1:draw_info.GREEN, i:draw_info.RED},True)
            yield True

            if not sort:
                break
            
            lst[i] = lst[i-1]
            i = i-1
            lst[i] = current
            
    return lst


def selection_sort(draw_info):
    lst = draw_info.lst

    for i in range(0,len(lst)):

        min_indx = i
        for j in range(i+1,len(lst)):
            if(lst[j] < lst[min_indx]):
                min_indx = j
            draw_list(draw_info, {i:draw_info.GREEN, j:draw_info.RED},True)
            yield True
        temp = lst[min_indx]
        lst[min_indx] = lst[i]
        lst[i]=temp

    return lst


#main driver
def main():
    run = True
    clock = pygame.time.Clock()

    n=200
    min_val = 0
    max_val = 200

    lst = generate_starting_list(n,min_val,max_val)
    draw_info = DrawInformation(800,600,lst)
    sorting = False
    
    # we need to call different sort functions
    sorting_algorithm = quick_sort
    sorting_algo_name = "Quick Sort"
    sorting_algoithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algoithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info,sorting_algo_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            #check keydown
            if event.type != pygame.KEYDOWN:
                continue
            
            #reset if pressed R
            if event.key == pygame.K_r:
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            #if space then start sorting
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algoithm_generator = sorting_algorithm(draw_info)
            elif event.key == pygame.K_q and sorting == False:
                if(n!=200):
                    n=200
                    lst = generate_starting_list(n,min_val,max_val)
                    draw_info.set_list(lst)
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_i and sorting == False:
                if(n!=50):
                    n=50
                    lst = generate_starting_list(n,min_val,max_val)
                    draw_info.set_list(lst)
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_s and sorting == False:
                if(n!=50):
                    n=50
                    lst = generate_starting_list(n,min_val,max_val)
                    draw_info.set_list(lst)
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
                
           
            

    pygame.quit()


if __name__ == "__main__":
    main()
