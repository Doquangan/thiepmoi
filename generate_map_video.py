import math
import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 968
FPS = 24
TOTAL_FRAMES = 240
OUT_DIR = "d:/thiepmoi/temp_frames"

if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

# Fonts
try:
    font_header_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14)
    font_header_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
    font_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
    font_bld_sm = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
    font_reg = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    font_sm = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
    font_xs = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 10)
    font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14)
    font_big_i = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
except:
    font_header_title = font_header_sub = font_bold = font_bld_sm = font_reg = font_sm = font_xs = font_badge = font_big_i = ImageFont.load_default()

def draw_sparkle(draw, cx, cy, radius=8, color="#D97706"):
    r_in = radius * 0.25
    pts = [
        (cx, cy - radius),
        (cx + r_in, cy - r_in),
        (cx + radius, cy),
        (cx + r_in, cy + r_in),
        (cx, cy + radius),
        (cx - r_in, cy + r_in),
        (cx - radius, cy),
        (cx - r_in, cy - r_in)
    ]
    draw.polygon(pts, fill=color)

def make_icon(draw_func, size=40):
    scale = 4
    big_size = size * scale
    big_img = Image.new("RGBA", (big_size, big_size), (0, 0, 0, 0))
    d = ImageDraw.Draw(big_img)
    draw_func(d, big_size, scale)
    return big_img.resize((size, size), Image.Resampling.LANCZOS)

def draw_scooter_shape(d, size, s):
    d.ellipse([2 * s, 2 * s, size - 2 * s, size - 2 * s], fill="#881337", outline="#FFFFFF", width=int(2.5 * s))
    d.ellipse([9 * s, 23 * s, 18 * s, 32 * s], fill="#FFFFFF")
    d.ellipse([11.5 * s, 25.5 * s, 15.5 * s, 29.5 * s], fill="#881337")
    d.ellipse([23 * s, 23 * s, 32 * s, 32 * s], fill="#FFFFFF")
    d.ellipse([25.5 * s, 25.5 * s, 29.5 * s, 29.5 * s], fill="#881337")
    d.line([(14 * s, 25 * s), (22 * s, 25 * s), (27 * s, 15 * s), (24 * s, 13 * s)], fill="#FFFFFF", width=int(3 * s))
    d.line([(12 * s, 19 * s), (19 * s, 19 * s)], fill="#FFFFFF", width=int(3.5 * s))

def draw_walker_shape(d, size, s):
    d.ellipse([2 * s, 2 * s, size - 2 * s, size - 2 * s], fill="#881337", outline="#FFFFFF", width=int(2.5 * s))
    d.ellipse([16 * s, 7 * s, 24 * s, 15 * s], fill="#FFFFFF")
    d.line([(20 * s, 15 * s), (20 * s, 25 * s)], fill="#FFFFFF", width=int(3 * s))
    d.line([(20 * s, 25 * s), (14 * s, 33 * s)], fill="#FFFFFF", width=int(3 * s))
    d.line([(20 * s, 25 * s), (26 * s, 32 * s)], fill="#FFFFFF", width=int(3 * s))
    d.line([(14 * s, 19 * s), (26 * s, 21 * s)], fill="#FFFFFF", width=int(2.5 * s))

scooter_icon = make_icon(draw_scooter_shape, 40)
walker_icon = make_icon(draw_walker_shape, 40)

# Pre-render Student Chibi Avatar (68x68)
try:
    raw_student = Image.open("assets/student.png").convert("RGBA")
    student_thumb = raw_student.resize((64, 64), Image.Resampling.LANCZOS)
    student_avatar = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(student_avatar)
    sdraw.ellipse([0, 0, 71, 71], fill="#FEF3C7", outline="#D97706", width=2)
    smask = Image.new("L", (64, 64), 0)
    smdraw = ImageDraw.Draw(smask)
    smdraw.ellipse([0, 0, 63, 63], fill=255)
    student_avatar.paste(student_thumb, (4, 4), smask)
except Exception as e:
    print("Student load error:", e)
    student_avatar = None

