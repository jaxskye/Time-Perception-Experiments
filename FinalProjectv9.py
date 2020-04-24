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
log_file = None

#define empty array of trials to be used by trialhandler for loops
trials = []

#intervals in seconds possible for each trial
duration_levels = [1, 2, 3]
#defines 2 modality types, audio and visual
#-1 is audio and 1 is visual
modality_levels = [-1, 1]

for i in range(len(duration_levels)):
    duration = duration_levels[i]
for i in range(len(modality_levels)):
    modality = modality_levels[i]

for duration in duration_levels:
    for modality in modality_levels:
        #append trials based on duration and modality
        t = [duration, modality]
        #add t to trials
        trials.append(t)

#randomly shuffle between audio/visual trials with 1 of 3 possible durations
random.shuffle(trials)
###DELETE PRIOR TO SUBMISSION
print(trials)


def Instructions():
    #declare global variables
    global window
    global direction_prompt
    
    #initializes a window over which text and stimuli can be drawn
    window = visual.Window([1920, 1080], monitor = "testMonitor", color = 'white')
    
    #defines properties of the text stimulus to show instructions
    instr = visual.TextStim(window, height = 2, wrapWidth = 2, color = 'black', pos = (0, 0))
    
    #creates content of text displayed for pre-experiment instructions
    instr.text = 'DISPLAY INSTRUCTIONS HERE / Press any key to continue.'
    
    while not event.getKeys():
        #draw instructions on screen
        instr.draw()
        #flip window so instructions are visible to user
        window.flip()
    
    #get rid of instructions from the window
    window.flip()

#audio trial with no feedback
def TrialA():
    #declare global variables
    global window
    global kb
    global s
    global duration
    
    #initialize variable s which is the auditory stimulis wav file
    s = sound.Sound(value='440.wav')
    
    ##Estimation Epoch (EE)
    #start playing the tone
    s.play()
    #play the tone for a duration defined by "xa"
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
    #only accept space bar as response
    keys = kb.getKeys(keyList='space')
    #get start of RE for comparison to duration in later loops
    astart_time = core.getTime()
    #begin playing the sound
    s.play()
    
    while not('space' in keys):
        window.flip()
        keys = kb.getKeys('space')
    #stop the sound after space bar has been pressed
    s.stop()
    
    #note time that participant reproduction stops
    astop_time = core.getTime()
    #get duration of reproduction
    a_feedback = astop_time - astart_time
    
    #wait 2 seconds between trials for consistency with feedback being displayed for 2 seconds in other trials
    core.wait(2)

#visual trial with no feedback
def TrialV():
    global window
    global kb
    global log_file
    
    #initializes a window over which text and stimuli can be drawn
    window = visual.Window([1920, 1080], monitor = "testMonitor", color = 'white')
    
    ##Estimation Epoch (EE)
    #defines properties of the text stimulus to show instructions
    cross = visual.TextStim(window, text='+', height=0.3, wrapWidth=1, color='black', pos=(0, 0))
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
    #only get keyboard input from space bar
    keys = kb.getKeys('space')
    
    #define start of trial 
    vstart_time = core.getTime()
    
    while not event.getKeys('space'):
        #define properties of the cross
        cross = visual.TextStim(window, text='+', height=0.3, wrapWidth=1, color='black', pos=(0, 0))
        #draw cross on the window
        cross.draw()
        #flip window so participant can view stimulus
        window.flip()
    
    #define end of reproduction 
    vstop_time = core.getTime()
    #subtract the trial stop time from stop time to get duration of reproduction
    v_feedback = vstop_time - vstart_time
    
    #wait 2 seconds for consistency with 
    core.wait(2)

