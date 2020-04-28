#import psychtoolbox under the name "ptb"
import psychtoolbox as ptb
#import prefs to change preferred sound engine to ptb
from psychopy import prefs
#import random for trial handler
import random
#set sound engine to ptb, which has more precise timing abilities
prefs.hardware['audioLib'] = ['PTB']
#import needed classes from psychopy
from psychopy import visual, sound, core, event, misc, data
#import they keyboard from psychopy as hardware
from psychopy.hardware import keyboard

#define global variables
window = None
s = None
cross = None
direction_prompt = None

#define empty array of trials to be used by trial handler for loops
trials = []

#intervals in seconds possible for each trial
duration_levels = [1, 2, 3]
#defines 2 modality types, audio and visual
#-1 is audio and 1 is visual
modality_levels = [-1, 1]

#select number from the array in duration_levels
for i in range(len(duration_levels)):
    #create a new variable which is the number from the array
    duration = duration_levels[i]
#select number from the array in modality_levels
for i in range(len(modality_levels)):
    #create a new variable which is the number from the array
    modality = modality_levels[i]

#combine both duration and modality to form a trial
for duration in duration_levels:
    #combine both duration and modality to form a trial
    for modality in modality_levels:
        #append trials based on duration and modality
        t = [duration, modality]
        #add t to trials
        trials.append(t)

#shuffle trials randomly
random.shuffle(trials)

#Input: space bar from user to advance from screen
#Output: none aside from flipping the window
#Purpose: display instructions to the user
def Instructions():
    #declare global variables
    global window
    global direction_prompt
    
    #initializes a window over which text and stimuli can be drawn
    window = visual.Window([1920, 1080], monitor = "testMonitor", color = 'white')
    
    #defines properties of the text stimulus to show instructions
    instr = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
    
    #creates content of text displayed for pre-experiment instructions
    instr.text = 'Thank you for your participation. You can stop this experiment at any time for any reason. Press any key to continue.'
    
    while not event.getKeys():
        #draw instructions on screen
        instr.draw()
        #flip window so instructions are visible to user
        window.flip()
    
    #get rid of instructions from the window
    window.flip()

#open log file
log_file = open('logfile.csv', 'a')

#Input: variable 'duration', space bar from user during reproduction epoch
#Output: duration of interval reproduction created by user in log_file
#Purpose: run audio trial with no feedback
def TrialA(duration):
    #declare global variables
    global window
    global kb
    global s
    global log_file
    
    #initialize variable s which is the auditory stimulis wav file
    s = sound.Sound(value='440.wav')
    
    ##Estimation Epoch (EE)
    #start playing the tone
    s.play()
    #play the tone for a duration defined by "duration"
    core.wait(duration)
    #stop playing the tone after the interval has passed
    s.stop()
    
    #wait 2 seconds between the estimation epoch and the reproduction epoch
    core.wait(2)
    
    ##Reproduction Epoch(RE)
    #define keyboard
    kb = keyboard.Keyboard()
    #clear prior keypresses
    kb.clearEvents()
    #get start of RE for comparison to duration in later loops
    astart_time = core.getTime()
    #begin playing the sound
    s.play()
    
    #set variable keys as an empty array
    keys = []
    
    #stop playing the tone after space bar has been pressed
    while not('space' in keys):
        window.flip()
        keys = kb.getKeys('space')
    #stop playing the sound file
    s.stop()
    
    #note time that participant reproduction stops
    astop_time = core.getTime()
    #subtract trial start time from stop time to use for feedback loops
    a_feedback = astop_time - astart_time

    #write participant response to log file
    log_file.write(str("AudioNF:") + "," + str(a_feedback - duration) + "," + str("RealDur:") + "," + str(duration) + "\n")

