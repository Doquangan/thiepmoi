# Script to generate high-resolution invitation cards matching the new editorial style
import math
import os
from PIL import Image, ImageDraw, ImageFont

def render_invitation_card(
    guest_name="Việt Hoàng",
    school_name="Trường ĐH Khoa học Tự nhiên",
    univ_name="ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH",
    event_date_time="Thứ 5, 26.11.2026 • 11:00",
    venue_name="ĐH Khoa học Tự nhiên",
    venue_address="Cơ sở 1 – 227 Nguyễn Văn Cừ, Phường 4, Quận 5, TP. Hồ Chí Minh.",
    host_name="Đỗ Quang An",
    qr_image=None,
    output_path="assets/sample_card_viet_hoang.png"
):
    W, H = 1080, 1445
    im = Image.new("RGBA", (W, H), "#F7F3EA")
    draw = ImageDraw.Draw(im)

    # Load Windows fonts
    font_header_pill = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
    font_header_univ = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 19)
    font_title = ImageFont.truetype("C:/Windows/Fonts/timesbd.ttf", 94)
    font_tag = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 19)
    font_label = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
    font_guest = ImageFont.truetype("C:/Windows/Fonts/timesbd.ttf", 52)
    font_qr_sub = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
    font_col_label = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 19)
    font_col_val = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 29)
    font_col_addr = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 21)
    font_footer_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)
    font_footer_sig = ImageFont.truetype("C:/Windows/Fonts/timesi.ttf", 36)
    font_hcmus = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 24)

    # 1. Dot Grid background
    dot_spacing = 30.5
    dot_r = 1.6
    for x in range(15, W, 30):
        for y in range(15, H, 30):
            draw.ellipse([x - dot_r, y - dot_r, x + dot_r, y + dot_r], fill="#DDD6CB")

    # 2. Header
    header_y = 96
    pill_text = school_name.upper()
    pill_bbox = font_header_pill.getbbox(pill_text)
    pill_w = (pill_bbox[2] - pill_bbox[0]) + 52
    pill_h = 44

    univ_text = univ_name
    univ_bbox = font_header_univ.getbbox(univ_text)
    univ_w = univ_bbox[2] - univ_bbox[0]

    header_gap = 22
    total_header_w = pill_w + header_gap + univ_w
    start_x = (W - total_header_w) // 2

    # Draw pill
    draw.rounded_rectangle([start_x, header_y - pill_h // 2, start_x + pill_w, header_y + pill_h // 2], radius=pill_h // 2, fill="#F3D7DC")
    draw.text((start_x + pill_w // 2, header_y), pill_text, font=font_header_pill, fill="#5A1220", anchor="mm")
    draw.text((start_x + pill_w + header_gap, header_y), univ_text, font=font_header_univ, fill="#8A8278", anchor="lm")

    # 3. Title: Lễ Tốt Nghiệp.
    draw.text((W // 2, 218), "Lễ Tốt Nghiệp.", font=font_title, fill="#300A14", anchor="mm")

    # 4. Pill tag: GRADUATION INVITATION • CLASS OF 2026
    tag_y = 296
    tag_text = "GRADUATION INVITATION • CLASS OF 2026"
    tag_bbox = font_tag.getbbox(tag_text)
    tag_w = (tag_bbox[2] - tag_bbox[0]) + 60
    tag_h = 42
    draw.rounded_rectangle([(W - tag_w) // 2, tag_y - tag_h // 2, (W + tag_w) // 2, tag_y + tag_h // 2], radius=tag_h // 2, fill="#CDA799")
    draw.text((W // 2, tag_y), tag_text, font=font_tag, fill="#3A211A", anchor="mm")

    # 5. Recipient Section
    label_y = 352
    draw.text((W // 2, label_y), "THƯ MỜI THAM DỰ TRÂN TRỌNG GỬI ĐẾN", font=font_label, fill="#756A67", anchor="mm")

    guest_bbox = font_guest.getbbox(guest_name)
    gn_w = guest_bbox[2] - guest_bbox[0]
    box_w = max(460, min(W - 160, gn_w + 140))
    box_h = 76
    box_x = (W - box_w) // 2
    box_y = 380
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=16, fill="#FAF7F2", outline="#CDA799", width=2)
    draw.text((W // 2, box_y + box_h // 2), guest_name, font=font_guest, fill="#151111", anchor="mm")

    # 6. QR Container
    qr_card_w = 460
    qr_card_h = 440
    qr_card_x = (W - qr_card_w) // 2
    qr_card_y = 492
    draw.rounded_rectangle([qr_card_x, qr_card_y, qr_card_x + qr_card_w, qr_card_y + qr_card_h], radius=28, fill="#CDA095")

    inner_pad = 22
    inner_x = qr_card_x + inner_pad
    inner_y = qr_card_y + inner_pad
    inner_w = qr_card_w - inner_pad * 2
    inner_h = qr_card_h - inner_pad * 2
    draw.rounded_rectangle([inner_x, inner_y, inner_x + inner_w, inner_y + inner_h], radius=22, fill="#FFFFFF")

    # QR code
    qr_sz = 356
    qr_x = (W - qr_sz) // 2
    qr_y = inner_y + (inner_h - qr_sz) // 2
    if qr_image:
        qr_resized = qr_image.resize((qr_sz, qr_sz), Image.Resampling.LANCZOS)
        im.paste(qr_resized, (qr_x, qr_y))

    # Center Badge: HCMUS
    badge_w = 126
    badge_h = 48
    badge_x = (W - badge_w) // 2
    badge_y = qr_y + (qr_sz - badge_h) // 2
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=10, fill="#FFFFFF")
    draw.text((W // 2, badge_y + badge_h // 2), "HCMUS", font=font_hcmus, fill="#70142C", anchor="mm")

    # Subtitle below QR
    draw.text((W // 2, 966), "✦   QUÉT MÃ QR ĐỂ MỞ THIỆP MỜI & CHỈ ĐƯỜNG   ✦", font=font_qr_sub, fill="#70142C", anchor="mm")

    # 7. Divider lines & Two-Column Info
    line_y1 = 1008
    line_y2 = 1222
    line_x1 = 96
    line_x2 = W - 96
    draw.line([(line_x1, line_y1), (line_x2, line_y1)], fill="#D4CDC6", width=2)
    draw.line([(line_x1, line_y2), (line_x2, line_y2)], fill="#D4CDC6", width=2)

    # Column 1
    col1_x = line_x1
    draw.text((col1_x, 1042), "01 // THỜI GIAN", font=font_col_label, fill="#70142C", anchor="la")
    draw.text((col1_x, 1084), event_date_time, font=font_col_val, fill="#151111", anchor="la")

    # Column 2
    col2_x = 575
    draw.text((col2_x, 1042), "02 // ĐỊA ĐIỂM", font=font_col_label, fill="#70142C", anchor="la")
    draw.text((col2_x, 1084), venue_name, font=font_col_val, fill="#151111", anchor="la")

    # Address lines
    # Split address into 2 lines
    addr_line1 = "Cơ sở 1 – 227 Nguyễn Văn Cừ, Phường 4,"
    addr_line2 = "Quận 5, TP. Hồ Chí Minh."
    draw.text((col2_x, 1126), addr_line1, font=font_col_addr, fill="#66615D", anchor="la")
    draw.text((col2_x, 1156), addr_line2, font=font_col_addr, fill="#66615D", anchor="la")

    # 8. Footer Section
    draw.text((W // 2, 1266), "Rất hân hạnh được đón tiếp bạn trong ngày vui này!", font=font_footer_sub, fill="#6B635E", anchor="mm")
    draw.text((W // 2, 1320), f"Thân mời từ {host_name}", font=font_footer_sig, fill="#200D13", anchor="mm")

    # 4-point sparkle in bottom right
    # draw sparkle at (918, 1262)
    sp_x, sp_y, sp_sz = 918, 1262, 24
    draw.polygon([
        (sp_x, sp_y - sp_sz), (sp_x + sp_sz // 4, sp_y - sp_sz // 4),
        (sp_x + sp_sz, sp_y), (sp_x + sp_sz // 4, sp_y + sp_sz // 4),
        (sp_x, sp_y + sp_sz), (sp_x - sp_sz // 4, sp_y + sp_sz // 4),
        (sp_x - sp_sz, sp_y), (sp_x - sp_sz // 4, sp_y - sp_sz // 4)
    ], fill="#ECE7DD")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.convert("RGB").save(output_path, "PNG")
    print(f"Generated card saved to: {output_path}")

if __name__ == "__main__":
    ref_im = Image.open(r"C:\Users\anold\.gemini\antigravity\brain\3442d546-7e5c-4e54-8ded-1033760df313\.user_uploaded\media_1794672435780_3e46218d.jpg")
    qr_crop = ref_im.crop((239, 365, 525, 638))
    render_invitation_card(qr_image=qr_crop)
