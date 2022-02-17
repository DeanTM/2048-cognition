import gym_2048
import gym
import keyboard

import json
from datetime import datetime
from time import time
import os

import numpy as np


DATA_FOLDER = 'data'
ACTION_LIST = ['left', 'up', 'right', 'down']

def clear_console():
    os.system('cls||clear')

def save_data(
    start_time, player_name,
    observations, times, key_presses, highest_number, rewards):
    if player_name:
        data = dict(
            player_name=player_name,
            times=times,
            observations=observations,
            key_presses=key_presses,
            highest_number=highest_number,
            rewards=rewards)
        with open(os.path.join(DATA_FOLDER, f"{start_time}.json"), 'w') as f:
            json.dump(data, f)

def run_game(topscore=0):
    clear_console()
    start_time = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    player_name = input(
        "What is your name (or unique identifier)?\nLeave blank to not save data.\n")
    env = gym.make('2048-v0')

    highest_number = 2
    times = []
    observations = []
    rewards = []
    key_presses = []
    done = False

    
    clear_console()
    score = 0
    print(f"Current score: {score}; Top score: {topscore}")
    obs = env.reset()
    env.render()
    display_time = time()

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            press_time = time()
            times.append(press_time - display_time)
            observations.append(obs)
            x = keyboard.read_key()
            if x in ACTION_LIST:
                key_presses.append(x)
                action = ACTION_LIST.index(x)
                clear_console()
                obs, reward, done, info = env.step(action)
                rewards.append(reward)
                score += reward
                if reward > highest_number:
                    highest_number = reward
                
                print(f"Current score: {score}; Top score: {topscore}; You pressed {x}")
                env.render()
                display_time = time()

            elif x == 'x':
                done = True
            if done:
                final_message = f"Game Over! Well played {player_name}!"\
                                if player_name else "Game Over!"
                print(final_message)
                break
    
    observations = [obs.tolist() for obs in observations]
    rewards = [int(rew) for rew in rewards]
    
    print("Times taken:")
    print(f"mean: {np.mean(times):.4f}, std: {np.std(times):.4f}")

    return start_time, player_name, observations, times, key_presses, int(highest_number), rewards, score


if __name__ == '__main__':    
    start_time, player_name, observations, times, key_presses, highest_number, rewards, score = run_game()
    save_data(start_time, player_name, observations, times, key_presses, highest_number, rewards)
    
    while True:
        print("\nEnter 'y' to play again.")
        play_again_event = keyboard.read_event()
        if play_again_event.event_type == keyboard.KEY_DOWN and keyboard.read_key() == 'y':
            start_time, player_name, observations, times, key_presses, highest_number, rewards, score = run_game(score)
            save_data(start_time, player_name, observations, times, key_presses, highest_number, rewards)
        elif play_again_event.event_type == keyboard.KEY_DOWN:
            print("Done. Thank you.")
            break
