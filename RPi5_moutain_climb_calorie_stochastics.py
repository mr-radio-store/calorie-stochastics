# =====================================================
# Stochastic Simulation: Calories Burned Walking Up Chiso Mountain
# Save per-person cumulative calories as JPEG plots
# =====================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# Create output folder
output_folder = "chiso_calories_plots"
os.makedirs(output_folder, exist_ok=True)

# =====================================================
# 1. Simulation Parameters
# =====================================================
num_people = 10
g = 9.81
step_height_avg = 0.18
step_height_sigma = 0.02
e_base = 0.25
mountain_elevation = 120.0
num_steps = int(mountain_elevation / step_height_avg)

# Randomly generate people attributes
weights = np.random.uniform(50, 90, num_people)
ages = np.random.randint(15, 70, num_people)

# =====================================================
# 2. Environment Noise Function
# =====================================================
def environmental_factor():
    temp = np.random.uniform(20, 35)
    temp_factor = 1 + 0.01 * (temp - 25)
    thirsty = np.random.uniform(0, 1)
    thirst_factor = 1 + 0.05 * thirsty
    wind = np.random.uniform(0, 5)
    wind_factor = 1 + 0.01 * wind
    unstable_sigma = step_height_sigma + np.random.uniform(0, 0.02)
    total_factor = temp_factor * thirst_factor * wind_factor
    return total_factor, unstable_sigma

# =====================================================
# 3. Efficiency Function (age-dependent)
# =====================================================
def efficiency(age):
    if age <= 50:
        return e_base
    else:
        return e_base * (1 - 0.005 * (age - 50))

# =====================================================
# 4. Initialize Tracking Variables
# =====================================================
calories_per_step = np.zeros((num_people, num_steps))
total_calories = np.zeros(num_people)
stop_step = np.zeros(num_people, dtype=int)

# =====================================================
# 5. Stochastic Simulation Loop
# =====================================================
STOP_THRESHOLD = 0.8

for i in range(num_people):
    w = weights[i]
    e = efficiency(ages[i])
    env_factor, sigma_h = environmental_factor()
    
    calories = 0.0
    for s in range(num_steps):
        h_i = np.random.normal(step_height_avg, sigma_h)
        work_joules = w * g * h_i
        step_calories = (work_joules / (e * 4184)) * env_factor
        calories += step_calories
        calories_per_step[i, s] = calories
        
        # Determine recommended stop
        if stop_step[i] == 0 and calories >= STOP_THRESHOLD * (calories + (num_steps - s - 1) * step_calories):
            stop_step[i] = s

    total_calories[i] = calories

# =====================================================
# 6. Save Individual Plots as JPEG
# =====================================================
for i in range(num_people):
    plt.figure(figsize=(8,5))
    plt.plot(range(num_steps), calories_per_step[i], 'b-', linewidth=2)
    plt.axvline(stop_step[i], color='r', linestyle='--', alpha=0.7,
                label=f'Recommended Stop ~ Step {stop_step[i]}')
    plt.xlabel("Step Number")
    plt.ylabel("Cumulative Calories Burned (kcal)")
    plt.title(f"Person {i+1}: Weight {weights[i]:.1f} kg, Age {ages[i]}")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    filename = os.path.join(output_folder, f"person_{i+1}_calories.jpeg")
    plt.savefig(filename, dpi=150)
    plt.close()

print(f"✓ Saved all individual cumulative calorie plots to '{output_folder}'")