#Input: variable 'duration', space bar from user during reproduction epoch
#Output: duration of interval reproduction created by user in log_file
#Purpose: run video trial with no feedback
def TrialV(duration):
    #declare global variables
    global window
    global kb
    global log_file
    
    #initializes a window over which text and stimuli can be drawn
    window = visual.Window([1920, 1080], monitor = "testMonitor", color = 'white')
    
    ##Estimation Epoch (EE)
    #defines properties of the text stimulus to show instructions
    cross = visual.TextStim(window, text='+', height=2, wrapWidth=1, color='black', pos=(0, 0))
    #draw the cross in the window
    cross.draw()
    #flip the window to reveal the cross
    window.flip()
    #keep the cross displayed for the duration
    core.wait(duration)
    #get rid of the cross after it is presented
    window.flip()
    
    #wait 2 seconds before Reproduction Epoch begins
    core.wait(2)
    
    ##Reproduction Epoch (RE)
    #define keyboard
    kb = keyboard.Keyboard()
    #clear prior keypresses
    kb.clearEvents()
    
    #define start of trial 
    vstart_time = core.getTime()
    
    #set keys as an empty array variable
    keys = []
    
    #stop presentation of the cross when space bar is pressed
    while not event.getKeys('space'):
        #define properties of the cross
        cross = visual.TextStim(window, text='+', height=2, wrapWidth=1, color='black', pos=(0, 0))
        #draw cross on the window
        cross.draw()
        #flip window so participant can view stimulus
        window.flip()
    
    #define end of reproduction 
    vstop_time = core.getTime()
    #subtract the trial stop time from stop time to get duration of reproduction
    v_feedback = vstop_time - vstart_time
    
    #write participant response to log file
    log_file.write(str("VideoNF:") + "," + str(v_feedback - duration) + "," + str("RealDur:") + "," + str(duration) + "\n")
    
    #flip window to get rid of the reproduced cross
    window.flip()

#Input: variable 'duration', space bar from user during re production epoch
#Output: duration of interval reproduction created by userin log_file, text display of feedback based on space bar press
#Purpose: run audio trial with accurate feedback
def TrialAFeed1(duration):
    #declare global variables
    global window
    global kb
    global s
    global log_file
        
    #initialize variable s which is the auditory stimulis wav file
    s = sound.Sound(value='440.wav')
    
    ##Estimation Epoch (EE)
    #start playing the tone
    s.play()
    #play the tone for a duration defined by "duration"
    core.wait(duration)
    #stop playing the tone after the interval has passed
    s.stop()
    
    #wait 2 seconds between the estimation epoch and the reproduction epoch
    core.wait(2)
    
    ##Reproduction Epoch(RE)
    #define keyboard
    kb = keyboard.Keyboard()
    #clear prior keypresses
    kb.clearEvents()
    #get start of RE for comparison to duration in later loops
    astart_time = core.getTime()
    #begin playing the sound
    s.play()
    
    #set variable keys as an empty array
    keys = []
    
    #stop playing the tone after space bar has been pressed
    while not('space' in keys):
        #flip the window
        window.flip()
        #get space bar input
        keys = kb.getKeys('space')
    #stop playing the sound file
    s.stop()
    
    #note time that participant reproduction stops
    astop_time = core.getTime()
    #subtract trial start time from stop time to use for feedback loops
    a_feedback = astop_time - astart_time

    #write participant response to log file
    log_file.write(str("AudioAF:") + "," + str(a_feedback - duration) + "," + str("RealDur:") + "," + str(duration) + "\n")
    
    
    #compare the interval reproduction with the duration from EE to determine feedback text
    #l is long, s is short, p is perfect
    #display feedback if trial is too long
    if a_feedback > duration:
        #define properties of text feedback
        la_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        la_feed.text = 'INTERVAL REPRODUCTION WAS TOO LONG'
        #draw text onto the window
        la_feed.draw()
    #display feedback if trial is too long
    elif a_feedback < duration:
        #define properties of text feedback
        sa_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        sa_feed.text = 'INTERVAL REPRODUCTION WAS TOO SHORT'
        #draw text onto the window
        sa_feed.draw()
    #display feedback if trial is perfect
    else: 
        #define properties of text feedback
        pa_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        pa_feed.text = 'INTERVAL REPRODUCTION WAS PERFECT, GREAT JOB!'
        #draw text onto the window
        pa_feed.draw()
    
    #flip window to reveal feedback drawn from above loop
    window.flip()