# Render Base Static Map
base_img = Image.new("RGBA", (W, H), "#FBF9F5")
bdraw = ImageDraw.Draw(base_img)

# Millimeter grid
for x in range(0, W, 24):
    bdraw.line([(x, 0), (x, H)], fill="#F4EFE8", width=1)
for y in range(0, H, 24):
    bdraw.line([(0, y), (W, y)], fill="#F4EFE8", width=1)

# Card Box
card_x0, card_y0, card_x1, card_y1 = 32, 14, 688, 770
bdraw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=22, fill="#FCFBF9", outline="#D5CCC0", width=2)
bdraw.rounded_rectangle([card_x0 + 4, card_y0 + 4, card_x1 - 4, card_y1 - 4], radius=18, outline="#E8E2D7", width=1)

# Top route legend in card (clean, spacious top bar)
bdraw.text((360, card_y0 + 26), "— Đi xe máy", fill="#881337", font=font_bld_sm)
bdraw.line([(330, card_y0 + 34), (356, card_y0 + 34)], fill="#881337", width=3)
bdraw.polygon([(356, card_y0 + 31), (363, card_y0 + 34), (356, card_y0 + 37)], fill="#881337")

bdraw.text((530, card_y0 + 26), "--- Đi bộ", fill="#881337", font=font_bld_sm)
for bx in range(494, 524, 7):
    bdraw.line([(bx, card_y0 + 34), (bx + 3, card_y0 + 34)], fill="#881337", width=2)

