import random
import tkinter as tk

# Function to add noise to the angle
def add_noise(angle, mean=0, sigma=15):
    noise = random.gauss(mean, sigma)  # Gaussian noise with mean and standard deviation
    return angle + noise

# Function to correct the angle using PID control
def correct_angle(current, desired, Kp, Ki, Kd, error_threshold):
    integral = 0
    prev_error = 0
    error = desired - current
    results = []  # To store results for display

    # Loop until error is within threshold or maximum iterations reached
    for t in range(1, 1000):
        current = add_noise(current)  # Add noise to current angle

        integral += error  # Accumulate integral error
        derivative = error - prev_error  # Calculate derivative error

        # PID control equation
        correction = Kp * error + Ki * integral + Kd * derivative

        current += correction  # Apply correction to current angle
        current = current % 360  # Ensure angle wraps around to 0-360 range

        prev_error = error  # Update previous error
        error = desired - current  # Calculate new error

        # Store results for display
        results.append(f"t={t}, Change in Angle={correction:.2f}°, Current Angle={current:.2f}°")

        # Break loop if error is within threshold
        if abs(error) < error_threshold:
            break

    # Display final angle
    final_heading_label.config(text=f"Final Angle: {current:.2f}°")

    # Display results in a new window
    results_window = tk.Toplevel(root)
    results_window.title("Results")
    results_text = tk.Text(results_window)
    results_text.pack(fill=tk.BOTH, expand=True)

    # Insert results into the text widget
    for result in results:
        results_text.insert(tk.END, result + "\n")

# Create main window
root = tk.Tk()
root.title("Angle Correction with PID")

# Create variables to hold PID parameters and other values
Kp_var = tk.DoubleVar(value=1.0)
Ki_var = tk.DoubleVar(value=0.1)
Kd_var = tk.DoubleVar(value=0.01)
current_var = tk.DoubleVar(value=0)
desired_var = tk.DoubleVar(value=360)
error_threshold_var = tk.DoubleVar(value=1)

# Create UI elements for adjusting PID parameters and other values
Kp_label = tk.Label(root, text="Kp (Proportional Gain):")
Kp_scale = tk.Scale(root, variable=Kp_var, from_=0.1, to=2, resolution=0.01, orient="horizontal")

Ki_label = tk.Label(root, text="Ki (Integral Gain):")
Ki_scale = tk.Scale(root, variable=Ki_var, from_=0.01, to=0.2, resolution=0.01, orient="horizontal")

Kd_label = tk.Label(root, text="Kd (Derivative Gain):")
Kd_scale = tk.Scale(root, variable=Kd_var, from_=0.001, to=0.02, resolution=0.001, orient="horizontal")

current_label = tk.Label(root, text="Current Angle:")
current_scale = tk.Scale(root, variable=current_var, from_=0, to=360, resolution=1, orient="horizontal")

desired_label = tk.Label(root, text="Desired Angle:")
desired_scale = tk.Scale(root, variable=desired_var, from_=0, to=360, resolution=1, orient="horizontal")

error_threshold_label = tk.Label(root, text="Error Threshold:")
error_threshold_scale = tk.Scale(root, variable=error_threshold_var, from_=0.5, to=10, resolution=0.1, orient="horizontal")

start_button = tk.Button(root, text="Start Correction", command=lambda: correct_angle(current_var.get(), desired_var.get(), Kp_var.get(), Ki_var.get(), Kd_var.get(), error_threshold_var.get()))

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text)
final_heading_label = tk.Label(root, text="Final Angle: ")

# Pack UI elements into the main window
Kp_label.pack()
Kp_scale.pack()
Ki_label.pack()
Ki_scale.pack()
Kd_label.pack()
Kd_scale.pack()
current_label.pack()
current_scale.pack()
desired_label.pack()
desired_scale.pack()
error_threshold_label.pack()
error_threshold_scale.pack()
start_button.pack()
result_label.pack()
final_heading_label.pack()

# Start the main event loop
root.mainloop()