#Input: variable 'duration', space bar from user during reproduction epoch
#Output: duration of interval reproduction created by user in log_file, text display of feedback based on space bar press
#Purpose: run visual trial with accurate feedback
def TrialVFeed1(duration):
    #define global variables
    global window
    global kb
    global log_file
    
    #initializes a window over which text and stimuli can be drawn
    window = visual.Window([1920, 1080], monitor = "testMonitor", color = 'white')
    
    ##Estimation Epoch (EE)
    #defines properties of the text stimulus to show instructions
    cross = visual.TextStim(window, text='+', height=2, wrapWidth=1, color='black', pos=(0, 0))
    #draw the cross in the window
    cross.draw()
    #flip the window to reveal the cross
    window.flip()
    #keep the cross displayed for the duration x
    core.wait(duration)
    #get rid of the cross after it is presented
    window.flip()
    
    #wait 2 seconds before Reproduction Epoch begins
    core.wait(2)
    
    ##Reproduction Epoch (RE)
    #define keyboard
    kb = keyboard.Keyboard()
    #clear prior keypresses
    kb.clearEvents()
    
    #define start of trial 
    vstart_time = core.getTime()
    
    #set array keys to empty
    keys = []
    
    #press the space bar to end cross presentation
    while not event.getKeys('space'):
        #define properties of the cross
        cross = visual.TextStim(window, text='+', height=2, wrapWidth=1, color='black', pos=(0, 0))
        #draw cross on the window
        cross.draw()
        #flip window so participant can view stimulus
        window.flip()
    
    #define end of reproduction 
    vstop_time = core.getTime()
    #subtract the trial stop time from stop time to get duration of reproduction
    v_feedback = vstop_time - vstart_time
    
    #write participant response to log file
    log_file.write(str("VisualAF:") + "," + str(v_feedback - duration) + "," + str("RealDur:") + "," + str(duration) + "\n")
    
    #give visual feedback of interval reproduction by comparing reproduced interval with probe interval
    #l is long, s is short, p is perfect
    #display feedback if trial is too short
    if v_feedback > duration:
        #define properties of text feedback
        lv_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        lv_feed.text = 'INTERVAL REPRODUCTION WAS TOO LONG'
        #draw text onto the window
        lv_feed.draw()
    #display feedback if trial is too short
    elif v_feedback < duration:
        #define properties of text feedback
        sv_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        sv_feed.text = 'INTERVAL REPRODUCTION WAS TOO SHORT'
        #draw text onto the window
        sv_feed.draw()
    #display feedback if trial is perfect
    else:
        #define properties of text feedback
        pv_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        pv_feed.text = 'INTERVAL REPRODUCTION WAS PERFECT, GREAT JOB!'
        #draw text onto the window
        pv_feed.draw()
    
    #flip window to display drawn feedback text based on above loop
    window.flip()
    #display text for 2 seconds
    core.wait(2)

#Input: variable 'duration', space bar from user during reproduction epoch
#Output: duration of interval reproduction created by user in log_file, text display of feedback based on space bar press
#Purpose: run audio trial with inaccurate feedback
def TrialAFeed2(duration):
    #declare global variables
    global window
    global kb
    global s
    global log_file
        
    #initialize variable s which is the auditory stimulis wav file
    s = sound.Sound(value='440.wav')
    
    ##Estimation Epoch (EE)
    #start playing the tone
    s.play()
    #play the tone for a duration defined by "duration"
    core.wait(duration)
    #stop playing the tone after the interval has passed
    s.stop()
    
    #wait 2 seconds between the estimation epoch and the reproduction epoch
    core.wait(2)
    
    ##Reproduction Epoch(RE)
    #define keyboard
    kb = keyboard.Keyboard()
    #clear prior keypresses
    kb.clearEvents()
    #get start of RE for comparison to duration in later loops
    astart_time = core.getTime()
    #begin playing the sound
    s.play()
    
    #set variable keys as an empty array
    keys = []
    
    #stop playing the tone after space bar has been pressed
    while not('space' in keys):
        #flip window
        window.flip()
        #get space bar input
        keys = kb.getKeys('space')
    #stop playing the sound file
    s.stop()
    
    #note time that participant reproduction stops
    astop_time = core.getTime()
    #subtract trial start time from stop time to use for feedback loops
    a_feedback = astop_time - astart_time

    #write participant response to log file
    log_file.write(str("AudioXF:") + "," + str(a_feedback - duration) + "," + str("RealDur:") + "," + str(duration) + "\n")
    
    #compare the interval reproduction with the duration from EE to determine feedback text
    #l is long, s is short, p is perfect
    #display feedback if trial is too long
    if a_feedback*0.9 > duration:
        #define properties of text feedback
        la_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        la_feed.text = 'INTERVAL REPRODUCTION WAS TOO LONG'
        #draw text onto the window
        la_feed.draw()
    #display feedback if trial is too short
    elif a_feedback*0.9 < duration:
        #define properties of text feedback
        sa_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        sa_feed.text = 'INTERVAL REPRODUCTION WAS TOO SHORT'
        #draw text onto the window
        sa_feed.draw()
    #display feedback if trial is perfect
    else: 
        #define properties of text feedback
        pa_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        pa_feed.text = 'INTERVAL REPRODUCTION WAS PERFECT, GREAT JOB!'
        #draw text onto the window
        pa_feed.draw()
    
    #flip window to reveal feedback drawn from above loop
    window.flip()

