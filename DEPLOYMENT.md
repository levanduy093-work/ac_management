# 🚀 Triển khai lên domain (Cloudflare Tunnel)

Hướng dẫn đưa dự án AC Management lên Internet an toàn, không mở port, hỗ trợ HTTPS và WebSocket.

## 1) Chuẩn bị
- Domain quản lý bởi Cloudflare (nameserver Cloudflare)
- Raspberry Pi/server chạy Ubuntu/Debian
- Dự án ở: `/home/duy/ac_management`

Tạo `.env` (gitignored):
```bash
cd /home/duy/ac_management
cat > .env << 'ENV'
API_TOKEN=<mat_khau_manh>
SECRET_KEY=<chuoi_ngau_nhien_dai>
DISABLE_DOCS=true
COOKIE_SECURE=true
ENV
```

## 2) Chạy stack bằng systemd (monitor + web)
```bash
# Web listens only on localhost
sudo tee /etc/systemd/system/acm-monitor.service >/dev/null << 'EOF'
[Unit]
Description=AC Management - Sensor Monitor (DB)
After=network.target

[Service]
User=duy
WorkingDirectory=/home/duy/ac_management
EnvironmentFile=/home/duy/ac_management/.env
ExecStart=$(command -v python) /home/duy/ac_management/tools/read_ac_sensor_db.py
Restart=always

[Install]
WantedBy=acm.target
EOF

sudo tee /etc/systemd/system/acm-web.service >/dev/null << 'EOF'
[Unit]
Description=AC Management - Web Dashboard
After=network.target

[Service]
User=duy
WorkingDirectory=/home/duy/ac_management
EnvironmentFile=/home/duy/ac_management/.env
ExecStart=$(command -v python) /home/duy/ac_management/run_web.py --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=acm.target
EOF

sudo tee /etc/systemd/system/acm.target >/dev/null << 'EOF'
[Unit]
Description=AC Management Stack (monitor + web)
Wants=acm-monitor.service acm-web.service
After=network.target

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now acm.target
```

## 3) Cài và tạo Cloudflare Tunnel
```bash
# Cài cloudflared (ARM64)
sudo apt-get update && sudo apt-get install -y cloudflared || true
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb -o cf.deb
sudo dpkg -i cf.deb

# Đăng nhập chọn zone domain (nếu chưa có cert)
[ -f "$HOME/.cloudflared/cert.pem" ] || cloudflared tunnel login

# Tạo tunnel và gán subdomain
cloudflared tunnel create acm-dashboard
cloudflared tunnel route dns acm-dashboard power.mysolarpower.store
```

Lấy Tunnel UUID:
```bash
cloudflared tunnel list | awk '/ acm-dashboard\b/ {print $1}'
```

Tạo cấu hình `/etc/cloudflared/config.yml`:
```bash
sudo tee /etc/cloudflared/config.yml >/dev/null << EOF
tunnel: <TUNNEL-UUID>
credentials-file: /etc/cloudflared/<TUNNEL-UUID>.json
ingress:
  - hostname: power.mysolarpower.store
    service: http://127.0.0.1:8000
  - service: http_status:404
EOF

sudo cp -f $HOME/.cloudflared/<TUNNEL-UUID>.json /etc/cloudflared/
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```

## 4) Kiểm tra
```bash
# Local app
curl -I http://127.0.0.1:8000/login  # 200 OK
# Tunnel
cloudflared tunnel info acm-dashboard
curl -I https://power.mysolarpower.store/login
```

## 5) Bảo mật
- Cookie HttpOnly, đăng nhập tại `/login` (API không dùng API key)
- CSRF header `X-Requested-With` và Origin check
- Tắt `/docs` bằng `DISABLE_DOCS=true`
- `COOKIE_SECURE=true` khi đi qua HTTPS/Tunnel

## 6) Troubleshooting
- 1033/530: xác minh Tunnel UUID trong `/etc/cloudflared/config.yml` khớp `cloudflared tunnel list`, và service `cloudflared` đang chạy
- 404: kiểm `ingress` hostname đúng subdomain
- 200 nội bộ nhưng lỗi ngoài: chờ DNS 1–5 phút hoặc kiểm tra Zero Trust/Tunnel status