# Street & Pavements
street_y0, street_y1 = 696, 766
bdraw.rectangle([card_x0 + 4, street_y0, card_x1 - 4, street_y1], fill="#D8D1C4")
for rx in range(card_x0 + 16, card_x1 - 16, 24):
    bdraw.line([(rx, (street_y0 + street_y1) // 2), (rx + 12, (street_y0 + street_y1) // 2)], fill="#FFFFFF", width=2)
bdraw.text((220, street_y0 + 14), "ĐƯỜNG NGUYỄN VĂN CỪ", fill="#4A4138", font=font_bold)

pavement_col = "#EFEAE0"
bdraw.rectangle([308, 180, 398, street_y0], fill=pavement_col)
bdraw.rectangle([116, 180, 660, 212], fill=pavement_col)
bdraw.rectangle([308, 400, 568, 446], fill=pavement_col)
bdraw.rectangle([530, 212, 568, street_y0], fill=pavement_col)
bdraw.rectangle([116, 212, 194, 446], fill=pavement_col)

def draw_bldg(draw, box, title, subtitle=None, is_ceremony=False, custom_title_font=None):
    bx0, by0, bx1, by1 = box
    draw.rounded_rectangle([bx0 + 2, by0 + 3, bx1 + 2, by1 + 3], radius=7, fill="#DFD8CE")
    b_fill = "#FFFDF7" if is_ceremony else "#FFFFFF"
    b_outline = "#881337" if is_ceremony else "#A3998C"
    draw.rounded_rectangle(box, radius=7, fill=b_fill, outline=b_outline, width=2 if is_ceremony else 1)
    if (bx1 - bx0) > 28 and (by1 - by0) > 28:
        draw.rounded_rectangle([bx0 + 4, by0 + 4, bx1 - 4, by1 - 4], radius=4, outline="#ECE6DC", width=1)
    t_font = custom_title_font or font_bold
    bbox = t_font.getbbox(title)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (bx0 + bx1 - tw) // 2
    ty = (by0 + by1 - th) // 2 - (8 if subtitle else 0)
    draw.text((tx, ty), title, fill="#881337" if is_ceremony else "#2A2421", font=t_font)
    if subtitle:
        sbox = font_xs.getbbox(subtitle)
        sw = sbox[2] - sbox[0]
        draw.text(((bx0 + bx1 - sw) // 2, ty + th + 4), subtitle, fill="#881337" if is_ceremony else "#73695F", font=font_xs)

# Buildings
draw_bldg(bdraw, [84, 28, 168, 108], "GĐ 2")
draw_bldg(bdraw, [114, 126, 168, 180], "H")
draw_bldg(bdraw, [174, 126, 660, 180], "F", "Dãy phòng F")

# DH Su Pham
bdraw.rounded_rectangle([42, 96, 78, 624], radius=6, fill="#F6F2EA", outline="#CFC4B4", width=1)
sp_chars = ["Đ","H"," ","S","Ư"," ","P","H","Ạ","M"," ","T","P",".","H","C","M"]
spy = 180
for ch in sp_chars:
    if ch != " ":
        bdraw.text((54, spy), ch, fill="#85796C", font=font_xs)
    spy += 16

draw_bldg(bdraw, [120, 218, 168, 400], "")
draw_bldg(bdraw, [194, 212, 248, 400], "C")

# Building B with arch facade motif
draw_bldg(bdraw, [254, 212, 308, 400], "B")
bdraw.arc([262, 220, 300, 260], start=180, end=0, fill="#B5ADA3", width=1)

draw_bldg(bdraw, [406, 212, 460, 400], "A")
draw_bldg(bdraw, [476, 212, 530, 400], "E")

# Flagpole
bdraw.ellipse([348, 350, 368, 370], fill="#881337", outline="#FBF9F5", width=2)
bdraw.line([(358, 340), (358, 362)], fill="#2B2625", width=2)
bdraw.polygon([(358, 340), (378, 346), (358, 352)], fill="#DC2626")
bdraw.text((328, 374), "Cột cờ", fill="#5A524A", font=font_sm)

draw_bldg(bdraw, [388, 446, 524, 516], "GĐ 1", "Giảng đường 1")
draw_bldg(bdraw, [388, 524, 524, 592], "VP", "Thông tin")
draw_bldg(bdraw, [576, 542, 678, 626], "TT", "Tin học")

# Nha I (Graduation Venue)
draw_bldg(bdraw, [194, 446, 298, 626], "I", "SẢNH TỐT NGHIỆP", is_ceremony=True, custom_title_font=font_big_i)

# Trees
tree_coords = [
    (308, 465), (308, 500), (308, 535), (308, 570), (308, 605),
    (386, 465), (386, 500), (386, 535), (386, 570), (386, 605),
    (332, 318), (382, 318)
]
for tx, ty in tree_coords:
    bdraw.ellipse([tx - 7, ty - 7, tx + 7, ty + 7], fill="#769878", outline="#4E7050", width=1)
    bdraw.ellipse([tx - 3, ty - 3, tx + 3, ty + 3], fill="#98B89A")

# Gates
bdraw.rectangle([338, 694, 368, 698], fill="#FCFBF9")
bdraw.text((318, 672), "Cổng chính", fill="#2A2421", font=font_bld_sm)
bdraw.rectangle([534, 694, 564, 698], fill="#FCFBF9")
bdraw.text((498, 664), "Cổng vào bãi xe", fill="#881337", font=font_bld_sm)

print("Base map prepared. Rendering 240 animated frames...")

def get_scooter_pos(t):
    if t <= 0.0:
        return 549, 675
    if t >= 1.0:
        return 450, 422
    d = t * 352.0
    if d <= 253.0:
        return 549, 675 - d
    else:
        return 549 - (d - 253.0), 422

def get_walker_pos(t):
    if t <= 0.0:
        return 450, 422
    if t >= 1.0:
        return 338, 525
    d = t * 215.0
    if d <= 112.0:
        return 450 - d, 422
    else:
        return 338, 422 + (d - 112.0)

for f in range(TOTAL_FRAMES):
    im = base_img.copy()
    draw = ImageDraw.Draw(im)

    active_step = 1
    if f >= 165:
        active_step = 3
    elif f >= 100:
        active_step = 3
    elif f >= 30:
        active_step = 2
    else:
        active_step = 1

    # Route progressive drawing
    if f < 30:
        scooter_x, scooter_y = 549, 675
        show_scooter = True
        show_walker = False
        show_avatar = False
        moto_progress = 0.0
    elif f < 100:
        moto_progress = (f - 30) / 70.0
        moto_eased = 0.5 - 0.5 * math.cos(moto_progress * math.pi)
        scooter_x, scooter_y = get_scooter_pos(moto_eased)
        show_scooter = True
        show_walker = False
        show_avatar = False
    else:
        scooter_x, scooter_y = 450, 422
        show_scooter = False
        moto_progress = 1.0

    # Draw motorbike trail
    if moto_progress > 0.0:
        if scooter_y < 675:
            draw.line([(549, 675), (549, max(422, scooter_y))], fill="#881337", width=3)
        if scooter_x < 549:
            draw.line([(549, 422), (scooter_x, 422)], fill="#881337", width=3)
    if moto_progress >= 1.0:
        draw.line([(549, 675), (549, 422)], fill="#881337", width=3)
        draw.line([(549, 422), (450, 422)], fill="#881337", width=3)
        draw.polygon([(450, 418), (442, 422), (450, 426)], fill="#881337")

    # Walking progress
    if f >= 100 and f < 165:
        walk_progress = (f - 100) / 65.0
        walk_eased = 0.5 - 0.5 * math.cos(walk_progress * math.pi)
        walker_x, walker_y = get_walker_pos(walk_eased)
        show_walker = True
        show_avatar = False
    elif f >= 165:
        walker_x, walker_y = 338, 525
        show_walker = False
        show_avatar = True
        walk_progress = 1.0
    else:
        walker_x, walker_y = 450, 422
        show_walker = False
        show_avatar = False
        walk_progress = 0.0

    # Draw walking dashed trail
    if walk_progress > 0.0:
        cur_wx, cur_wy = get_walker_pos(walk_progress)
        end_x = min(450, max(338, int(cur_wx)))
        for wx in range(end_x, 450, 8):
            draw.line([(wx, 422), (wx + 4, 422)], fill="#881337", width=3)
        if cur_wy > 422:
            for wy in range(422, int(cur_wy), 8):
                draw.line([(338, wy), (338, wy + 4)], fill="#881337", width=3)

    if walk_progress >= 1.0:
        for wx in range(338, 450, 8):
            draw.line([(wx, 422), (wx + 4, 422)], fill="#881337", width=3)
        for wy in range(422, 525, 8):
            draw.line([(338, wy), (338, wy + 4)], fill="#881337", width=3)

    # Step Markers
    # Marker 1 (Quẹt thẻ)
    m1_scale = 1.0 + 0.15 * math.sin(f * 0.2) if active_step == 1 else 1.0
    r1 = int(12 * m1_scale)
    draw.ellipse([549 - r1, 600 - r1, 549 + r1, 600 + r1], fill="#881337", outline="#FFFFFF", width=2)
    draw.text((545, 592), "1", fill="#FFFFFF", font=font_bld_sm)

    if active_step == 1:
        rip_r = 16 + (f % 20) * 1.5
        draw.ellipse([549 - rip_r, 675 - rip_r, 549 + rip_r, 675 + rip_r], outline="#881337", width=2)

    # Marker 2 (Bãi gửi xe)
    m2_fill = "#881337" if f >= 30 else "#A3998C"
    draw.ellipse([440, 410, 464, 434], fill=m2_fill, outline="#FFFFFF", width=2)
    draw.text((447, 415), "2", fill="#FFFFFF", font=font_bld_sm)
    if active_step == 2:
        draw.text((426, 392), "BÃI XE", fill="#881337", font=font_xs)

    # Marker 3 (Điểm hẹn)
    m3_fill = "#881337" if f >= 100 else "#A3998C"
    draw.ellipse([326, 546, 350, 570], fill=m3_fill, outline="#FFFFFF", width=2)
    draw.text((333, 551), "3", fill="#FFFFFF", font=font_bld_sm)
    draw.text((308, 576), "Điểm hẹn", fill="#881337", font=font_bld_sm)

    # Moving scooter icon
    if show_scooter:
        sx = int(scooter_x) - 20
        sy = int(scooter_y) - 20
        im.paste(scooter_icon, (sx, sy), scooter_icon)

    # Moving walker icon
    if show_walker:
        wx = int(walker_x) - 20
        wy = int(walker_y) - 20
        im.paste(walker_icon, (wx, wy), walker_icon)

    # Celebration at Point 3
    if show_avatar and student_avatar:
        pulse = math.sin((f - 165) * 0.15)
        # Bounded ripple inside central courtyard
        rip_rad = int(36 + 6 * pulse)
        draw.ellipse([338 - rip_rad, 492 - rip_rad, 338 + rip_rad, 492 + rip_rad], outline="#F59E0B", width=2)
        
        im.paste(student_avatar, (338 - 36, 492 - 36), student_avatar)
        
        tag_w, tag_h = 176, 24
        tag_x = 338 - tag_w // 2
        tag_y = 440
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=12, fill="#881337", outline="#D97706", width=2)
        
        draw_sparkle(draw, tag_x + 12, tag_y + 12, radius=5, color="#FDE68A")
        draw.text((tag_x + 22, tag_y + 5), "ĐỖ QUANG AN ĐÓN BẠN!", fill="#FFFFFF", font=font_xs)
        draw_sparkle(draw, tag_x + tag_w - 12, tag_y + 12, radius=5, color="#FDE68A")

        draw_sparkle(draw, 298, 470, radius=5 + 2 * pulse, color="#D97706")
        draw_sparkle(draw, 378, 470, radius=5 - 2 * pulse, color="#F59E0B")
        draw_sparkle(draw, 296, 516, radius=4 - 2 * pulse, color="#F59E0B")
        draw_sparkle(draw, 380, 516, radius=4 + 2 * pulse, color="#D97706")

    # Bottom Legend
    legend_y0 = 794
    legend_cards = [
        ("1", "Quẹt thẻ", "Cổng vào bãi xe", 42, 230),
        ("2", "Gửi xe", "Bãi xe sau GĐ 1", 254, 442),
        ("3", "Điểm hẹn", "Trước sảnh Nhà I", 466, 654)
    ]

    for idx, (num, l_title, l_desc, lx0, lx1) in enumerate(legend_cards):
        step_num = idx + 1
        is_active = (step_num == active_step)
        
        card_fill = "#FFFDF9" if not is_active else "#FEF2F2"
        card_border = "#D8CFC2" if not is_active else "#881337"
        draw.rounded_rectangle([lx0, legend_y0, lx1, legend_y0 + 100], radius=14, fill=card_fill, outline=card_border, width=2 if is_active else 1)
        
        badge_fill = "#881337" if is_active else "#6B5E52"
        badge_x = (lx0 + lx1) // 2
        badge_y = legend_y0 + 26
        draw.ellipse([badge_x - 14, badge_y - 14, badge_x + 14, badge_y + 14], fill=badge_fill, outline="#FFFFFF", width=2)
        
        nbb = font_badge.getbbox(num)
        nw, nh = nbb[2] - nbb[0], nbb[3] - nbb[1]
        draw.text((badge_x - nw // 2, badge_y - nh // 2 - 2), num, fill="#FFFFFF", font=font_badge)
        
        tbb = font_bold.getbbox(l_title)
        tw = tbb[2] - tbb[0]
        draw.text(((lx0 + lx1 - tw) // 2, legend_y0 + 48), l_title, fill="#881337" if is_active else "#2A2421", font=font_bold)
        
        dbb = font_sm.getbbox(l_desc)
        dw = dbb[2] - dbb[0]
        draw.text(((lx0 + lx1 - dw) // 2, legend_y0 + 72), l_desc, fill="#786D61", font=font_sm)

    for cx in range(232, 252, 6):
        draw.line([(cx, legend_y0 + 50), (cx + 3, legend_y0 + 50)], fill="#881337", width=2)
    for cx in range(444, 464, 6):
        draw.line([(cx, legend_y0 + 50), (cx + 3, legend_y0 + 50)], fill="#881337", width=2)

    im.convert("RGB").save(f"{OUT_DIR}/frame_{f:04d}.png")

print("All 240 frames rendered successfully!")
