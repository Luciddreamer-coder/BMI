
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.patches import Circle, Rectangle


MIN_BMI, MAX_BMI = 10, 50
BG_COLOR = "#0a0e27"
PANEL_COLOR = "#1a1f3a"

def angle(val):
    normalized = (val - MIN_BMI) / (MAX_BMI - MIN_BMI)
    return (5 * np.pi / 4) - (normalized * 3 * np.pi / 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#2196F3"
    elif bmi < 25:
        return "Normal", "#4CAF50"
    elif bmi < 30:
        return "Overweight", "#FF9800"
    else:
        return "Obese", "#F44336"


def draw_gauge(ax):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.0, 1.3)

    def arc(start, end, color, label):
        theta = np.linspace(angle(start), angle(end), 150)
        ax.plot(np.cos(theta), np.sin(theta),
                linewidth=28, color=color, solid_capstyle='round', alpha=0.9)
        
        mid = (start + end) / 2
        label_angle = angle(mid)
        ax.text(0.72*np.cos(label_angle), 0.72*np.sin(label_angle),
                label, color='white', ha='center', va='center', 
                fontsize=10, fontweight='bold')

    arc(10, 18.5, '#2196F3', 'Under')
    arc(18.5, 25, '#4CAF50', 'Normal')
    arc(25, 30, '#FF9800', 'Over')
    arc(30, 50, '#F44336', 'Obese')


    ax.text(0, 1.35, "BMI CALCULATOR", fontsize=22, ha='center', 
            color='#00FF88', fontweight='bold', family='monospace')

    for bmi_val in [18.5, 25, 30]:
        ang = angle(bmi_val)
        ax.plot([1.05*np.cos(ang), 1.15*np.cos(ang)], 
                [1.05*np.sin(ang), 1.15*np.sin(ang)],
                color='white', linewidth=2, alpha=0.5)
        ax.text(1.25*np.cos(ang), 1.25*np.sin(ang), 
                str(bmi_val), color='white', ha='center', 
                va='center', fontsize=8, alpha=0.7)

def update(val):
    height = height_slider.val
    weight = weight_slider.val
    age = age_slider.val
    
    bmi = weight / ((height / 100) ** 2)
    category, color = get_bmi_category(bmi)
    

    bmi_clamped = max(MIN_BMI, min(bmi, MAX_BMI))
    

    needle.set_data([0, 0.95*np.cos(angle(bmi_clamped))], 
                    [0, 0.95*np.sin(angle(bmi_clamped))])
    
  
    bmi_text.set_text(f"{bmi:.1f}")
    bmi_text.set_color(color)
    category_text.set_text(category.upper())
    category_text.set_color(color)
    
    height_val.set_text(f"{int(height)}")
    weight_val.set_text(f"{int(weight)}")
    age_val.set_text(f"{int(age)}")
    
    fig.canvas.draw_idle()

def update_gender(label):
    gender_val.set_text(label.upper())
    gender_val.set_color("#00D9FF" if label == "Male" else "#FF4D94")
    fig.canvas.draw_idle()


fig = plt.figure(figsize=(12, 8))
fig.patch.set_facecolor(BG_COLOR)


ax = plt.axes([0.35, 0.30, 0.5, 0.6])
ax.set_facecolor(BG_COLOR)
draw_gauge(ax)


h0, w0, a0 = 170, 70, 25
bmi0 = w0 / ((h0 / 100) ** 2)
cat0, col0 = get_bmi_category(bmi0)


needle, = ax.plot([0, 0.95*np.cos(angle(bmi0))], 
                  [0, 0.95*np.sin(angle(bmi0))],
                  color='white', linewidth=4, zorder=10)
ax.scatter(0, 0, s=250, color='white', zorder=11, edgecolors='#00FF88', linewidths=3)

bmi_text = ax.text(0, -0.35, f"{bmi0:.1f}", fontsize=48, 
                   fontweight='bold', ha='center', color=col0, family='monospace')
ax.text(0, -0.48, "BMI", fontsize=14, ha='center', color='white', alpha=0.7)
category_text = ax.text(0, -0.58, cat0.upper(), fontsize=16, 
                        fontweight='bold', ha='center', color=col0)


info_ax = plt.axes([0.05, 0.35, 0.25, 0.6])
info_ax.set_facecolor(PANEL_COLOR)
info_ax.set_xlim(0, 1)
info_ax.set_ylim(0, 1)
info_ax.axis('off')


rect = Rectangle((0.02, 0.01), 0.96, 0.98, fill=False, 
                 edgecolor='#00FF88', linewidth=2, alpha=0.3)
info_ax.add_patch(rect)

