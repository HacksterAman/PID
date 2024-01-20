import random
import tkinter as tk

def add_noise(angle, mean=0, sigma=15):
    noise = random.gauss(mean, sigma)
    return angle + noise

def correct_angle(current, desired, Kp, Ki, Kd, error_threshold):
    integral = 0
    prev_error = 0
    error = desired - current
    results = []

    for t in range(1, 1000):
        current = add_noise(current)

        integral += error
        derivative = error - prev_error

        correction = Kp * error + Ki * integral + Kd * derivative

        current += correction
        current = current % 360

        prev_error = error
        error = desired - current

        results.append(f"t={t}, Change in Angle={correction:.2f}°, Current Angle={current:.2f}°")

        if abs(error) < error_threshold:
            break

    final_heading_label.config(text=f"Final Angle: {current:.2f}°")

    results_window = tk.Toplevel(root)
    results_window.title("Results")
    results_text = tk.Text(results_window)
    results_text.pack(fill=tk.BOTH, expand=True)

    for result in results:
        results_text.insert(tk.END, result + "\n")

root = tk.Tk()
root.title("Angle Correction with PID")

Kp_var = tk.DoubleVar(value=1.0)
Ki_var = tk.DoubleVar(value=0.1)
Kd_var = tk.DoubleVar(value=0.01)
current_var = tk.DoubleVar(value=0)
desired_var = tk.DoubleVar(value=360)
error_threshold_var = tk.DoubleVar(value=1)

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

root.mainloop()