#Input: variable 'duration', space bar from user during reproduction epoch
#Output: duration of interval reproduction created by user in log_file, text display of feedback based on space bar press
#Purpose: run visual trial with inaccurate feedback
def TrialVFeed2(duration):
    #define global variables
    global window
    global kb
    global log_file
    
    #initializes a window over which text and stimuli can be drawn
    window = visual.Window([1920, 1080], monitor = "testMonitor", color = 'white')
    
    ##Estimation Epoch (EE)
    #defines properties of the text stimulus to show instructions
    cross = visual.TextStim(window, text='+', height=2, wrapWidth=1, color='black', pos=(0, 0))
    #draw the cross in the window
    cross.draw()
    #flip the window to reveal the cross
    window.flip()
    #keep the cross displayed for the duration x
    core.wait(duration)
    #get rid of the cross after it is presented
    window.flip()
    
    #wait 2 seconds before Reproduction Epoch begins
    core.wait(2)
    
    ##Reproduction Epoch (RE)
    #define keyboard
    kb = keyboard.Keyboard()
    #clear prior keypresses
    kb.clearEvents()
    
    #define start of trial 
    vstart_time = core.getTime()
    
    #define keys as empty array
    keys = []
    
    #get rid of cross from screen if space bar is pressed
    while not event.getKeys('space'):
        #define properties of the cross
        cross = visual.TextStim(window, text='+', height=2, wrapWidth=1, color='black', pos=(0, 0))
        #draw cross on the window
        cross.draw()
        #flip window so participant can view stimulus
        window.flip()
    
    #define end of reproduction 
    vstop_time = core.getTime()
    #subtract the trial stop time from stop time to get duration of reproduction
    v_feedback = vstop_time - vstart_time
    
    #write participant response to log file
    log_file.write(str("VisualXF:") + "," + str(v_feedback - duration) + "," + str("RealDur:") + "," + str(duration) + "\n")
    
    #compare the interval reproduction with the duration from EE to determine feedback text
    #l is long, s is short, p is perfect
    #display feedback if trial is too long
    if v_feedback*9 > duration:
    #define properties of text feedback
        lv_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        lv_feed.text = 'INTERVAL REPRODUCTION WAS TOO LONG'
        #draw text onto the window
        lv_feed.draw()
    #display feedback if trial is too short
    elif v_feedback*9 < duration:
        #define properties of text feedback
        sv_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        sv_feed.text = 'INTERVAL REPRODUCTION WAS TOO SHORT'
        #draw text onto the window
        sv_feed.draw()
    #display feedback if trial is perfect
    else:
        #define properties of text feedback
        pv_feed = visual.TextStim(window, height = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        pv_feed.text = 'INTERVAL REPRODUCTION WAS PERFECT, GREAT JOB!'
        #draw text onto the window
        pv_feed.draw()
    
    #flip window to display drawn feedback text based on above loop
    window.flip()
    #display text for 2 seconds
    core.wait(2)

#Input: log file
#Output: None
#Purpose: close the log_file, window, and program
def TerminateTask():
    #define global variables
    global window
    global log_file
    
    #close log file
    log_file.close()
    
    #close the global window
    window.close()
    
    #quit the experiment
    core.quit()

#Input: variable "trials", function "TrialA"
#Output: implementation of Trial A with appropriate duration values defined in trials
#Purpose: run function Trial A
def RunTrialA():
    #select a number from the range defined by variable "trials"
    for i in range(len(trials)):
        #run the number selected from trials 
        if trials[i][1] < 0:
            #use number defined by trials in TrialA
            TrialA(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip the window after waiting to advance 
            window.flip()
        #otherwise, run other interval
        else:
            #use number defined by trials in TrialA
            TrialA(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip the window after waiting to advance 
            window.flip()

#Input: variable "trials", function "TrialV"
#Output: implementation of TrialV with appropriate duration values defined in trials
#Purpose: run function TrialV
def RunTrialV():
    random.shuffle(trials)
    #select a number from the range defined by variable "trials"
    for i in range(len(trials)):
        #run the number selected from trials
        if trials[i][1] < 0:
            #use the number defined by trials in TrialB
            TrialV(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip the window after waiting to advance 
            window.flip()
        #otherwise, run other interval
        else:
            #use the number defined by trials in TrialB
            TrialV(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip the window after waiting to advance 
            window.flip()

#Input: variable "trials", function "TrialAFeed1"
#Output: implementation of TrialAFeed1 with appropriate duration values defined in trials
#Purpose: run function TrialAFeed1
def RunAFeed1():
    #select a number from the range defined in variable "trials"
    for i in range(len(trials)):
        #run the number selected from trials
        if trials[i][1] < 0:
            #use the number defined by trials in TrialAFeed1
            TrialAFeed1(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip window after waiting to advance
            window.flip()
        #otherwise, run other interval
        else:
            #use the number defined by trials in TrialAFeed1
            TrialAFeed1(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip window after waiting to advance
            window.flip()

#Input: variable "trials", function "TrialVFeed1"
#Output: implementation of TrialVFeed1 with appropriate duration values defined in trials
#Purpose: run function TrialVFeed1
def RunVFeed1():
    #select a number from the range defined in variable "trials"
    for i in range(len(trials)):
        #run the number selected from trials
        if trials[i][1] < 0:
            #use the number defined by trials in TrialVFeed2
            TrialVFeed1(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip window after waiting to advance
            window.flip()
        #otherwise, run other interval
        else:
            #use the number defined by trials in TrialVFeed2
            TrialVFeed1(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip window after waiting to advance
            window.flip()

#Input: variable "trials", function "TrialAFeed2"
#Output: implementation of TrialAFeed2 with appropriate duration values defined in trials
#Purpose: run function TrialAFeed2
def RunAFeed2():
    #select a number from the range defined in variable "trials"
    for i in range(len(trials)):
        #use the number defined by trials in TrialAFeed2
        if trials[i][1] < 0:
            #use the number defined by trails in TrailAFeed2
            TrialAFeed2(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip window after waiting to advance
            window.flip()
        #otherwise, run other interval
        else:
            #use the number defined by trails in TrailAFeed2
            TrialAFeed2(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip window after waiting to advance
            window.flip()

#Input: variable "trials", function "TrialVFeed2"
#Output: implementation of TrialVFeed2 with appropriate duration values defined in trials
#Purpose: run function TrialVFeed2
def RunVFeed2():
    #select a number from the range defined in variable "trials"
    for i in range(len(trials)):
        #use the number defined by trials in TrialVFeed2
        if trials[i][1] < 0:
            #use the number defined by trials in TrialVFeed2
            TrialVFeed2(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip window after waiting to advance
            window.flip()
        #otherwise, run other interval
        else:
            #use the number defined by trials in TrialVFeed2
            TrialVFeed2(trials[i][0])
            #wait for 2 seconds
            core.wait(2)
            #flip window after waiting to advance
            window.flip()

#Input: functions RunTrialA, RunTrialV
#Output: None
#Purpose: define first and fourth trial blocks
def Block1_4():
    RunTrialA()
    RunTrialV()
    RunTrialA()
    RunTrialV()

#Input: functions RunTrialAFeed1, RunTrialVFeed2
#Output: None
#Purpose: define second trial block
def Block2():
    RunAFeed1()
    RunVFeed1()
    RunAFeed1()
    RunVFeed1()

#Input: functions RunTrialAFeed1, RunTrialVFeed2
#Output: None
#Purpose: define third trial block
def Block3():
    RunAFeed2()
    RunVFeed2()
    RunAFeed2()
    RunVFeed2()

#initiate Instructions function
Instructions()
#initiate first trial block
Block1_4()
#initiate second trial block
Block2()
#initiate thrid trial block
Block3()
#initiate fouth trial block
Block1_4()
#iniate task termination
TerminateTask()