# Raspberry Pi Server Setup (power.mysolarpower.store)

Tài liệu mô tả CHÍNH XÁC cách Pi này đã được cấu hình để chạy AC Management qua domain `https://power.mysolarpower.store`.

## 1) Tổng quan stack đang chạy
- Web app (Uvicorn/FastAPI) lắng nghe nội bộ: `127.0.0.1:8000`
- Caddy reverse proxy lắng nghe nội bộ: `127.0.0.1:8080` → proxy tới `127.0.0.1:8000`
- Cloudflare Tunnel trỏ domain → `http://127.0.0.1:8080`
- Systemd đảm nhiệm tự khởi động 2 dịch vụ: monitor (ghi DB) và web

Sơ đồ: Client → Cloudflare → cloudflared (tunnel) → Caddy:8080 → Uvicorn:8000 → App `web/api.py`

## 2) Biến môi trường (.env)
File: `/home/duy/ac_management/.env` (đã gitignore)
- `API_TOKEN` = mật khẩu đăng nhập `/login`
- `SECRET_KEY` = chuỗi ngẫu nhiên dài (ký session)
- `DISABLE_DOCS=true` = tắt `/docs` trong production
- `COOKIE_SECURE=true` = cookie chỉ dùng qua HTTPS/Tunnel

## 3) Dịch vụ systemd (stack giống `make run-server`)
Tạo 3 unit:

File: `/etc/systemd/system/acm-monitor.service`
```
[Unit]
Description=AC Management - Sensor Monitor (DB)
After=network.target

[Service]
User=duy
WorkingDirectory=/home/duy/ac_management
EnvironmentFile=/home/duy/ac_management/.env
ExecStart=/home/duy/miniconda3/bin/python /home/duy/ac_management/tools/read_ac_sensor_db.py
Restart=always

[Install]
WantedBy=acm.target
```

File: `/etc/systemd/system/acm-web.service`
```
[Unit]
Description=AC Management - Web Dashboard
After=network.target

[Service]
User=duy
WorkingDirectory=/home/duy/ac_management
EnvironmentFile=/home/duy/ac_management/.env
ExecStart=/home/duy/miniconda3/bin/python /home/duy/ac_management/run_web.py --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=acm.target
```

File: `/etc/systemd/system/acm.target`
```
[Unit]
Description=AC Management Stack (monitor + web)
Wants=acm-monitor.service acm-web.service
After=network.target

[Install]
WantedBy=multi-user.target
```

Kích hoạt:
```
sudo systemctl daemon-reload
sudo systemctl enable --now acm.target
```

Kiểm tra nhanh:
```
systemctl status --no-pager acm-monitor
systemctl status --no-pager acm-web
```

## 4) Cloudflare Tunnel
- Tên tunnel: `acm-dashboard`
- UUID: `1a409e5c-0140-44b2-b7dd-e91be0a51662`
- Domain: `power.mysolarpower.store` (CNAME về `<UUID>.cfargotunnel.com`)

File cấu hình: `/etc/cloudflared/config.yml`
```
tunnel: 1a409e5c-0140-44b2-b7dd-e91be0a51662
credentials-file: /etc/cloudflared/1a409e5c-0140-44b2-b7dd-e91be0a51662.json
ingress:
  - hostname: power.mysolarpower.store
    service: http://127.0.0.1:8080
  - service: http_status:404
```

Dịch vụ:
```
sudo systemctl enable --now cloudflared
sudo systemctl status --no-pager cloudflared
```

Thông tin/kiểm tra:
```
cloudflared tunnel list
cloudflared tunnel info acm-dashboard
```

## 5) Caddy reverse proxy
Caddy phục vụ cổng 8080 và proxy về Uvicorn 8000.

File: `/etc/caddy/Caddyfile`
```
:8080 {
  encode zstd gzip
  reverse_proxy 127.0.0.1:8000
}
```

Dịch vụ:
```
sudo systemctl enable --now caddy
sudo systemctl status --no-pager caddy
```

Gợi ý tối ưu (có thể áp dụng sau):
```
:8080 {
  encode zstd gzip
  handle_path /static/* {
    root * /home/duy/ac_management/web/static
    file_server
    header { Cache-Control "public, max-age=31536000, immutable" }
  }
  reverse_proxy 127.0.0.1:8000
}
```

## 6) Cổng và tiến trình
- App (Uvicorn): 127.0.0.1:8000
- Caddy: 127.0.0.1:8080
- Tunnel kết nối tới Caddy (8080) — không mở port công khai

## 7) Bảo mật ứng dụng
- Auth: đăng nhập tại `/login` (cookie HttpOnly)
- CSRF: bắt buộc header `X-Requested-With: XMLHttpRequest` với POST/DELETE/PUT/PATCH
- Origin: chấp nhận `X-Forwarded-Host`/`X-Forwarded-Proto` từ proxy/Tunnel
- Có thể tắt `/docs` bằng `DISABLE_DOCS=true`

## 8) Dữ liệu & backup
- Database: `/home/duy/ac_management/data/pzem_data.db`
- Backup nhanh:
```
cp data/pzem_data.db data/pzem_data_backup_$(date +%Y%m%d_%H%M%S).db
```

## 9) Cập nhật code & khởi động lại
```
cd /home/duy/ac_management
# (pull nếu dùng git)
# git pull
sudo systemctl restart acm-web        # chỉ web
sudo systemctl restart acm-monitor    # chỉ monitor
sudo systemctl restart cloudflared    # tunnel
sudo systemctl restart caddy          # proxy
```

## 10) Kiểm tra nhanh khi lỗi
```
# App nội bộ
curl -I http://127.0.0.1:8000/login
# Caddy proxy
curl -I http://127.0.0.1:8080/login
# Domain
curl -I https://power.mysolarpower.store/login
# Log dịch vụ
journalctl -u acm-web -e
journalctl -u acm-monitor -e
journalctl -u caddy -e
journalctl -u cloudflared -e
```

## 11) Ghi chú khác
- Tunnel/Cloudflare có thể gây thêm độ trễ so với `localhost`. Việc dùng Caddy giúp nén và có thể cache static.
- Nếu sửa Caddyfile, đảm bảo cú pháp chuẩn (có thể dùng `sudo caddy fmt --overwrite /etc/caddy/Caddyfile`).
- Nếu thay đổi subdomain/UUID, cập nhật `/etc/cloudflared/config.yml` và restart `cloudflared`.

---
Tài liệu này phản ánh cấu hình thực tế đang chạy trên Pi tại thời điểm cập nhật. Lưu cùng dự án để các agent/khác nắm được trạng thái hệ thống.
