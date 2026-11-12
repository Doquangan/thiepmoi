# 🎓 Hệ Thống Thiệp Mời Tốt Nghiệp Cá Nhân Hóa (HCMUS Graduation)

Dự án website thiệp mời tốt nghiệp cá nhân hóa dành riêng cho sinh viên tốt nghiệp (HCMUS — Class of 2026), sẵn sàng triển khai (deploy) trực tiếp lên **Vercel**.

---

## 🌟 Tính Năng Nổi Bật

1. **Trang Quản trị & Trình tạo mã QR (`/` hoặc `/admin`)**:
   - Nhập tên người bạn muốn mời (Ví dụ: `Minh Khoa`, `Trần Bảo Ngọc`, `Thầy Cô`...).
   - Hệ thống tự động sinh đường dẫn endpoint riêng biệt: `https://ten-mien.vercel.app/Minh-Khoa`.
   - Sinh mã QR thời gian thực với màu đỏ rượu thương hiệu HCMUS (`#881337`).
   - Hỗ trợ cả tên có dấu tiếng Việt (`/Trần-Bảo-Ngọc`) và tên không dấu (`/tran-bao-ngoc`).
   - **Tải ảnh mã QR (PNG)** sắc nét để in hoặc gửi.
   - **Tải Thẻ Thiệp Mời Ảnh (Graduation QR Badge)** kích thước chuẩn dọc (1080x1350) có sẵn tên bạn bè và mã QR để gửi qua Messenger / Zalo / Instagram.
   - **Tạo hàng loạt (Batch Generation)**: Dán danh sách 20-50 bạn bè, hệ thống tự động tạo mã cho tất cả chỉ trong 1 giây!
   - **Quản lý danh sách khách mời**: Lưu tự động vào trình duyệt (`localStorage`), tìm kiếm, xuất file danh sách `.txt`.

2. **Thiệp Mời Cá Nhân Hóa (`/tên-của-bạn`)**:
   - Khi bạn bè quét mã QR hoặc bấm vào link `https://ten-mien.vercel.app/Minh-Khoa`, website tự động đọc tên từ đường dẫn URL.
   - Lời chào, tiêu đề trang và thư mời hiển thị đúng tên người đó: *"Gửi Minh Khoa,"*, *"Thư mời dành riêng cho Minh Khoa"*.
   - **Hiệu ứng tương tác đĩa than (Vinyl Record Unlock)**: Chạm hạ kim đĩa than, phát hợp âm tốt nghiệp bằng Web Audio API và mở ra thiệp mời sang trọng mang phong cách báo chí (Editorial Design).
   - Tải tệp lịch hẹn `.ics` để lưu vào Google Calendar / Apple Calendar.
   - Xem bản đồ và định vị Google Maps đến trường ĐH Khoa học Tự nhiên (227 Nguyễn Văn Cừ).

---

## 📂 Cấu Trúc Thư Mục

```text
d:\thiepmoi\
├── index.html          # Trang Admin & Trình tạo mã QR
├── invite.html         # Trang Thiệp mời tốt nghiệp (kế thừa concept thiepmoihcmus.html)
├── vercel.json         # Cấu hình rewrite URL linh hoạt cho Vercel (hỗ trợ /:name)
├── server.js           # Server chạy thử nghiệm cục bộ (Zero-dependency)
├── package.json        # Định nghĩa dự án & lệnh chạy
├── README.md           # Tài liệu hướng dẫn sử dụng
└── assets/
    ├── qrcode.min.js   # Thư viện sinh mã QR offline
    ├── portrait.jpg    # (Tùy chọn) Ảnh chân dung cử nhân tốt nghiệp
    └── map.jpg         # (Tùy chọn) Ảnh sơ đồ khuôn viên trường
```

---

## 🚀 Hướng Dẫn Chạy Thử Tại Máy (Local)

Mở terminal tại thư mục dự án và chạy lệnh:

```bash
# Cách 1: Dùng lệnh Node trực tiếp
node server.js

# Hoặc Cách 2: Dùng npm
npm run dev
```

Truy cập trên trình duyệt:
- **Trang Admin**: `http://localhost:3000` hoặc `http://localhost:3000/admin`
- **Thiệp mời mẫu**: `http://localhost:3000/Minh-Khoa`

---

## 🌐 Hướng Dẫn Deploy Lên Vercel

### Cách 1: Qua GitHub (Đơn giản & Khuyên dùng)
1. Đẩy thư mục này lên một repository trên GitHub của bạn.
2. Đăng nhập [Vercel](https://vercel.com) bằng tài khoản GitHub.
3. Bấm **"Add New"** → **"Project"** → Chọn repository vừa tạo.
4. Giữ nguyên toàn bộ cấu hình mặc định và bấm **"Deploy"**.
5. Vercel sẽ cung cấp cho bạn một domain miễn phí (ví dụ: `https://thiepmoi-totnghiep.vercel.app`).

### Cách 2: Bằng Vercel CLI
Mở terminal tại thư mục này và chạy:
```bash
npx vercel
```
Làm theo các bước hướng dẫn trên màn hình (chọn `Y` và nhấn `Enter`).

> **Lưu ý quan trọng sau khi Deploy:**
> Sau khi có tên miền Vercel của bạn (ví dụ: `https://totnghiep-nam.vercel.app`), hãy truy cập vào trang Admin của bạn, bấm nút **"Thay đổi"** ở góc phải phần *Domain hệ thống* và dán tên miền của bạn vào. Mọi mã QR và link được tạo ra từ lúc đó sẽ tự động trỏ đến đúng tên miền Vercel chính thức!

---

## 🎨 Cách Tùy Chỉnh Thông Tin & Hình Ảnh

1. **Thông tin cử nhân & buổi lễ:**
   - Vào tab **"⚙️ Thông tin cử nhân"** ngay trên giao diện Admin để chỉnh sửa Tên, Ngày giờ, Địa điểm, Số điện thoại.
   - Hoặc chỉnh sửa trực tiếp trong file `invite.html` nếu muốn thay đổi nội dung thư mời.

2. **Ảnh chân dung & Sơ đồ trường:**
   - Để hiển thị ảnh chân dung của bạn cố định trên web mà không cần tải lên thủ công: Đặt file ảnh của bạn vào thư mục `assets/` với tên `portrait.jpg`.
   - Để hiển thị sơ đồ trường cố định: Đặt ảnh sơ đồ vào thư mục `assets/` với tên `map.jpg`.