info_ax.text(0.5, 0.89, "YOUR STATS", ha='center', fontsize=14, 
             color='#00FF88', fontweight='bold')


info_ax.plot([0.1, 0.9], [0.84, 0.84], color='#00FF88', linewidth=1, alpha=0.3)


y_pos = 0.76
spacing = 0.13


info_ax.text(0.12, y_pos, "Gender", fontsize=11, color='white', alpha=0.7)
gender_val = info_ax.text(0.88, y_pos, "MALE", fontsize=11, 
                          color='#00D9FF', ha='right', fontweight='bold')
y_pos -= 0.04
info_ax.plot([0.1, 0.9], [y_pos, y_pos], color='white', linewidth=0.5, alpha=0.2)


y_pos -= 0.09
info_ax.text(0.12, y_pos, "Height", fontsize=11, color='white', alpha=0.7)
height_val = info_ax.text(0.72, y_pos, f"{h0}", fontsize=11, 
                          color='white', ha='right', fontweight='bold')
info_ax.text(0.74, y_pos, "cm", fontsize=9, color='white', alpha=0.5, ha='left')
y_pos -= 0.04
info_ax.plot([0.1, 0.9], [y_pos, y_pos], color='white', linewidth=0.5, alpha=0.2)


y_pos -= 0.09
info_ax.text(0.12, y_pos, "Weight", fontsize=11, color='white', alpha=0.7)
weight_val = info_ax.text(0.72, y_pos, f"{w0}", fontsize=11, 
                          color='white', ha='right', fontweight='bold')
info_ax.text(0.74, y_pos, "kg", fontsize=9, color='white', alpha=0.5, ha='left')
y_pos -= 0.04
info_ax.plot([0.1, 0.9], [y_pos, y_pos], color='white', linewidth=0.5, alpha=0.2)


y_pos -= 0.09
info_ax.text(0.12, y_pos, "Age", fontsize=11, color='white', alpha=0.7)
age_val = info_ax.text(0.72, y_pos, f"{a0}", fontsize=11, 
                       color='white', ha='right', fontweight='bold')
info_ax.text(0.74, y_pos, "yrs", fontsize=9, color='white', alpha=0.5, ha='left')


y_pos -= 0.06
info_ax.plot([0.1, 0.9], [y_pos, y_pos], color='#00FF88', linewidth=1, alpha=0.3)


y_pos = 0.24
info_ax.text(0.5, y_pos, "BMI RANGES", ha='center', fontsize=11, 
             color='#00FF88', fontweight='bold')
y_pos -= 0.07
info_ax.text(0.5, y_pos, "< 18.5  Underweight", ha='center', 
             fontsize=9, color='#2196F3', alpha=0.8)
y_pos -= 0.05
info_ax.text(0.5, y_pos, "18.5-25  Normal", ha='center', 
             fontsize=9, color='#4CAF50', alpha=0.8)
y_pos -= 0.05
info_ax.text(0.5, y_pos, "25-30  Overweight", ha='center', 
             fontsize=9, color='#FF9800', alpha=0.8)
y_pos -= 0.05
info_ax.text(0.5, y_pos, "> 30  Obese", ha='center', 
             fontsize=9, color='#F44336', alpha=0.8)


slider_left = 0.15
slider_width = 0.7

ax_h = plt.axes([slider_left, 0.20, slider_width, 0.03], facecolor=PANEL_COLOR)
ax_w = plt.axes([slider_left, 0.13, slider_width, 0.03], facecolor=PANEL_COLOR)
ax_a = plt.axes([slider_left, 0.06, slider_width, 0.03], facecolor=PANEL_COLOR)

height_slider = Slider(ax_h, 'Height (cm)', 140, 220, valinit=h0, 
                       color='#00FF88', track_color=PANEL_COLOR)
weight_slider = Slider(ax_w, 'Weight (kg)', 30, 150, valinit=w0, 
                       color='#00FF88', track_color=PANEL_COLOR)
age_slider = Slider(ax_a, 'Age (yrs)', 5, 100, valinit=a0, valstep=1, 
                    color='#00FF88', track_color=PANEL_COLOR)

for s in (height_slider, weight_slider, age_slider):
    s.label.set_color('white')
    s.label.set_fontsize(10)
    s.valtext.set_visible(False)

height_slider.on_changed(update)
weight_slider.on_changed(update)
age_slider.on_changed(update)


ax_g = plt.axes([0.88, 0.06, 0.1, 0.14], facecolor=PANEL_COLOR)
gender_radio = RadioButtons(ax_g, ('Male', 'Female'), active=0)


for lbl in gender_radio.labels:
    lbl.set_color('white')
    lbl.set_fontsize(10)

gender_radio.on_clicked(update_gender)

plt.show()