#audio trial with accurate feedback
def TrialAFeed1():
    #declare global variables
    global window
    global kb
    global s
    global duration
    
    #initialize variable s which is the auditory stimulis wav file
    s = sound.Sound(value='440.wav')
    
    ##Estimation Epoch (EE)
    #start playing the tone
    s.play()
    #play the tone for a duration defined by "xa"
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
    
    keys = []
    while not('space' in keys):
        window.flip()
        keys = kb.getKeys('space')
    #stop the sound after space bar has been pressed
    s.stop()
    
    #note time that participant reproduction stops
    astop_time = core.getTime()
    #subtrack trial start time from stop time to use for feedback loops
    a_feedback = astop_time - astart_time
    ##get rid of in final form
    print(a_feedback)
    
    #defines visual feedback on reproduction performance
    a_feed_text = visual.TextStim(window, height = 2, wrapWidth = 2, color = 'black', pos = (0, 0))
    
    #l is long, s is short, p is perfect
    if a_feedback > duration:
        #define properties of text feedback
        la_feed = visual.TextStim(window, height = 2, wrapWidth = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        la_feed.text = 'INTERVAL REPRODUCTION WAS TOO LONG'
        #draw text onto the window
        la_feed.draw()
    elif a_feedback < duration:
        #define properties of text feedback
        sa_feed = visual.TextStim(window, height = 2, wrapWidth = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        sa_feed.text = 'INTERVAL REPRODUCTION WAS TOO SHORT'
        #draw text onto the window
        sa_feed.draw()
    else: 
        #define properties of text feedback
        pa_feed = visual.TextStim(window, height = 2, wrapWidth = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        pa_feed.text = 'INTERVAL REPRODUCTION WAS PERFECT, GREAT JOB!'
        #draw text onto the window
        pa_feed.draw()
    
    #flip window to reveal feedback drawn from above loop
    window.flip()
    #display this feedback for 2 seconds
    core.wait(2)

#visual trial with accurate feedback
def TrialVFeed1():
    global window
    global kb
    global xv
    global log_file
    
    #initializes a window over which text and stimuli can be drawn
    window = visual.Window([1920, 1080], monitor = "testMonitor", color = 'white')
    
    ##Estimation Epoch (EE)
    #defines properties of the text stimulus to show instructions
    cross = visual.TextStim(window, text='+', height=0.3, wrapWidth=1, color='black', pos=(0, 0))
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
    #only get keyboard input from space bar
    #keys = kb.getKeys('space')
    
    #define start of trial 
    vstart_time = core.getTime()
    keys = []
    while not event.getKeys('space'):
        #define properties of the cross
        cross = visual.TextStim(window, text='+', height=0.3, wrapWidth=1, color='black', pos=(0, 0))
        #draw cross on the window
        cross.draw()
        #flip window so participant can view stimulus
        window.flip()
    
    #define end of reproduction 
    vstop_time = core.getTime()
    #subtract the trial stop time from stop time to get duration of reproduction
    v_feedback = vstop_time - vstart_time
    
    #define properties of feedback text
    v_feed_text = visual.TextStim(window, height = 2, wrapWidth = 2, color = 'black', pos = (0, 0))
    
    #l is long, s is short, p is perfect
    if v_feedback > duration:
        #define properties of text feedback
        lv_feed = visual.TextStim(window, height = 2, wrapWidth = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        lv_feed.text = 'INTERVAL REPRODUCTION WAS TOO LONG'
        #draw text onto the window
        lv_feed.draw()
    elif v_feedback < duration:
        #define properties of text feedback
        sv_feed = visual.TextStim(window, height = 2, wrapWidth = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        sv_feed.text = 'INTERVAL REPRODUCTION WAS TOO SHORT'
        #draw text onto the window
        sv_feed.draw()
    else:
        #define properties of text feedback
        pv_feed = visual.TextStim(window, height = 2, wrapWidth = 2, color = 'black', pos = (0, 0))
        #text participant sees after trial completion
        pv_feed.text = 'INTERVAL REPRODUCTION WAS PERFECT, GREAT JOB!'
        #draw text onto the window
        pv_feed.draw()
    
    #flip window to display drawn feedback text based on above loop
    window.flip()
    #display text for 2 seconds
    core.wait(2)

#encapsulation of termination sequences
def TerminateTask():
    #close the global window
    window.close()
    
    #quit the experiment
    core.quit()

Instructions()
#TrialA()
#TrialV()
TrialAFeed1()
TrialVFeed1()
#TrialAFeed2()
#TrialVFeed2()
TerminateTask()
