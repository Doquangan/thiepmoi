# 🎓 Hệ Thống Thiệp Mời Tốt Nghiệp Cá Nhân Hóa (HCMUS Graduation)

Dự án website thiệp mời tốt nghiệp cá nhân hóa dành riêng cho sinh viên tốt nghiệp (HCMUS — Class of 2026), sẵn sàng triển khai (deploy) trực tiếp lên **Vercel**.

---

## 🌟 Tính Năng Nổi Bật

1. **Trang Quản trị Bảo Mật (`/admin-server`)**:
   - **Mã bảo vệ PIN**: Truy cập bắt buộc nhập mã PIN bảo mật (mặc định ban đầu: `1111`).
   - **Đổi mã PIN**: Cho phép admin cập nhật mã PIN bất kỳ lúc nào ngay trên giao diện.
   - **Nút Khóa nhanh**: Cho phép khóa ngay phiên làm việc của admin khi rời máy.
   - Nhập tên bạn bè (Ví dụ: `Minh Khoa`, `Trần Bảo Ngọc`, `Thầy Cô`...).
   - Hệ thống tự động sinh đường dẫn endpoint riêng biệt: `https://ten-mien.vercel.app/Minh-Khoa`.
   - Sinh mã QR thời gian thực với màu đỏ rượu thương hiệu HCMUS (`#881337`).
   - Hỗ trợ cả tên có dấu tiếng Việt (`/Trần-Bảo-Ngọc`) và tên không dấu (`/tran-bao-ngoc`).
   - **Tải ảnh mã QR (PNG)** sắc nét để in hoặc gửi.
   - **Tải Thẻ Thiệp Mời Ảnh (Graduation QR Badge)** kích thước chuẩn dọc (1080x1350) có sẵn tên bạn bè và mã QR để gửi qua Messenger / Zalo / Instagram.
   - **Tạo hàng loạt (Batch Generation)**: Dán danh sách 20-50 bạn bè, hệ thống tự động tạo mã cho tất cả chỉ trong 1 giây!
   - **Quản lý danh sách khách mời**: Lưu tự động vào trình duyệt (`localStorage`), tìm kiếm, xuất file danh sách `.txt`.

2. **Thiệp Mời Cá Nhân Hóa (`/tên-của-bạn` & `/`)**:
   - Khi bạn bè quét mã QR hoặc bấm vào link `https://ten-mien.vercel.app/Minh-Khoa`, website tự động đọc tên từ đường dẫn URL.
   - Lời chào, tiêu đề trang và thư mời hiển thị đúng tên người đó: *"Gửi Minh Khoa,"*, *"Thư mời dành riêng cho Minh Khoa"*.
   - Khi truy cập trang chủ (`/`), thiệp mời hiển thị phiên bản thư mời chung.
   - **Hiệu ứng tương tác đĩa than (Vinyl Record Unlock)**: Chạm hạ kim đĩa than, phát hợp âm tốt nghiệp bằng Web Audio API và mở ra thiệp mời sang trọng mang phong cách báo chí (Editorial Design).
   - Tải tệp lịch hẹn `.ics` để lưu vào Google Calendar / Apple Calendar.
   - Xem bản đồ và định vị Google Maps đến trường ĐH Khoa học Tự nhiên (227 Nguyễn Văn Cừ).

---

## 📂 Cấu Trúc Thư Mục

```text
d:\thiepmoi\
├── admin.html          # Trang Admin Server (Bảo vệ bằng mã PIN 1111)
├── index.html          # Trang Thiệp mời tốt nghiệp chính
├── invite.html         # Trang Thiệp mời dự phòng
├── vercel.json         # Cấu hình routing cho Vercel (hỗ trợ /admin-server và /:name)
├── server.js           # Server chạy thử nghiệm cục bộ
├── package.json        # Định nghĩa dự án & lệnh chạy
├── README.md           # Tài liệu hướng dẫn sử dụng
└── assets/
    ├── qrcode.min.js   # Thư viện sinh mã QR offline
    ├── portrait.jpg    # (Tùy chọn) Ảnh chân dung cử nhân tốt nghiệp
    └── map.jpg         # (Tùy chọn) Ảnh sơ đồ khuôn viên trường
```

---

## 🚀 Hướng Dẫn Chạy Thử Tại Máy (Local)

Mở terminal tại thư mục dự án và chạy:

```bash
node server.js
```

Truy cập trên trình duyệt:
- 🔒 **Trang Quản trị (Admin Server)**: [http://localhost:3000/admin-server](http://localhost:3000/admin-server)
  - **Mã truy cập mặc định**: `1111`
- 💌 **Trang Thiệp mời tốt nghiệp**: [http://localhost:3000](http://localhost:3000)
- 👉 **Thiệp mời theo tên**: [http://localhost:3000/Minh-Khoa](http://localhost:3000/Minh-Khoa)

---

## 🌐 Hướng Dẫn Deploy Lên Vercel

1. Đẩy thư mục này lên repository trên GitHub của bạn:
   ```bash
   git add .
   git commit -m "Update admin-server route with PIN code protection"
   git push
   ```
2. Đăng nhập [Vercel](https://vercel.com) → Chọn **"Add New"** → **"Project"** → Chọn repo vừa tạo → Bấm **"Deploy"**.
3. Sau khi deploy xong:
   - Trang quản trị sẽ nằm ở: `https://ten-mien-cua-ban.vercel.app/admin-server`
   - Nhập mã PIN mặc định `1111` để mở khóa và bấm **"Đổi mã PIN"** để đặt mật mã mới của riêng bạn!
